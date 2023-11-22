import csv
import matplotlib.pyplot as plt
import pandas as pd
class Save:

    def save_to_csv_agent(agent_data, filename="agent.csv"):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writerow(["iteration", "agentID", "agentPositionX", "agentPositionY", "packageID"])

            # Write data for each agent
            for row in agent_data:
                writer.writerow([row[0], row[1], row[2], row[3], row[4]])


    def save_to_csv_package(package_data, filename="package.csv"):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writerow(["iteration", "packageID", "packagePosX", "packagePosY", "packageDesX", "packageDesY", "delay"])

            # Write data for each agent
            for row in package_data:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])