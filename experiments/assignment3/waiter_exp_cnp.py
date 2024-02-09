import os
from datetime import datetime
from src.agents.strategies.waiter_cnp import WaiterCNP
from src.environment.kitchen import KitchenInitiator
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
from src.utils.automatic_environment import ENV_PP_UNIFORM_SQUARES
from src.visualization.save_grid import save_grid

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f"logs/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir

# Grid dimensions
grid_height = 20
grid_width = 20
# Starting package point
kitchen_initiator = KitchenInitiator("kitchen")
starting_package_point_pos = Position(10, 10)
starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=5, n_packages_per_spawn=4, assign_intermediate=False, kitchen_initiator=kitchen_initiator)
# starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=2, n_packages_per_spawn=1, assign_intermediate=False, kitchen_initiator=kitchen_initiator)
# Ending package points
ending_package_points = [Position(0, 0)]

total_iterations = 1000

# Agents
agents = [WaiterCNP(f'w{i}', starting_package_point_pos, [], Perception(3), 'dijkstra', 'naive_greedy', linear_decreasing_time_tips, starting_package_point_pos) for i in range(15)]


environment = Environment(grid_height, grid_width, agents, starting_package_point, 9, 25, [], pp_distribution_strategy=ENV_PP_UNIFORM_SQUARES, initiator=kitchen_initiator)

m = environment.grid_as_matrix(mode='visualization')

for agent in agents:
    Save.save_agent_data(agent, 0, "init_agent_data.csv")

save_grid(environment.grid, Save.log_dir)

m = environment.grid_as_matrix(mode='visualization')
print('Initial grid:')
for m_i in range(len(m)):
    print(m[m_i])
print()

for iteration in range(1, total_iterations+1):
    print(f'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    for agent in agents:
        print(f"Agent {agent.id} tips: {agent.collected_tips}")
    print()
    
Save.save_agent_final_state(agents, "final_agent_data_cnp.csv")