from src.agents.chain_agent import ChainAgent
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
Save.log_dir = 'logs'



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
n_intermediate_package_points = 5
# Ending package points
n_ending_package_points = 3
# Obstacles
obstacles = [Obstacle('o1', Position(0, 1), 1, 1, 1, 2)]
# Agents
total_n_agents = 10
n_shuffles = 1
agents_configurations = distribute_agents(total_n_agents, {'ChainAgent' : [
                                        {'id':'cha1', 'position':None, 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'},
                                        {'id':'cha2', 'position':Position(4, 4), 'package':[], 'perception':Perception(1), 'goal_package_point':PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':'dijkstra'}
                                       ]
                            }, 3)
agents = agents_configurations[0]

environment = Environment(grid_height, grid_width, agents, starting_package_point, n_intermediate_package_points, n_ending_package_points, obstacles)

m = environment.grid_as_matrix(mode='visualization')
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()


iterations = 40
for iteration in range(1, iterations+1):
    print(f'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    # m = environment.grid_as_matrix(mode='pheromone')
    # for i in range(len(m)):
    #     print(m[i])
    # print()
    #print(environment.grid)


"""


    def __init__(self, grid_height: int, grid_width: int, agents_distribution: dict, \
                 starting_package_point: PackagePoint, n_intermediate_package_points: int, n_ending_package_points: int, 
                 obstacles: List[Obstacle], agents_distribution_strategy:str='strategic') -> None:


# Environment elements
starting_position = Position(4, 4)
end_position = Position(6, 4)

# starting_package = Package('p1', starting_position, end_position, 10)

starting_package_point = PackagePoint('pp1', starting_position, PACKAGE_POINT_START, 5, 5)

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

start_agent = ChainAgent('1', starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")
intermediate_agent = ChainAgent('2', intermediate_position, [], Perception(1), PACKAGE_POINT_END, "dijkstra")

# Environment
#environment = Environment(5, 5, [a], [], [], [])
# environment = Environment(5, 5, [a], [starting_package_point, end_package_point], [starting_obstacle], [starting_package])
environment = Environment(10, 10, [a], starting_package_point, 1, 1, [starting_obstacle])


m = environment.grid_as_matrix(mode='visualization')
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

iterations = 40
for iteration in range(1, iterations+1):
    print(f'Iteration {iteration}')
    environment.step()
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    # m = environment.grid_as_matrix(mode='pheromone')
    # for i in range(len(m)):
    #     print(m[i])
    # print()
    #print(environment.grid)




"""