from typing import Optional, Union, Dict

from src.environment.package import Package
from src.utils.position import Position


class TaskType:
    PICKUP = "PICKUP"
    DELIVER = "DELIVER"

class Task:
    def __init__(self, task_type: str, package: Optional[Package], target_position: Position) -> None:
        """
        Constructor for the Task class.

        Args:
            task_type (str): Type of the task (PICKUP or DELIVER).
            package (Union[None, Package]): The package associated with the task (None for DELIVER tasks).
            target_position (Position): The target position for the task.
        """
        self.task_type = task_type
        self.package = package
        self.target_position = target_position