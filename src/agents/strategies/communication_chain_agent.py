from typing import Optional
from src.agents.strategies.chain_agent import ChainAgent
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.agents.agent import Agent
from src.environment.communication.Task import Task
from src.environment.communication.communication_layer import MSG_DELIVERY_NOTIFY, MSG_PICKUP_RESPONSE, CommunicationLayer, Message


class CommunicationChainAgent(ChainAgent):
    def __init__(self, id: str, position, packages, perception: Perception, goal_package_point_type: str, algorithm_name: str):
        super().__init__(id, position, packages, perception, goal_package_point_type, algorithm_name)

    def receive_message(self, message: Message):
        print(f"Agent {self.id} received message: {message}")
        # if message.type == MSG_PICKUP_RESPONSE and message.value["response"] == "yes":
        #     print(f"Package accepted the pickup request. Assigning task...")
            # TODO: Implement task assignment logic

    def deliver_package(self, package: Package, package_point: PackagePoint, grid) -> None:
        super().deliver_package(package, package_point, grid)
        message = Message(sender_id=self.id, destination_id="broker", type=MSG_DELIVERY_NOTIFY, value={"package_id": package.id, "pos": package_point.pos})
        CommunicationLayer.send_to_broker(message)

    # def get_next_task(self) -> Optional[Task]:
    #     """
    #     Get the next task for the agent.

    #     Returns:
    #         Optional[Task]: The next task if available, else None.
    #     """
    #     # Check if the agent has a current package to deliver
    #     if self.package:
    #         target_position = self.package.destination.pos  # Deliver the current package
    #         task_type = Task.TaskType.DELIVER
    #         return Task(self.id, task_type, target_position, package=self.package)

    #     # Check for available packages to pick up
    #     pickup_point = self.package_point
    #     available_packages = pickup_point.packages
    #     if available_packages:
    #         target_package = available_packages[0] # Pick up the first available package
    #         target_position = target_package.pos
    #         task_type = Task.TaskType.PICKUP
    #         return Task(self.id, task_type, target_position, package=target_package)

    #     return None  # No task available