import csv
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import pandas as pd
import os

class Save:
    log_dir = None
    # def save_to_csv(agent_data, filename="agent_data.csv"):
    #     with open(filename, mode="w", newline="") as file:
    #         writer = csv.writer(file)
    #         # Header
    #         writer.writerow(["AgentID", "PackageID", "PackagePoint X", "PackagePoint Y", "Delayed", "OriginPackage X", "OriginPackage Y"])
    #         # data
    #         for agent in agent_data:
    #             writer.writerow([agent.id, agent.package.id, agent.package.destination.x, agent.package.destination.y, agent.package.is_delayed, agent.package.pos.x, agent.package.pos.y])

    def save_agent_data(agent, iteration_num=None, filename="agent_data.csv"):
        filename = f"{Save.log_dir}/{filename}"
        file_exists = os.path.exists(filename)
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Header
                writer.writerow(["iteration", "AgentID", "Strategy", "Pos X", "Pos Y", "algorithm"])
            # data
            writer.writerow([iteration_num, agent.id, type(agent), agent.pos.x, agent.pos.y, agent.algorithm_name])
            

    def save_to_csv_package(package, delivered=True):
        if delivered:
            filename=f"{Save.log_dir}/delivery_data.csv"
        else: 
            filename=f"{Save.log_dir}/package_data.csv"
            
        file_exists = os.path.exists(filename)
        with open(filename, mode="a") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Header
                writer.writerow(["PackageID", "PackagePoint X", "PackagePoint Y", "Delayed", "Delivery Time", "End X", "End Y"])
            # data
            data = [
                package.id, 
                    package.pos.x, 
                    package.pos.y, 
                    package.is_delayed, 
            ]
            if delivered:
                data.append(package.iterations)
            else:
                data.append(None)
                
            if package.intermediate_point_pos:
                data += [package.destination.x, package.destination.y]
            else:
                data += [None, None]
            writer.writerow(data)


    def save_to_csv_messages(message, print):
        filename = f"{Save.log_dir}/messages.csv"
        file_exists = os.path.exists(filename)
        with open(filename, mode="a") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Header
                writer.writerow(["Message", "Type", "Sender ID", "Destination ID", "Value"])
            # data
            data = [
                print,
                message.type,
                    message.sender_id,
                    message.destination_id,
                    message.value,
            ]
            writer.writerow(data)

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
     