from typing import List

from mesa import Model
from mesa.space import MultiGrid

from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle


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
        
        self.current_iteration = 0

        # Create self.grid with grid_height rows and grid_width columns
        self.grid = MultiGrid(width=self.grid_width, height=self.grid_height, torus=False)
        self.init_grid(agents, package_points, packages, obstacles)


    def step(self) -> None:
        """ Main method of the environment. It is called every iteration.

        Args:
            current_iteration (int): The current iteration of the experiment.
        
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

        # Dynamic entities that do not move, but can disappear: Obstacles
        for obstacle in self.obstacles:
            if obstacle.iterations_left == -1 and obstacle.pos is not None:
                # The object has to disappear from the grid. It has already stayed in the environment for the required iterations.
                self.grid.remove_agent(obstacle)
            elif self.current_iteration == obstacle.starting_iteration:
                # The object has to appear in the grid now, it is the starting iteration.
                obstacle.determine_position(self.grid)
                self.grid.place_agent(obstacle, obstacle.pos)
                
        self.current_iteration += 1
            

    def init_grid(self, agents: List[Agent], package_points: List[PackagePoint], packages: List[Package], obstacles: List[Obstacle]) -> None:
        """ Initializes the grid with the static entities (Package Points, Obstacles and Packages).
        Called only once, at the beginning of the experiment.
        """        
        for entity in agents + package_points + packages:
            self.grid.place_agent(entity, entity.pos)

        for obstacle in obstacles:
            if obstacle.starting_iteration == 1:
                obstacle.determine_position(self.grid)
                self.grid.place_agent(obstacle, obstacle.pos)


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
                        for entity in self.grid._grid[i][j]:
                            if isinstance(entity, Obstacle):
                                column.append(0)
                            else:
                                column.append(1)
                    else:
                        column.append(1)
                matrix_grid.append(column)
        if mode == 'visualization':
            # Be aware this can add more columns, if more than 1 entity is in the same cell.
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    if self.grid._grid[i][j]:
                        for entity in self.grid._grid[i][j]:
                            if isinstance(entity, PackagePoint):
                                column.append('x')
                            if isinstance(entity, Obstacle):
                                column.append('o')
                            if isinstance(entity, Package):
                                column.append('p')
                            if isinstance(entity, Agent):
                                column.append('a')
                    else:
                        column.append(' ')
                matrix_grid.append(column)

        return matrix_grid
        