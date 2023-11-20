from typing import List

from src.utils.position import Position

PACKAGE_POINT_START = 'pp-start'
PACKAGE_POINT_INTERMEDIATE = 'pp-intermediate'
PACKAGE_POINT_END = 'pp-end'

class PackagePoint:
    """ A point where the agent can leave a package, or pick up from."""
    def __init__(self, id: str, position: Position, point_type: str, max_simultaneous_packages_storage:float=float('inf')) -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the package point.
            position (Position): Position of the package point in the environment.
            point_type (str): Point type, possible options are defined in environment constants (i.e., 'end-point')
            max_simultaneous_packages_storage (float, optional): Maximum number of packages that can be stored simultaneously. Defaults to float('inf').
        """        
        self.id = id
        self.pos = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage
        self.point_type = point_type
