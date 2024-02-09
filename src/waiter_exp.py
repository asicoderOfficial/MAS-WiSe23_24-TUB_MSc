from datetime import datetime
import os
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
log_dir = f"logs/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir

# Grid dimensions
grid_height = 10
grid_width = 10
# Starting package point
starting_package_point_pos = Position(4, 4)
starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=10, n_packages_per_spawn=2, assign_intermediate=False)
# Ending package points
ending_package_points = [Position(0, 0)]

total_iterations = 100

# Agents
agents = [Waiter('w1', Position(7, 7), [], Perception(3), 'dijkstra', 'refined_greedy', linear_decreasing_time_tips, starting_package_point_pos)]


environment = Environment(grid_height, grid_width, agents, starting_package_point, 0, 10, [], pp_distribution_strategy=ENV_PP_UNIFORM_SQUARES)

m = environment.grid_as_matrix(mode='visualization')

for agent in agents:
    Save.save_agent_data(agent, 0, "init_agent_data.csv")

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