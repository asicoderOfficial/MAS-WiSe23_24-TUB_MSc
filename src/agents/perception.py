from typing import List


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
    

    def percept(self, agent_position: Position, environment_grid: List[List]) -> List[List]:
        """ The agent perceives the environment.

        Args:
            agent_position (Position): The position of the agent in the environment.
            environment_grid (List[List]): The current state of the environment.

        Returns:
            List[List]: The subgrid the agent can perceive.
        """        
        visible_submatrix = []
        
        for i in range(max(0, agent_position.x - agent_position.y), min(len(environment_grid), agent_position.x + self.n_cells_around + 1)):
            row = []
            for j in range(max(0, agent_position.y - self.n_cells_around), min(len(environment_grid[0]), agent_position.y + self.n_cells_around + 1)):
                row.append(environment_grid[i][j])
            visible_submatrix.append(row)
        
        return visible_submatrix
