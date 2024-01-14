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

base_log_dir = f"logs/"

# Environment parameters
# Grid dimensions
grid_sides = [10, 50, 100, 250, 500]
# Obstacles
n_obstacles_perc = [0, 10, 25]
# Starting package point
package_spawn_interval = 5
n_packages_per_spawn = 5
# Intermediate package points
n_intermediate_package_points = 3
# Ending package points
n_ending_package_points = 5

# Experiment parameters
n_iterations = [100, 1_000, 10_000]
n_shuffles = 1
perception_cells = 3

# Agents parameters
n_chain_agents = [2, 8, 32]
n_roaming_agents = [2, 8, 32]
movement_algorithm = 'dijkstra'

for grid_side in grid_sides:
    for n_chain_agent in n_chain_agents:
        for n_roaming_agent in n_roaming_agents:
            for n_obstacles_perc in n_obstacles_perc:
                for max_iterations in n_iterations:
                    # Logging
                    log_dir = f'{base_log_dir}_g{grid_side}_ca{n_chain_agent}_ra{n_roaming_agent}_ob{n_obstacles_perc}_{datetime.now()}'
                    os.makedirs(log_dir, exist_ok=True)
                    Save.log_dir = log_dir
                    # Environment dimensions
                    grid_height = grid_side
                    grid_width = grid_side
                    # Agents
                    total_n_agents = n_chain_agent + n_roaming_agent

                    agents_configurations = distribute_agents(total_n_agents,
                                                                {'CommunicationChainAgent' :
                                                                [
                                                                    {'id':f'comcha_{i}', 'position':None, 'packages':[], 'perception':Perception(perception_cells), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':movement_algorithm}
                                                                    for i in range(n_chain_agent)
                                                                ],
                                                                'RoamingAgent' :
                                                                [
                                                                    {'id':f'roaming_{i}', 'position':None, 'packages':[], 'perception':Perception(perception_cells), 'algorithm_name':movement_algorithm}
                                                                    for i in range(n_roaming_agent)
                                                                ]
                                                                },
                                                                n_shuffles
                                                            )

                    # Starting package point
                    starting_package_point_pos = Position(grid_height//2, grid_width//2)
                    starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=package_spawn_interval, n_packages_per_spawn=n_packages_per_spawn)
                    # Obstacles
                    obstacle_number = int((grid_height * grid_width) * (n_obstacles_perc/100))
                    obstacle_heights = [random.randint(1,3) for i in range(obstacle_number)]
                    obstacle_widths = list(map(lambda x: x[1] if obstacle_heights[x[0]] == 1 else 1, enumerate([random.randint(1,3) for i in range(obstacle_number)])))
                    obstacles = [
                        Obstacle('o1', Position(random.randint(0,grid_width-1), random.randint(0,grid_height-1)), width=obstacle_widths[i], height=obstacle_heights[i], starting_iteration=random.randint(1,n_iterations-1), duration=random.randint(1,5))
                        for i in range(obstacle_number)
                    ]
                    for agents in agents_configurations:
                        environment = Environment(grid_height, grid_width, agents, starting_package_point, n_intermediate_package_points, n_ending_package_points, obstacles)
                        # Start experiment
                        m = environment.grid_as_matrix(mode='visualization')
                        for m_i in range(len(m)):
                            print(m[m_i])

                        for agent in agents:
                            Save.save_agent_data(agent, 0, "init_agent_data.csv")

                        for n_iteration in range(max_iterations):
                            print(f'Iteration {n_iteration}') 
                            environment.step()
                            m = environment.grid_as_matrix(mode='visualization')
                            for i in range(len(m)):
                                print(m[i])
                            print()
                            print()
                        break
                    break
                break
            break
        break
    break
                    
