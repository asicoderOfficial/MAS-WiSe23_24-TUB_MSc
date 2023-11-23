from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint


def save_grid(grid):
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
    plt.savefig("grid.png")   