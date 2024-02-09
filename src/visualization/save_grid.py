from typing import List

import pandas as pd
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


def agent_grids():
    # Load the data from the CSV file
    df = pd.read_csv("logs/{timestamp}/naive_fast_agents_data.csv")

    # Filter data for refined_greedy agents
    refined_greedy_agents = df[df['utility_function'] == 'naive_fast']

    # Calculate the total mean tips and total mean tables served for refined_greedy agents
    total_mean_tips = refined_greedy_agents['total_tips'].mean()
    total_mean_tables_served = refined_greedy_agents['total_table_served'].mean()

    print("TOTAL TIPS:")
    print(total_mean_tips)
    print("TOTAL TABLE SERVED:")
    print(total_mean_tables_served)

    # Create bar chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot total mean tips and total mean tables served
    ax1.bar('Naive Fast Agents', total_mean_tips, color='skyblue')
    ax1.set_title('Total Mean Tips Received by Naive Fast Agents')

    ax2.bar('Naive Fast Agents', total_mean_tables_served, color='skyblue')
    ax2.set_title('Total Mean Tables Served by Naive Fast Agents')

    # Add annotation with precise numbers
    ax1.text('Naive Fast Agents', total_mean_tips, f'{total_mean_tips:.2f}', ha='center', va='bottom')
    ax2.text('Naive Fast Agents', total_mean_tables_served, f'{total_mean_tables_served:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def comapison_grid():
    df_naive_fast = pd.read_csv("logs/{timestamp}/naive_fast_agents_data.csv")
    df_naive_greedy = pd.read_csv("logs/{timestamp}/naive_greedy_agents_data.csv")
    df_refined = pd.read_csv("logs/{timestamp}/refine_greedy_agents_data.csv")

    # Calculate mean total tips and total tables served for each algorithm
    mean_total_tips_naive_fast = df_naive_fast['total_tips'].mean()
    mean_total_tables_served_naive_fast = df_naive_fast['total_table_served'].mean()

    mean_total_tips_naive_greedy = df_naive_greedy['total_tips'].mean()
    mean_total_tables_served_naive_greedy = df_naive_greedy['total_table_served'].mean()

    mean_total_tips_refined = df_refined['total_tips'].mean()
    mean_total_tables_served_refined = df_refined['total_table_served'].mean()

    # Create bar chart for mean total tips
    algorithms = ['Naive Fast', 'Naive Greedy', 'Refined']
    mean_total_tips = [mean_total_tips_naive_fast, mean_total_tips_naive_greedy, mean_total_tips_refined]
    tips_colors = ['skyblue', 'orange', 'red']  # Define colors for mean total tips

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot mean total tips
    ax1.bar(algorithms, mean_total_tips, color=tips_colors, label='Mean Total Tips')

    # Add annotation with precise numbers for mean total tips
    for i, tip in enumerate(mean_total_tips):
        ax1.text(i, tip, f'{tip:.2f}', ha='center', va='bottom')

    ax1.set_ylabel('Mean Total Tips')
    ax1.set_title('Comparison of mean total tips')

    # Create bar chart for mean total tables served
    mean_total_tables_served = [mean_total_tables_served_naive_fast, mean_total_tables_served_naive_greedy,
                                mean_total_tables_served_refined]

    fig, ax2 = plt.subplots(figsize=(10, 6))

    # Plot mean total tables served
    ax2.bar(algorithms, mean_total_tables_served, color=tips_colors, label='Mean Total Tables Served')

    # Add annotation with precise numbers for mean total tables served
    for i, table_served in enumerate(mean_total_tables_served):
        ax2.text(i, table_served, f'{table_served:.2f}', ha='center', va='bottom')

    ax2.set_ylabel('Mean Total Tables Served')
    ax2.set_title('Comparison of mean total tables served')

    # Show plots
    plt.tight_layout()
    plt.show()
    