from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment

# Environment elements
starting_package = Package('p1', Position(1, 2), Position(1, 2), 10)

starting_package_point = PackagePoint('pp1', Position(1, 1), Position(2, 2))

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

starting_position = Position(0, 0)
a = Agent('a', starting_position, starting_package, Perception(1))

# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(5, 5, [a], [starting_package_point], [starting_obstacle], [starting_package])

m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

iterations = 5
for iteration in range(1, iterations+1):
    environment.step(iteration)
    print(f'Iteration {iteration}')
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    #print(environment.grid)