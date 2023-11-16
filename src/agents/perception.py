from typing import Union, List


from src.utils.position import Position


class Perception:
    def __init__(self, n_cells_around:int) -> None:
        self.n_cells_around = n_cells_around
    

    def percept(self, agent_position: Position, environment_grid: List[List]) -> List[List]:
        """ Returns the list of packages in the agent's perception."""
        visible_submatrix = []
        
        for i in range(max(0, agent_position.x - agent_position.y), min(len(environment_grid), agent_position.x + self.n_cells_around + 1)):
            row = []
            for j in range(max(0, agent_position.y - self.n_cells_around), min(len(environment_grid)[0], agent_position.y + self.n_cells_around + 1)):
                row.append(environment_grid[i][j])
            visible_submatrix.append(row)
        
        return visible_submatrix
