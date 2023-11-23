from typing import List
from mesa.space import MultiGrid

from src.environment.obstacle import Obstacle

def convert_grid_to_matrix(grid: MultiGrid) -> List[List]:
    matrix_grid = []
    
    for i in range(grid.height):
        column = []
        for j in range(grid.width):
            if grid[i][j]:
                for entity in grid[i][j]:
                    if isinstance(entity, Obstacle):
                        column.append(0)
                        break
                else:
                    column.append(1)
        matrix_grid.append(column)