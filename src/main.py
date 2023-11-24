from datetime import datetime
import os
from src.agents.strategies.chain_agent import ChainAgent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
from src.agents.strategies.greedy_agent import GreedyAgent
import random
from src.visualization.save import Save

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

timestamp = datetime.now()
log_dir = f"logs/{timestamp}"
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
            for n_agents in range(strategies_allocations[cnt * 2]):
                if agent_strategy_id == 'ChainAgent':
                    agent = ChainAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'GreedyAgent':
                    agent = GreedyAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}'
                    ith_configuration.append(agent)
            for n_agents in range(strategies_allocations[cnt * 2 + 1]):
                if agent_strategy_id == 'ChainAgent':
                    agent = ChainAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'GreedyAgent':
                    agent = GreedyAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}'
                    ith_configuration.append(agent)
            cnt += 1
        agents_distribution.append(ith_configuration)
    
    return agents_distribution


# Grid dimensions
grid_height = 10
grid_width = 10
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
                                        {'GreedyAgent' :
                                         [
                                            {'id':'gre1', 'position':None, 'packages':[], 'perception':Perception(1), 'algorithm_name':algorithm},
                                            {'id':'gre2', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(1), 'algorithm_name':algorithm}
                                         ],
                                         'ChainAgent' : 
                                         [
                                            {'id':'cha1', 'position':None, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'},
                                            {'id':'cha2', 'position':starting_package_point_pos, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'}, 
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
