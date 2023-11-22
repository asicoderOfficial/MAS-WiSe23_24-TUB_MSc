import random
from typing import List

from mesa import Model
from mesa.space import MultiGrid

from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle, ObstacleCell


class Environment(Model):
    """ The environment where the agents interact."""
    def __init__(self, grid_height: int, grid_width: int, agents: List[Agent], \
                 package_points: List[PackagePoint], obstacles: List[Obstacle], packages: List[Package]) -> None:
        """ Constructor.

        Args:
            grid_height (int): Height of the grid (number of rows)
            grid_width (int): Width of the grid (number of columns)
            agents (List[Agent]): Agents in the environment.
            package_points (List[PackagePoint]): Package points in the environment.
            obstacles (List[Obstacle]): Obstacles in the environment.
            packages (List[Package]): Packages in the environment.
        
        Returns:
            None
        """        
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = agents
        self.package_points = package_points
        self.obstacles = obstacles
        self.packages = packages
        
        self.current_iteration = 1

        # Create self.grid with grid_height rows and grid_width columns
        self.grid = MultiGrid(width=self.grid_width, height=self.grid_height, torus=False)
        self.init_grid()


    def step(self) -> None:
        """ Main method of the environment. It is called every iteration.
        
        Returns:
            None 
        """        
        for agent in self.agents:
            agent.step(self.grid)
            if agent.package:
                # The agent package_id != '', so the agent is carrying the package. So wherever the agent goes, the package goes too.
                agent.package.step(agent.pos, self.grid)
        
        for obstacle in self.obstacles:
            obstacle.step(self.current_iteration, self.grid)
            
        for package_point in self.package_points:
            if package_point.point_type == PACKAGE_POINT_START and package_point.steps_per_package != None and self.current_iteration - package_point.previous_package_generation_step > package_point.steps_per_package:
                self.generate_package(package_point)

        self.current_iteration += 1
            

    def init_grid(self) -> None:
        """ Initializes the grid with the static entities (Package Points, Obstacles and Packages).
        Called only once, at the beginning of the experiment.
        """        
        # Place static objects for the first time: package points
        
        # Place dynamic objects for the first time
        for entity in self.agents + self.package_points + self.packages:
            self.grid.place_agent(entity, entity.pos)

        for obstacle in self.obstacles:
            obstacle.step(self.current_iteration, self.grid)
        
        self.current_iteration += 1
        
                

    def generate_package(self, package_point: PackagePoint) -> None:
        # Choose random destination
        destination = random.choice([pp for pp in self.package_points if pp.point_type == PACKAGE_POINT_END and pp.id != package_point.id])
        
        # Create package and place it on grid
        package = Package(f'p{len(self.packages)}', package_point.pos, destination.pos, 10)
        self.grid.place_agent(package, package_point.pos)
        self.packages.append(package)
        print("Generated package")
        # Update package point
        package_point.previous_package_generation_step = self.current_iteration
        

    def grid_as_matrix(self, mode:str='dijkstra') -> List[List]:
        """ Convert the grid to a matrix of dimensions self.grid_height x self.grid_width.

        Args:
            mode (str, optional): How to create the matrix, depending on the purpose. Defaults to 'dijkstra'.

        Returns:
            List[List]: The grid as a matrix.
        """        
        matrix_grid = []
        if mode == 'dijkstra':
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    if self.grid._grid[i][j]:
                        # check if there is some instance of ObstacleCell in the cell
                        if any(isinstance(entity, ObstacleCell) for entity in self.grid._grid[i][j]):
                            column.append(0)
                        else:
                            column.append(1)
                    else:
                        column.append(1)
                matrix_grid.append(column)
        if mode == 'visualization':
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    cell = ''
                    if self.grid[i][j]:
                        for entity in self.grid[i][j]:
                            if isinstance(entity, PackagePoint):
                                cell += 'x'
                            if isinstance(entity, Package):
                                cell += 'p'
                            if isinstance(entity, Agent):
                                cell += 'a'
                            else:
                                cell += 'o'
                        column.append(cell)
                    else:
                        column.append(' ')
                matrix_grid.append(column)

        return matrix_grid
        