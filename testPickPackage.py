from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment

from src.visualization.save import Save
# Environment elements
starting_position = Position(0, 0)

starting_package = Package('p1', starting_position, Position(4, 4), 10)
starting_package2 = Package('p2', Position(1,0), Position(4, 4), 10)

starting_package_point = PackagePoint('pp1', Position(4, 4), Position(2, 2))

starting_obstacle = Obstacle('o1', Position(1, 1), 1, 1, 1, 2)

# - None for non package
a = Agent('a', starting_position, starting_package, Perception(1))
ab = Agent('ab', Position(1,0), starting_package2, Perception(1))
# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(5, 5, [a, ab], [starting_package_point], [starting_obstacle], [starting_package, starting_package2])
m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

iterations = 10
for iteration in range(1, iterations+1):
    print(f'Iteration {iteration}')
    environment.step(iteration)
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    #print(environment.grid)

# Save agent data
Save.save_to_csv([a])
# Visualize it
Save.visualize_data()

