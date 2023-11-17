from msilib.schema import Environment
from typing import List
from constants.environment import OBSTACLE_KEY, PACKAGE_KEY, PACKAGE_POINT_KEY


from src.utils.position import Position


class Perception:
    """ What the agent can perceive from the environment."""
    def __init__(self, n_cells_around:int) -> None:
        """ Constructor.

        Args:
            n_cells_around (int): The number of cells around the agent that it can perceive forming a square.
        
        Returns:
            None
        """        
        self.n_cells_around = n_cells_around
        self.visible_packages = []
        self.visible_obstacles = []
        self.visible_package_points = []
    

    def percept(self, agent_position: Position, environment: Environment) -> List[List]:
        """ The agent perceives the environment.

        Args:
            agent_position (Position): The position of the agent in the environment.
            environment (Environment): The current state of the environment.

        Returns:
            List[List]: The subgrid the agent can perceive.
        """        
        visible_submatrix = []
        
        for i in range(max(0, agent_position.x - agent_position.y), min(len(environment.grid), agent_position.x + self.n_cells_around + 1)):
            row = []
            for j in range(max(0, agent_position.y - self.n_cells_around), min(len(environment.grid[0]), agent_position.y + self.n_cells_around + 1)):
                row.append(environment.grid[i][j])
                if environment.grid[i][j][PACKAGE_KEY] != {}:
                    self.visible_packages.append(environment.packages[environment.grid[i][j][PACKAGE_KEY]["id"]])
                if environment.grid[i][j][PACKAGE_POINT_KEY] != {}:
                    self.visible_package_points.append(environment.packages[environment.grid[i][j][PACKAGE_POINT_KEY]["id"]])
                if environment.grid[i][j][OBSTACLE_KEY] != {}:
                    self.visible_obstacles.append(environment.packages[environment.grid[i][j][OBSTACLE_KEY]["id"]])
            visible_submatrix.append(row)
        
        return visible_submatrix
