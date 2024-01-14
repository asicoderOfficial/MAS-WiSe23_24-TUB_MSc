from datetime import datetime
import os
from src.agents.strategies.communication_chain_agent import CommunicationChainAgent
from src.agents.strategies.roaming_agent import RoamingAgent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
import random
from src.visualization.save import Save
from src.utils.automatic_environment import distribute_agents

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f"logs/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir





# Grid dimensions
grid_height = 10
grid_width = 10

chain_agent = CommunicationChainAgent("agent1", Position(0, 0), [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")
roaming_agent = RoamingAgent("agent2", Position(5,5), [], Perception(1), "dijkstra")


# Starting package point
starting_package_point_pos = Position(4, 4)
starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=5, n_packages_per_spawn=5)
# Intermediate package points
n_intermediate_package_points = 3
# Ending package points
n_ending_package_points = 5
# Obstacles
total_iterations = 1000

obstacle_number = 10
obstacle_heights = [random.randint(1,3) for i in range(obstacle_number)]
obstacle_widths = list(map(lambda x: x[1] if obstacle_heights[x[0]] == 1 else 1, enumerate([random.randint(1,3) for i in range(obstacle_number)])))
obstacles = [
    Obstacle('o1', Position(random.randint(0,grid_width-1), random.randint(0,grid_height-1)), width=obstacle_widths[i], height=obstacle_heights[i], starting_iteration=random.randint(1,total_iterations-1), duration=random.randint(1,5))
    for i in range(obstacle_number)
]

# Agents
total_n_agents = 4
n_shuffles = 1
algorithm = 'dijkstra'
agents_configurations = distribute_agents(total_n_agents, 
                                        {'CommunicationChainAgent' :
                                         [
                                            {'id':'gre1', 'position':None, 'packages':[], 'perception':Perception(1), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':algorithm},
                                            {'id':'gre2', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(1), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':algorithm}
                                         ],
                                         'RoamingAgent' : 
                                         [
                                            {'id':'cha1', 'position':None, 'packages':[], 'perception':Perception(1), 'algorithm_name':'dijkstra'},
                                            {'id':'cha2', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(1), 'algorithm_name':'dijkstra'}, 
                                        ] 
                                        },
                                        n_shuffles)
"""
agents_configurations = distribute_agents(total_n_agents, 
                                        {'ChainAgent' : 
                                         [
                                            {'id':'cha1', 'position':None, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'},
                                            {'id':'cha2', 'position':Position(4, 4), 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'}
                                        ] },
                                        n_shuffles)
"""
agents = agents_configurations[0]


environment = Environment(grid_height, grid_width, agents, starting_package_point, n_intermediate_package_points, n_ending_package_points, obstacles)

m = environment.grid_as_matrix(mode='visualization')
for m_i in range(len(m)):
    print(m[m_i])

for agent in agents:
    Save.save_agent_data(agent, 0, "init_agent_data.csv")

for iteration in range(1, total_iterations+1):
    print(f'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    print()
