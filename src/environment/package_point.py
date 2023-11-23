from typing import List, Union
import random

from src.utils.position import Position
from src.environment.package import Package
from src.visualization.save import Save

PACKAGE_POINT_START = 'pp-start'
PACKAGE_POINT_INTERMEDIATE = 'pp-intermediate'
PACKAGE_POINT_END = 'pp-end'

class PackagePoint:
    """ A point where the agent can leave a package, or pick up from."""
    def __init__(self, id: str, position: Position, point_type: str, max_simultaneous_packages_storage:float=float('inf'), package_spawn_interval:Union[int, None]=None, n_packages_per_spawn:int=0, assign_intermediate=True) -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the package point.
            position (Position): Position of the package point in the environment.
            point_type (str): Point type, possible options are defined in environment constants (i.e., 'end-point')
            max_simultaneous_packages_storage (float, optional): Maximum number of packages that can be stored simultaneously. Defaults to float('inf').
            package_spawn_interval (Union[int, None]): Number of steps that should pass before a new package is generated. Defaults to None, which means that no new packages will be generated.
        """        
        self.id = id
        self.pos = position
        self.max_simultaneous_packages_storage = max_simultaneous_packages_storage
        self.point_type = point_type
        self.package_spawn_interval = package_spawn_interval
        self.previous_package_generation_step = -1
        self.n_packages_per_spawn = n_packages_per_spawn
        self.assign_intermediate = assign_intermediate

    def step(self, current_iteration:int, grid, intermediate_package_points, ending_package_points) -> None:
        if self.point_type == PACKAGE_POINT_START and self.package_spawn_interval is not None and current_iteration % self.package_spawn_interval == 0:
            self.generate_packages(grid, intermediate_package_points, ending_package_points, current_iteration)


    def generate_packages(self, grid, intermediate_package_points, ending_package_points, current_iteration:int) -> None:
        for i in range(self.n_packages_per_spawn):
            # Choose random destination
            destination = random.choice([pp for pp in ending_package_points])
            max_iterations_to_deliver = random.randint(1, 20)
            
            # Create package and place it on grid
            package = Package(f'p_it{current_iteration}_{i}', self.pos, destination.pos, max_iterations_to_deliver)
            if self.assign_intermediate:
                # find intermediate point, that is the nearest to the destination
                intermediate_point = min(intermediate_package_points, key=lambda pp: pp.pos.dist_to(destination.pos))
                package.intermediate_point_pos = intermediate_point.pos
                
            grid.place_agent(package, package.pos)
            print(f'Generated package with id {package.id} at position {package.pos.x}, {package.pos.y}')
            Save.save_to_csv_package(package, False)
