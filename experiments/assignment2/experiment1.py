from datetime import datetime
import os
import random
from src.agents.strategies.communication_chain_agent import CommunicationChainAgent
from src.agents.perception import Perception
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer
from src.agents.strategies.roaming_agent import RoamingAgent
from src.environment.environment import Environment
from src.environment.obstacle import Obstacle
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.agents.strategies.chain_agent import ChainAgent
from src.utils.position import Position
from src.visualization.save_grid import grid_as_matrix, save_grid

from mesa.space import MultiGrid

from src.visualization.save import Save

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f'logs/{timestamp}'
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir

grid_width = 10
grid_height = 10
total_iterations = 5

chain_agent = CommunicationChainAgent("agent1", Position(0, 0), [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")
roaming_agent = RoamingAgent("agent2", Position(5,5), [], Perception(1), "dijkstra")

broker = Broker("broker", "naive")
CommunicationLayer.instance([chain_agent, roaming_agent], broker)

# Environment elements
intermediate_pp_positions = [
    Position(3,4), Position(6,4),
    Position(3,7), Position(6,7)
]
ending_pp_positions = [
    Position(0,1), Position(5, 1), Position(8, 1),
    Position(0,5), Position(8,5),
    Position(0,9), Position(5,9), Position(8,9)
]    
starting_position = Position(int(grid_width / 2), int(grid_height / 2))
starting_pp = PackagePoint("pp0", starting_position, PACKAGE_POINT_START, package_spawn_interval=2, n_packages_per_spawn=1)

environment = Environment(10,10, [chain_agent, roaming_agent], starting_pp, intermediate_pp_positions, ending_pp_positions, [])
save_grid(environment.grid)

m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

# List of agents and package for logging
iteration_data_agent = []
iteration_data_package = []

iterations = 100
for iteration in range(1, iterations+1):
    environment.step()
    broker.step()
    print(f'Iteration {iteration}')
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()