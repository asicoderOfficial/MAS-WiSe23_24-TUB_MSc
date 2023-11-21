from typing import List, Union

from src.utils.position import Position

PACKAGE_POINT_START = 'pp-start'
PACKAGE_POINT_INTERMEDIATE = 'pp-intermediate'
PACKAGE_POINT_END = 'pp-end'

class PackagePoint:
    """ A point where the agent can leave a package, or pick up from."""
    def __init__(self, id: str, position: Position, point_type: str, max_simultaneous_packages_storage:float=float('inf'), steps_per_package:Union[int, None]=None) -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the package point.
            position (Position): Position of the package point in the environment.
            point_type (str): Point type, possible options are defined in environment constants (i.e., 'end-point')
            max_simultaneous_packages_storage (float, optional): Maximum number of packages that can be stored simultaneously. Defaults to float('inf').
            steps_per_package (Union[int, None]): Number of steps that should pass before a new package is generated. Defaults to None, which means that no new packages will be generated.
        """        
        self.id = id
        self.pos = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage
        self.point_type = point_type
        self.steps_per_package = steps_per_package
        self.previous_package_generation_step = -1
