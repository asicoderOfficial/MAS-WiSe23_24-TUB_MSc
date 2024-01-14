import random
from typing import List
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.communication.Task import Task, TaskType
from src.environment.communication.communication_layer import MSG_PICKUP_REQUEST, MSG_PICKUP_RESPONSE, Message
from src.environment.package_point import PACKAGE_POINT_INTERMEDIATE
from src.agents.agent import Agent
from src.utils.position import Position


class RoamingAgent(Agent):
    def __init__(self, id: str, position: Position, packages: List[Package], perception: Perception, algorithm_name: str) -> None:
        super().__init__(id, position, packages, perception, algorithm_name)
        self.package_task = None
        
    def step(self, grid) -> None:
        current_perception = self.perception.percept(self.pos, grid)
        
        # if no package, walk randomly 
        if len(self.packages) == 0 and self.package_task is None:
            available_directions = self.algorithm.get_available_directions(self.pos, current_perception, grid)
            random_direction = random.choice(available_directions)
            self.move(self.pos + random_direction, current_perception, grid)
            return
        
        # move to task target, if there is one
        if self.package_task is not None and self.package_task.type == TaskType.PICKUP:
            if self.pos == self.package_task.target_position:
                package = [package for package in self.perception.visible_packages if package.id == self.package_task.package_id][0]
                self.pick_package(package, grid)
                self.package_task = None
                return
            else:
                next_pos = self.get_next_position(grid, self.package_task.target_position)
                self.move(next_pos, current_perception, grid)
                return
        
        # currently holding package
        if self.pos == self.packages[0].destination:
            # deliver
            package_point = [pp for pp in self.perception.visible_package_points if pp.pos == self.pos][0]
            for package in self.packages:
                self.deliver_package(package, package_point, grid)
        else:
            # go to package point
            next_pos = self.get_next_position(grid, self.packages[0].destination)
            self.move(next_pos, current_perception, grid)
            
    def receive_message(self, message: Message) -> Message:
        if message.type == MSG_PICKUP_REQUEST:
            # TODO: probably need more complex strategy here
            if self.package_task is not None or len(self.packages) != 0:
                return Message(MSG_PICKUP_RESPONSE, self.id, message.sender_id, {"response": "no"})
            else:
                new_task = Task(TaskType.PICKUP, message.value["package_id"], message.value["pos"])
                self.package_task = new_task
                return Message(MSG_PICKUP_RESPONSE, self.id, message.sender_id, {"response": "yes"})
                

        return None