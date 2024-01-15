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

from src.visualization.save import Save
from src.utils.automatic_environment import ENV_PP_UNIFORM_SQUARES, distribute_agents

# Experiment that shows performance of different communication methods and different agent alocations
# Always using communication


# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

# Agents parameters
agent_distributions = [
    {
        "comm_chain_agents": 3,  
        "roaming_agents": 5,
    },
    {
        "comm_chain_agents": 8,  
        "roaming_agents": 16,
    }
]
movement_algorithm = 'dijkstra'
n_shuffles = 1
perception_range = 3
broker_optimality_criterias = ['naive', 'closer_to_package', 'loneliest']

grid_side = 50
total_iterations = 1000
n_obstacles_perc = 50

end_pp_num = 16
intermediate_pp_num = 4
packages_spawn_interval = 2
n_packages_per_spawn = 1

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
base_log_dir = "logs"


communication_mechanism = ["broker", "recruiter"]

for agent_distribution in agent_distributions:
    for broker_optimality_criteria in broker_optimality_criterias:
        for comm_mech in communication_mechanism:
            n_chain_agents = agent_distribution["comm_chain_agents"]
            n_roaming_agents = agent_distribution["roaming_agents"]
            
            log_dir = f'{base_log_dir}/{timestamp}_g{grid_side}_ca0_cca{n_chain_agents}_ra{n_roaming_agents}_ob{n_obstacles_perc}_{comm_mech}_{broker_optimality_criteria}'
            os.makedirs(log_dir, exist_ok=True)
            Save.log_dir = log_dir
            
            starting_position = Position(grid_side // 2, grid_side // 2)
            starting_pp = PackagePoint("spp", starting_position, PACKAGE_POINT_START, package_spawn_interval=packages_spawn_interval, n_packages_per_spawn=n_packages_per_spawn)

            comm_chain_agents = [
                CommunicationChainAgent(f"comcha_{i}", starting_position, [], Perception(perception_range), PACKAGE_POINT_INTERMEDIATE, movement_algorithm, communication_mechanism) 
                for i in range(n_chain_agents)
            ]
            
            roaming_agents = [
                RoamingAgent(f"roaming_{i}", None, [], Perception(perception_range), movement_algorithm)
                for i in range(n_roaming_agents)
            ]
            
            agents = comm_chain_agents + roaming_agents
            
            obstacle_number = int((grid_side * grid_side) * (n_obstacles_perc/100))
            obstacle_heights = [random.randint(1,3) for i in range(obstacle_number)]
            obstacle_widths = list(map(lambda x: x[1] if obstacle_heights[x[0]] == 1 else 1, enumerate([random.randint(1,3) for i in range(obstacle_number)])))
            obstacles = [
                Obstacle(f'o{i}', Position(random.randint(0, grid_side-1), random.randint(0,grid_side-1)), width=obstacle_widths[i], height=obstacle_heights[i], starting_iteration=random.randint(1,total_iterations-1), duration=random.randint(1,5))
                for i in range(obstacle_number)
            ]
            environment = Environment(grid_side, grid_side, agents, starting_pp, intermediate_pp_num, end_pp_num, [], broker_optimality_criteria=broker_optimality_criteria, pp_distribution_strategy=ENV_PP_UNIFORM_SQUARES)
            save_grid(environment.grid, Save.log_dir)

            m = environment.grid_as_matrix()
            print('Initial state')
            for i in range(len(m)):
                print(m[i])
            print()

            for n_iteration in range(total_iterations):
                print(f'Iteration {n_iteration}') 
                environment.step()
                m = environment.grid_as_matrix(mode='visualization')
                for i in range(len(m)):
                    print(m[i])
                print()
                print()
                
                