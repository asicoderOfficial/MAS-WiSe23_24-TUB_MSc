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

grid_width = 11
grid_height = 11
total_iterations = 5

# Environment elements
intermediate_pp_positions = [
    Position(3,3), Position(7,3),
    Position(3,7), Position(7,7)
]
ending_pp_positions = [
    Position(1,1), Position(5, 1), Position(9, 1),
    Position(1,5), Position(9,5),
    Position(1,9), Position(5,9), Position(9,9)
]    
starting_position = Position(int(grid_width / 2), int(grid_height / 2))
starting_pp = PackagePoint("pp0", starting_position, PACKAGE_POINT_START, package_spawn_interval=2, n_packages_per_spawn=1)

chain_agents = [ 
    CommunicationChainAgent("chain_agent1", starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra"),
    CommunicationChainAgent("chain_agent2", starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra"),
    CommunicationChainAgent("chain_agent3", starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra"),
    CommunicationChainAgent("chain_agent4", starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra") 
]

roaming_agents = []
agents_per_point = 2
i = 0
for point in intermediate_pp_positions:
    for j in range(agents_per_point):
        roaming_agents.append(RoamingAgent(f"roaming_agent{i}", point, [], Perception(1), "dijkstra"))
        i += 1
    
broker = Broker("broker", "naive")
CommunicationLayer.instance(chain_agents + roaming_agents, broker)

environment = Environment(grid_width,grid_height, chain_agents + roaming_agents, starting_pp, intermediate_pp_positions, ending_pp_positions, [])
save_grid(environment.grid)

m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

iterations = 1000
for iteration in range(1, iterations+1):
    environment.step()
    broker.step()
    print(f'Iteration {iteration}')
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    
save_grid(environment.grid)