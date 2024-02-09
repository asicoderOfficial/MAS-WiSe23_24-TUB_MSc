from collections import defaultdict
from copy import deepcopy
import itertools
from math import floor
from queue import Queue
import random

from typing import List
from src.agents.tips_functions import linear_decreasing_time_tips
from src.environment.communication.communication_layer import MSG_BID_ACCEPT, MSG_BID_REJECT, MSG_DELIVERY_ANNOUNCE, MSG_PLACE_BID, CommunicationLayer, Message
from src.agents.agent import Agent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.utils.position import Position
from src.constants.utility_functions import UTILITY_FUNCTIONS, UTILITY_FUNCTIONS_WITH_ONLY_ONE_ACTION, UTILITY_FUNCTIONS_WITH_ALL_POSSIBLE_ACTIONS


class WaiterCNP(Agent):
    def __init__(self, id: str, position: Position, package: List[Package], perception: Perception, movement_algorithm: str, 
                 utility_function:str, tips_function, starting_package_point_pos:Position, max_packages:int=3, utility_kwargs:dict={}) -> None:
        super().__init__(id, position, package, perception, movement_algorithm)
        self.max_packages = max_packages
        self.speed = self.max_packages + 1
        self.utility_function = utility_function
        self.utility_function_kwargs = utility_kwargs
        # self.current_action = ()
        self.scheduled_actions_queue = []
        self.collected_tips = 0
        self.table_served = 0
        self.tips_function = tips_function
        self.starting_package_point_pos = starting_package_point_pos
        self.bidded_pickups = [] 
        
    
    def step(self, grid) -> None:
        if len(self.scheduled_actions_queue) > 0:
            # while self.is_action_completed(self.scheduled_actions_queue[0]):
            #     self.scheduled_actions_queue.pop(0)
            
            current_action = self.scheduled_actions_queue[0]
            self.perform_action(current_action, grid)
            
            if "go" in current_action[0] and self.pos.x == current_action[1].x and self.pos.y == current_action[1].y:
                self.scheduled_actions_queue.pop(0)
            # action_completed = self.is_action_completed(current_action)
            # if current_action[0] == 'pick' and not action_completed:
            #     # Corner case: the agent performed the pick action, but the package was already picked up by another agent just before, in the same iteration
            #     # We have to make the agent forget about the action and re-evaluate the possible actions, as if not, the agent will be stuck in the same pick action without being able to perform it

            #     self.scheduled_actions_queue.pop(0)
            # if current_action[0] != 'pick' and current_action[0] != 'deliver':
            #     self.scheduled_actions_queue.pop(0)
        else:
            # If the agent is not carrying the maximum number of packages and there are packages in the environment
            perception = self.perception.percept(self.pos, grid)
            # possible_actions = self.get_possible_actions(perception)
            possible_actions = []
            if not possible_actions:
                possible_directions = self.algorithm.get_available_directions(self.pos, perception, grid)
                possible_positions = [self.pos + direction for direction in possible_directions]
                random_position = random.choice(possible_positions)
                best_action = ('go-random', random_position)
            else:
                # Evaluate the possible actions and pick the best one according to the utility function
                best_action = self.evaluate_actions(possible_actions, grid)

            # Perform the best action
            self.perform_action(best_action, grid)
            
    def get_possible_actions(self, perception):
        possible_actions = []

        for _, entities in perception.items():
            for entity in entities:
                if entity.pos.x == self.pos.x and entity.pos.y == self.pos.y:
                    if isinstance(entity, Package) and not entity.picked and len(self.packages) < self.max_packages and entity not in self.packages:
                        # The agent can pick up the package, as no other agent has picked it up
                        # it is not carrying the maximum number of packages and the package is not already being carried by the agent itself
                        possible_actions.append(('pick', entity))
                    elif isinstance(entity, PackagePoint):
                        for package in self.packages:
                            if package.destination == entity.pos:
                                # The agent can deliver a package to the package point
                                possible_actions.append(('deliver', entity, package))

        # If the agent is carrying packages, it can move to the delivery point
        if self.packages:
            for package in self.packages:
                if package.destination.x != self.pos.x and package.destination.y != self.pos.y:
                    possible_actions.append(('go-deliver', package.destination)) 

        # If the agent is not at the starting package point where packages spawn, it can move to it
        if self.pos.x != self.starting_package_point_pos.x and self.pos.y != self.starting_package_point_pos.y:
            possible_actions.append(('go-start', self.starting_package_point_pos))
    
        return possible_actions

    def evaluate_actions(self, possible_actions: List, grid) -> tuple:
        if self.utility_function in UTILITY_FUNCTIONS_WITH_ONLY_ONE_ACTION:
            return max([(action, UTILITY_FUNCTIONS[self.utility_function](action, grid, self)) for action in possible_actions], key=lambda x: x[1])[0]
        else:
            return max(UTILITY_FUNCTIONS[self.utility_function](possible_actions, grid, self), key=lambda x: x[0])


    def perform_action(self, best_action: tuple, grid) -> None:
        # print(best_action)
        # if len(best_action) == 3 and best_action[0] != 'deliver':
        #     best_action = (best_action[1], best_action[2])
        # elif len(best_action) == 4:
        #     best_action = (best_action[1], best_action[2], best_action[3])
        # print('best action', best_action)
        # Perform the best action
        if best_action[0] == 'pick':
            packages_to_pick = [best_action[1]]
            pick_further = True
            while pick_further and len(self.scheduled_actions_queue) > 0:
                action = self.scheduled_actions_queue[0]
                if action[0] == "pick":
                    packages_to_pick.append(action[1])
                    self.scheduled_actions_queue.pop(0)
                else:
                    pick_further = False
            
            for pp_package in packages_to_pick:    
                if pp_package in self.packages:
                    continue
                super().pick_package(pp_package, grid)
                self.speed -= 1
            # self.current_action = ()
        elif best_action[0] == 'deliver':
            pp_packages_to_deliver = [(best_action[2], best_action[1])]
            deliver_further = True
            while deliver_further and len(self.scheduled_actions_queue) > 0:
                action = self.scheduled_actions_queue[0]
                if action[0] == "deliver":
                    pp_packages_to_deliver.append((action[1], action[2]))
                    self.scheduled_actions_queue.pop(0)
                else:
                    deliver_further = False
            
            for pp_package in pp_packages_to_deliver:   
                if pp_package[0] not in self.packages:
                    continue
                self.deliver_package(pp_package[0], pp_package[1], grid)
                self.speed += 1
            # self.current_action = ()
        else:
            steps_left = self.speed
            while steps_left > 0:
                perception = self.perception.percept(self.pos, grid)
                if best_action[0] == 'go-random':
                    super().move(best_action[1], perception, grid)
                    # self.current_action = ()
                elif 'go' in best_action[0] and (best_action[1].x, best_action[1].y) != (self.pos.x, self.pos.y):
                    next_position = super().get_next_position(grid, best_action[1])
                    super().move(next_position, perception, grid)
                    if self.pos.x == best_action[1].x and self.pos.y == best_action[1].y:
                        steps_left = 0
                    # else:
                        # Continue moving towards the goal
                        # self.current_action = best_action
                
                steps_left -= 1
                
    def deliver_package(self, package: Package, package_point: PackagePoint, grid) -> None:
        super().deliver_package(package, package_point, grid)
        
        # Collect tips
        self.table_served += 1
        self.collected_tips += self.tips_function(package)

    def is_action_completed(self, action) -> bool:
        if "go" in action[0] and self.pos.x == action[1].x and self.pos.y == action[1].y:
            return True
        if "pick" in action[0] and action[1] in self.packages:
            return True
        return False

    def receive_message(self, message: Message) -> Message:
        if message.type == MSG_DELIVERY_ANNOUNCE:
            if self.speed == 1:
                return Message(MSG_PLACE_BID, self.id, message.sender_id, {"package": message.value["package"], "response": "no"})

            current_utility = self.estimate_delivery_tips(self.scheduled_actions_queue)
            
            # possible_actions_plan = deepcopy(self.scheduled_actions_queue)
            # possible_actions_plan.append(("go-start", self.starting_package_point_pos))
            # possible_actions_plan.append(("pick", message.value["package"]))
            # possible_actions_plan.append(("go-deliver", message.value["package"].destination))
            # possible_actions_plan.append(("deliver",  message.value["package"].destination_pp, message.value["package"]))
            
            schedule, utility = self.get_optimal_schedule(message.value["package"])
            if utility > current_utility:
                self.bidded_pickups.append(message.value["package"])
                return Message(MSG_PLACE_BID, self.id, message.sender_id, {"package": message.value["package"], "response": "yes", "bid": utility - current_utility})
            else: 
                return Message(MSG_PLACE_BID, self.id, message.sender_id, {"package": message.value["package"], "response": "no"})
            
        elif message.type == MSG_BID_ACCEPT:
            print(f"Agent {self.id} got bid accept message")
            # possible_actions_plan = deepcopy(self.scheduled_actions_queue)

            schedule, _ = self.get_optimal_schedule(message.value["package"])
            self.scheduled_actions_queue = schedule

        
        
    def get_optimal_schedule(self, new_package_to_deliver):
        """
        Gets optimal sequence of actions, in terms of delivery tips 
        """
        
        
        scheduled_packages = [action[1] for action in self.scheduled_actions_queue if action[0] == "pick"]
        
        delivery_sequence = []
        delivery_sequence.append(("go-start", self.starting_package_point_pos))
        delivery_sequence.append(("pick", new_package_to_deliver))
        delivery_sequence.append(("go-deliver", new_package_to_deliver.destination))
        delivery_sequence.append(("deliver", new_package_to_deliver.destination_pp, new_package_to_deliver))
        
        schedules = []
        schedules.append(delivery_sequence + self.scheduled_actions_queue)
        schedules.append(self.scheduled_actions_queue + delivery_sequence)
        
        for package in scheduled_packages:
            new_schedule = deepcopy(self.scheduled_actions_queue)
            pick_index = -1
            for i, action in enumerate(new_schedule):
                if action[0] == "pick" and action[1].id == package.id:
                    pick_index = i
                    break
            new_schedule.insert(pick_index, ("pick", new_package_to_deliver))
            
            if package.destination == new_package_to_deliver.destination:
                # there is package with the same destination
                for i, action in enumerate(new_schedule):
                    if i > pick_index and action[0] == "deliver" and action[2].id == package.id:
                        deliver_index = i
                        break
                new_schedule.insert(deliver_index, ("deliver", new_package_to_deliver.destination_pp, new_package_to_deliver))
            else:
                # deliver after delivering the package with nearest destination
                nearest_package_delivery = min(scheduled_packages, key=lambda x: x.destination.dist_to(new_package_to_deliver.destination))
                for i, action in enumerate(new_schedule):
                    if i > pick_index and action[0] == "deliver" and action[2].id == nearest_package_delivery.id:
                        deliver_index = i
                        break
                else:
                    continue
                new_schedule.insert(deliver_index, ("deliver", new_package_to_deliver.destination_pp, new_package_to_deliver))
            schedules.append(new_schedule)
        
        max_schedule = []
        max_utility = 0
        for schedule in schedules:
            picked_up = set()
            current_position = self.pos
            schedule_possible = True
            
            # check possibility of a schedule
            for action in schedule:
                if action[0] == "deliver":
                    if action[2] not in picked_up:
                        schedule_possible = False
                    elif action[2].destination != current_position:
                        schedule_possible = False
                elif action[0] == "pick":
                    picked_up.add(action[1])
                    if current_position != self.starting_package_point_pos:
                        schedule_possible = False
                elif action[0] == "go-start":
                    current_position = self.starting_package_point_pos
                elif action[0] == "go-deliver":  
                    current_position = action[1]
                
                if not schedule_possible:
                    break
            
            if schedule_possible:
                utility = self.estimate_delivery_tips(schedule)
                if utility > max_utility:
                    max_utility = utility
                    max_schedule = schedule
                    
        max_schedule = [step for step in max_schedule] 
        return max_schedule, max_utility
        
    def estimate_delivery_tips(self, scheduled_actions):
        """
        This utility function counts the delivery time of all packages in the schedule. 
        It uses the current iteration of the package, 
        as well as the number of steps that it will take to deliver it
        """
        tips = 0
        current_pos = self.pos
        current_time = 0
        current_speed = self.speed 
        for action in scheduled_actions:
            if current_speed == 0:
                return 0
                    
            if action[0] == "go-start":
                current_time += floor(current_pos.dist_to(action[1]) / current_speed)
                current_pos = action[1]
            elif action[0] == "go-deliver":
                current_time += floor(current_pos.dist_to(action[1]) / current_speed)
                current_pos = action[1]
            elif action[0] == "pick":
                current_speed -= 1
            elif action[0] == "deliver":
                tips += linear_decreasing_time_tips(action[2], current_time)
                current_speed += 1
        
        return tips