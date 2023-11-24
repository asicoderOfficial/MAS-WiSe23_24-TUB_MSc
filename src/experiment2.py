from datetime import datetime
from math import floor
import os
from src.agents.chain_agent import ChainAgent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
import random
from src.visualization.save import Save
from visualization.save_grid import save_grid

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f"experiments/with_n_without/without/{timestamp}"
os.makedirs(log_dir, exist_ok=True)
Save.log_dir = log_dir



def generate_random_strategy_allocation(total_n_agents, n_strategies_to_test):
    # Initialize the array with zeros
    strategy_allocation = [0] * (2 * n_strategies_to_test)

    # Generate random integers for each strategy
    for i in range(n_strategies_to_test * 2 - 1):
        strategy_allocation[i] = random.randint(1, total_n_agents - sum(strategy_allocation) - (n_strategies_to_test * 2 - 1 - i))

    # The last element is the remaining balance to ensure the sum is total_n_agents
    strategy_allocation[-1] = total_n_agents - sum(strategy_allocation)

    return strategy_allocation


def distribute_agents(total_n_agents: int, strategies_to_test: list, n_configurations_to_test: int):
    n_strategies_to_test = len(strategies_to_test)
    if total_n_agents < n_strategies_to_test * 2:
        raise Exception(f"Too low number of agents ({total_n_agents}) for {n_strategies_to_test} strategies. \
                        The minimum number of total agents to place would be {n_strategies_to_test * 2}")

    agents_distribution = []

    for n in range(n_configurations_to_test):
        strategies_allocations = generate_random_strategy_allocation(total_n_agents, n_strategies_to_test)
        cnt = 0
        ith_configuration = []
        for agent_strategy_id, parameters in strategies_to_test.items():
            for n_agents in range(floor(0 * total_n_agents)):
                if agent_strategy_id == 'ChainAgent':
                    agent = ChainAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}-{parameters[0]["goal_package_point"]}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'GreedyAgent':
                    agent = GreedyAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}'
                    ith_configuration.append(agent)
            for n_agents in range(floor(1 * total_n_agents)):
                if agent_strategy_id == 'ChainAgent':
                    agent = ChainAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}-{parameters[1]["goal_package_point"]}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'GreedyAgent':
                    agent = GreedyAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}'
                    ith_configuration.append(agent)
            cnt += 1
        agents_distribution.append(ith_configuration)
    
    return agents_distribution


# Grid dimensions
grid_height = 100
grid_width = 100
# Starting package point
starting_package_point_pos = Position(floor(grid_width / 2 - 1), floor(grid_height / 2 - 1))
starting_package_point = PackagePoint('spp', starting_package_point_pos, PACKAGE_POINT_START, package_spawn_interval=5, n_packages_per_spawn=5)
# Intermediate package points
n_intermediate_package_points = 7
n_ending_package_points = 15
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
total_n_agents = 20
n_shuffles = 5
algorithm = 'dijkstra'
agents_configurations = distribute_agents(total_n_agents, 
                                        {'ChainAgent' : 
                                         [
                                            {'id':'cha1', 'position':None, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_START, 'algorithm_name':'dijkstra'},
                                            {'id':'cha2', 'position':starting_package_point_pos, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_END, 'algorithm_name':'dijkstra'}, 
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
agents_config = agents_configurations[0]

# for i, agents_config in enumerate(agents_configurations):
    # Save.log_dir = log_dir + f"/{i}/"
    # os.makedirs(Save.log_dir, exist_ok=True)
    
intermediate_package_points = [
    PackagePoint('pp2', intermediate_position, PACKAGE_POINT_INTERMEDIATE, 5, 0)
    ]

    
environment = Environment(grid_height, grid_width, agents_config, starting_package_point, n_intermediate_package_points, n_ending_package_points, obstacles)

save_grid(environment.grid, Save.log_dir)

m = environment.grid_as_matrix(mode='visualization')
for m_i in range(len(m)):
    print(m[m_i])

for agent in agents_config:
    Save.save_agent_data(agent, 0, "init_agent_data.csv")

for iteration in range(1, total_iterations+1):
    print(f'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    print()
    # m = environment.grid_as_matrix(mode='pheromone')
    # for i in range(len(m)):
    #     print(m[i])
    # print()
    #print(environment.grid)
