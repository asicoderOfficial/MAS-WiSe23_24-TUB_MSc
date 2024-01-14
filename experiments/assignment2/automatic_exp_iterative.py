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
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer



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
n_intermediate_package_points = 8
# Ending package points
n_ending_package_points = 10

# Experiment parameters
n_iterations = [100, 1_000, 10_000]
n_shuffles = 1
perception_cells = 3

# Agents parameters
n_chain_agents = [2, 8, 32]
n_roaming_agents = [2, 8, 32]
movement_algorithm = 'dijkstra'

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


broker = Broker("broker", "naive")
# TODO: Add recruiter

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
                    # Starting package point
                    starting_package_point_pos = Position(grid_height//2, grid_width//2)
                    starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=package_spawn_interval, n_packages_per_spawn=n_packages_per_spawn)
                    # Agents
                    total_n_agents = n_chain_agent + n_roaming_agent

                    agents_configurations = distribute_agents(total_n_agents,
                                                                {'CommunicationChainAgent' :
                                                                [
                                                                    {'id':f'comcha_{i}', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(perception_cells), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':movement_algorithm}
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

                    # Obstacles
                    obstacle_number = int((grid_height * grid_width) * (n_obstacles_perc/100))
                    obstacle_heights = [random.randint(1,3) for i in range(obstacle_number)]
                    obstacle_widths = list(map(lambda x: x[1] if obstacle_heights[x[0]] == 1 else 1, enumerate([random.randint(1,3) for i in range(obstacle_number)])))
                    obstacles = [
                        Obstacle('o1', Position(random.randint(0,grid_width-1), random.randint(0,grid_height-1)), width=obstacle_widths[i], height=obstacle_heights[i], starting_iteration=random.randint(1,n_iterations-1), duration=random.randint(1,5))
                        for i in range(obstacle_number)
                    ]
                    for agents in agents_configurations:
                        CommunicationLayer.instance(agents, broker)
                        environment = Environment(grid_height, grid_width, agents, starting_package_point, intermediate_pp_positions, ending_pp_positions, obstacles)
                        # Start experiment
                        m = environment.grid_as_matrix(mode='visualization')
                        for m_i in range(len(m)):
                            print(m[m_i])

                        for agent in agents:
                            Save.save_agent_data(agent, 0, "init_agent_data.csv")

                        for n_iteration in range(max_iterations):
                            print(f'Iteration {n_iteration}') 
                            environment.step()
                            broker.step()
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
                    
