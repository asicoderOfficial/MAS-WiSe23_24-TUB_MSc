from datetime import datetime
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.agents.tips_functions import constant_tips, linear_decreasing_time_tips
from src.agents.strategies.chain_agent import ChainAgent
from src.agents.strategies.waiter import Waiter
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
from src.agents.strategies.greedy_agent import GreedyAgent
import random
from src.visualization.save import Save
from utils.automatic_environment import ENV_PP_UNIFORM_SQUARES

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = r"logs/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir

# Grid dimensions
grid_height = 20
grid_width = 20
# Starting package point
starting_package_point_pos = Position(10, 10)
starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=5, n_packages_per_spawn=4, assign_intermediate=False)
# Ending package points
ending_package_points = [Position(0, 0)]

total_iterations = 1000

# Agents
# Create 15 agents
agents = [Waiter('naive_fast1', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast2', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast3', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast4', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast5', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast6', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast7', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast8', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast9', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast10', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast11', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast12', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast13', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast14', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos),
          Waiter('naive_fast15', Position(10, 10), [], Perception(3), 'dijkstra', 'naive_fast', linear_decreasing_time_tips, starting_package_point_pos)]


environment = Environment(grid_height, grid_width, agents, starting_package_point, 9, 25, [], pp_distribution_strategy=ENV_PP_UNIFORM_SQUARES)

m = environment.grid_as_matrix(mode='visualization')

m = environment.grid_as_matrix(mode='visualization')
print('Initial grid:')
for m_i in range(len(m)):
    print(m[m_i])
print()

for iteration in range(1, total_iterations+1):
    #printf'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    for agent in agents:
        print(f"Agent {agent.id} tips: {agent.collected_tips}")
    print()

Save.save_agent_final_state(agents, "naive_fast_agents_data.csv")
