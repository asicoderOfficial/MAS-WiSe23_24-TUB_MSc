from typing import List

from mesa import Model


from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.utils.position import Position
from src.constants.environment import EMPTY_CELL


class Environment(Model):
    def __init__(self, grid_height: int, grid_width: int, agents: List[Agent], \
                 package_points: List[PackagePoint], obstacles: List[Obstacle], packages: List[Package]) -> None:
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = agents
        self.package_points = package_points
        self.obstacles = obstacles
        self.packages = packages

        # Create self.grid with grid_height rows and grid_width columns
        grid = [[EMPTY_CELL for _ in range(self.grid_width)] for _ in range(self.grid_height)]
    

    def update_grid(self) -> None:
        """ Updates the grid of the environment."""
        pass



class Perception:
    def __init__(self, n_cells_around:int) -> None:
        self.n_cells_around = n_cells_around
    

    def percept(self, agent_position: Position, environment: Environment) -> Environment:
        """ Returns the list of packages in the agent's perception."""
        pass
