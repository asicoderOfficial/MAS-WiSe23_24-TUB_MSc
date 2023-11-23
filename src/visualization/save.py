import csv
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import pandas as pd

from mesa.space import MultiGrid

from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint

class Save:
    def save_to_csv(agent_data, filename="delivery_data.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Header
            writer.writerow(["AgentID", "PackageID", "PackagePoint X", "PackagePoint Y", "Delayed", "OriginPackage X", "OriginPackage Y"])
            # data
            for agent in agent_data:
                writer.writerow([agent.id, agent.package.id, agent.package.destination.x, agent.package.destination.y, agent.package.is_delayed, agent.package.pos.x, agent.package.pos.y])

    def visualize_data():
        df = pd.read_csv("delivery_data.csv")
        x = df['PackagePoint X']
        y = df['PackagePoint Y']
        colors = df['Delayed'].map({True: 'red', False: 'green'})

        # Create a scatter plot
        plt.scatter(x, y, c=colors, marker='o', alpha=0.5)

        # Add labels and title
        plt.xlabel('PackagePoint X')
        plt.ylabel('PackagePoint Y')
        plt.title('Scatter Plot of Package Points')

        # Show the plot
        plt.show()

    def visualize_grid(grid: MultiGrid):
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