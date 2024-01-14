from typing import Optional, Union, Dict

from src.environment.package import Package
from src.utils.position import Position


class TaskType:
    PICKUP = "PICKUP"
    DELIVER = "DELIVER"

class Task:
    def __init__(self, task_type: str, package_id: str, target_position: Position) -> None:
        """
        Constructor for the Task class.

        Args:
            task_type (str): Type of the task (PICKUP or DELIVER).
            package (str): The package id associated with the task (None for DELIVER tasks).
            target_position (Position): The target position for the task.
        """
        self.type = task_type
        self.package_id = package_id
        self.target_position = target_position