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

broker = Broker("broker")
CommunicationLayer.instance([chain_agent, roaming_agent], broker)

# Environment elements
starting_position = Position(4, 4)
starting_pp = PackagePoint("pp0", Position(0,0), PACKAGE_POINT_START, package_spawn_interval=2, n_packages_per_spawn=1)
starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)


environment = Environment(10,10, [chain_agent, roaming_agent], starting_pp, [Position(x=2, y=3)], [Position(x=7, y=7)], [starting_obstacle])
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

#intermediate_pp = PackagePoint("pp1", Position(4,4), PACKAGE_POINT_INTERMEDIATE)
#end_pp = PackagePoint("pp1", Position(9,9), PACKAGE_POINT_END)

#grid = MultiGrid(width=grid_width, height=grid_height, torus=False)
#grid.place_agent(chain_agent, chain_agent.pos)
#grid.place_agent(roaming_agent, roaming_agent.pos)
#grid.place_agent(starting_pp, starting_pp.pos)
#grid.place_agent(intermediate_pp, intermediate_pp.pos)
#grid.place_agent(end_pp, end_pp.pos)


#for iteration in range(1, total_iterations+1):
#    print(f'Iteration {iteration}')
#    starting_pp.step(iteration, grid, [intermediate_pp], [end_pp])
#    chain_agent.step(grid)
#    for package in chain_agent.packages:
#        package.step(chain_agent.pos, grid)
#    roaming_agent.step(grid)
#    for package in roaming_agent.packages:
#        package.step(roaming_agent.pos, grid)
#    broker.step()
#    m = grid_as_matrix(grid, mode='visualization')
#    for i in range(len(m)):
#        print(m[i])
#    print()
#    print()

