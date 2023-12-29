from typing import Optional
from src.agents.agent import Agent
from src.environment.communication.Task import Task
from src.environment.communication.communication_layer import Message


class CommunicationChainAgent(Agent):
    def __init__(self, id: str, position, package=None, perception=None, algorithm_name=None, goal_package_point=None):
        super().__init__(id, position, package, perception, algorithm_name, goal_package_point)

    def receive_message(self, message: Message):
        print(f"Agent {self.id} received message: {message}")
        if message.type == "pickup_response" and message.value["response"] == "yes":
            print(f"Agent {self.id} accepted the pickup request. Assigning task...")
            # TODO: Implement task assignment logic

    def send_message(self, receiver_id: str, message_type: str, value: dict = None):
        message = Message(sender_id=self.id, receiver_id=receiver_id, type=message_type, value=value)
        self.broker.receive_message(message)

    def get_next_task(self) -> Optional[Task]:
        """
        Get the next task for the agent.

        Returns:
            Optional[Task]: The next task if available, else None.
        """
        # Check if the agent has a current package to deliver
        if self.package:
            target_position = self.package.destination.pos  # Deliver the current package
            task_type = Task.TaskType.DELIVER
            return Task(self.id, task_type, target_position, package=self.package)

        # Check for available packages to pick up
        pickup_point = self.package_point
        available_packages = pickup_point.packages
        if available_packages:
            target_package = available_packages[0]  # Pick up the first available package
            target_position = target_package.pos
            task_type = Task.TaskType.PICKUP
            return Task(self.id, task_type, target_position, package=target_package)

        return None  # No task available