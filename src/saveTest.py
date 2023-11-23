from datetime import datetime
from src.agents.chain_agent import ChainAgent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
import random
import os

from src.visualization.save import Save
from src.visualization.merge import Merge
from visualization.save_grid import save_grid


# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f"logs/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir

# Environment elements
starting_position = Position(4, 4)
# end_position = Position(4, 4)

# starting_position_ab = Position(1, 1)

starting_package_point = PackagePoint('pp1', starting_position, PACKAGE_POINT_START, 5, 1, 1)

# end_package_point = PackagePoint('pp2', end_position, PACKAGE_POINT_END)

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

# List of agents
starting_agents_num = 3
agents = [ChainAgent(f'a{i}', starting_position, [], Perception(1), PACKAGE_POINT_END, 'dijkstra') for i in range(starting_agents_num)]
# Environment
#environment = Environment(5, 5, [a], [], [], [])
# environment = Environment(10, 10, agents, [starting_package_point, end_package_point], [starting_obstacle], [starting_package])
environment = Environment(10,10, agents, starting_package_point, 2, 2, [])
save_grid(environment.grid)


m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

# List of agents and package for logging
iteration_data_agent = []
iteration_data_package = []

iterations = 1000
for iteration in range(1, iterations+1):
    environment.step()
    print(f'Iteration {iteration}')
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    
    # for agent in agents:
        # apend list for logging
        # Save.save_to_csv_agent(agent)
    #print(environment.grid)

# Save.save_to_csv_package(iteration_data_package)
# Merge.merge()

