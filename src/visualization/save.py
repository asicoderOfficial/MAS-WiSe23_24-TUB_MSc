import csv
import matplotlib.pyplot as plt
import pandas as pd

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
