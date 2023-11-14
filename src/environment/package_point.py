from typing import List

from src.utils.position import Position
from src.environment.package import Package
from src.environment.environment import Environment


class PackagePoint:
    def __init__(self, id: str, position: Position, max_simultaneous_packages_storage:float=float('inf')) -> None:
        self.id = id
        self.position = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage


    def current_packages(self, environment: Environment) -> List[Package]:
        """ Returns the list of packages in the package point."""
        pass
