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

# Environment elements
starting_position = Position(0, 0)
intermediate_position = Position(2, 2)
end_position = Position(4, 4)

# starting_package = Package('p1', starting_position, end_position, 10)

starting_package_point = PackagePoint('pp1', starting_position, PACKAGE_POINT_START, 5, 5)

intermediate_package_point = PackagePoint('pp2', intermediate_position, PACKAGE_POINT_INTERMEDIATE, 5, 0)

end_package_point = PackagePoint('pp3', end_position, PACKAGE_POINT_END)

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

start_agent = ChainAgent('1', starting_position, [], Perception(1), PACKAGE_POINT_INTERMEDIATE, "dijkstra")
intermediate_agent = ChainAgent('2', intermediate_position, [], Perception(1), PACKAGE_POINT_END, "dijkstra")

# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(5, 5, [start_agent, intermediate_agent], [starting_package_point, intermediate_package_point, end_package_point], [starting_obstacle], [], True)

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



