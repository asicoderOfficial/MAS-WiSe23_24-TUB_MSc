from src.agents.agent import Agent

from src.utils.position import Position
from src.utils.objects_parser import object_to_dict
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle

from src.environment.environment import Environment

# Environment elements
starting_package = Package('p1', Position(1, 1),  10)

starting_package_point = PackagePoint('pp1', Position(1, 1))

starting_obstacle = Obstacle('o1', Position(2, 2), 1, 1, 1)

starting_position = Position(0, 0)
a = Agent('a', starting_position, 'p1')

# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(5, 5, [a], [starting_package_point], [starting_obstacle], [starting_package])
for i in range(5):
    for j in range(5):
        print(i, j)
        print(environment.grid[i][j])
    print()
print()
print()
print('--------------------')
print()
print()
environment.step()
#print(environment.grid)
for i in range(5):
    for j in range(5):
        print(i, j)
        print(environment.grid[i][j])
    print()