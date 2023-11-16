from typing import List

from src.utils.position import Position


class PackagePoint:
    """ A point where the agent can leave a package, or pick up from."""
    def __init__(self, id: str, position: Position, max_simultaneous_packages_storage:float=float('inf')) -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the package point.
            position (Position): Position of the package point in the environment.
            max_simultaneous_packages_storage (float, optional): Maximum number of packages that can be stored simultaneously. Defaults to float('inf').
        """        
        self.id = id
        self.position = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage
