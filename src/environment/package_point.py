from typing import List

from src.utils.position import Position


class PackagePoint:
    def __init__(self, id: str, position: Position, max_simultaneous_packages_storage:float=float('inf')) -> None:
        self.id = id
        self.position = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage
