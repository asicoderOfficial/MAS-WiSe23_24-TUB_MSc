from typing import List
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
from src.agents.strategies.roaming_agent import RoamingAgent
from src.agents.strategies.chain_agent import ChainAgent
from src.agents.strategies.greedy_agent import GreedyAgent
from src.environment.obstacle import ObstacleCell
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint


def save_grid(grid, log_dir):
    start_pp_code = 0
    intermediate_pp_code = 1
    end_pp_code = 2
    empty_cell = 3
    
    pps_matrix = []
    for i in range(grid.height):
        row = []
        for j in range(grid.width):
            cell_code = empty_cell
            if grid[i][j]:
                for entity in grid[i][j]:
                    if isinstance(entity, PackagePoint):
                        if entity.point_type == PACKAGE_POINT_START:
                            cell_code = start_pp_code
                        elif entity.point_type == PACKAGE_POINT_INTERMEDIATE:
                            cell_code = intermediate_pp_code
                        elif entity.point_type == PACKAGE_POINT_END:
                            cell_code = end_pp_code
            row.append(cell_code)
        pps_matrix.append(row)

    x = [pp[0] for pp in pps_matrix]
    y = [pp[1] for pp in pps_matrix]
    # Create a scatter plot
    # plt.scatter(x, y, c=colors, marker='o', alpha=0.5)
    cmap = ListedColormap(['red','yellow', 'blue', 'white'])
    plt.pcolormesh(pps_matrix, cmap=cmap)
    # Add labels and title
    plt.xlabel('GRID X')
    plt.ylabel('GRID Y')
    plt.title('Scatter Plot of Package Points')

    # Show the plot
    figure_path = f"{log_dir}/grid.png"
    plt.savefig(figure_path)   
    plt.close()
    
def grid_as_matrix(grid, mode:str='dijkstra') -> List[List]:
    """ Convert the grid to a matrix of dimensions self.grid_height x self.grid_width.

    Args:
        mode (str, optional): How to create the matrix, depending on the purpose. Defaults to 'dijkstra'.

    Returns:
        List[List]: The grid as a matrix.
    """        
    matrix_grid = []
    if mode == 'dijkstra':
        for i in range(grid.height):
            column = []
            for j in range(grid.width):
                if grid._grid[i][j]:
                    # check if there is some instance of ObstacleCell in the cell
                    if any(isinstance(entity, ObstacleCell) for entity in grid._grid[i][j]):
                        column.append(0)
                    else:
                        column.append(1)
                else:
                    column.append(1)
            matrix_grid.append(column)
    elif mode == 'visualization':
        for i in range(grid.height):
            column = []
            for j in range(grid.width):
                cell = ''
                if grid[i][j]:
                    for entity in grid[i][j]:
                        # Package points
                        if isinstance(entity, PackagePoint):
                            if entity.point_type == PACKAGE_POINT_START:
                                cell += 's'
                            elif entity.point_type == PACKAGE_POINT_INTERMEDIATE:
                                cell += 'i'
                            elif entity.point_type == PACKAGE_POINT_END:
                                cell += 'e'
                        # Packages
                        if isinstance(entity, Package):
                            cell += 'p'
                        # Agents
                        if isinstance(entity, ChainAgent):
                            cell += 'c'
                        if isinstance(entity, RoamingAgent):
                            cell += 'r'
                        if isinstance(entity, GreedyAgent):
                            cell += 'g'
                        # Obstacles
                        if isinstance(entity, ObstacleCell):
                            cell += 'o'
                    column.append(cell)
                else:
                    column.append(' ')
            matrix_grid.append(column)

    return matrix_grid
    