from src.environment.package_counter import PackageCounter
from src.agents.chain_agent import ChainAgent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
import random

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)
grid_size = 10
# Environment elements
starting_pp_pos = Position(4, 4)
intermediate_pps_pos = [Position(2, 2), Position(3,4), Position(5, 5)]
end_pps_pos = [Position(0, 0), Position(3, 0), Position(0, 3), Position(9, 7)]

# starting_package = Package('p1', starting_position, end_position, 10)

starting_agents_num = 4
starting_package_point = PackagePoint('pp1', starting_pp_pos, PACKAGE_POINT_START, 5, 1)
start_agents = [ChainAgent(f's-{i}', starting_pp_pos, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra") for i in range(starting_agents_num)]

intermediate_pps = [PackagePoint(f'pp{i}', pos, PACKAGE_POINT_INTERMEDIATE, 5, 5) for i, pos in enumerate(intermediate_pps_pos)]
intermediate_agents = [ChainAgent(f'i-{i}', pp.pos, [], Perception(1), PACKAGE_POINT_END, "dijkstra") for i, pp in enumerate(intermediate_pps)]

end_pps = [PackagePoint(f'pp-e{i}', pos, PACKAGE_POINT_END) for i, pos in enumerate(end_pps_pos)]

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

package_counter = PackageCounter()

# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(grid_size, grid_size, start_agents + intermediate_agents, [starting_package_point] + intermediate_pps + end_pps, [starting_obstacle], [], True)

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
print(PackageCounter.delivered_packages, PackageCounter.generated_packages)