from src.agents.agent import Agent
from src.agents.perception import Perception
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_START, PackagePoint
from src.environment.obstacle import Obstacle
from src.environment.environment import Environment
import random

from src.visualization.save import Save
from src.visualization.merge import Merge

# Define seed for reproducibility, this will be used for the whole program
random.seed(1)

# Environment elements
starting_position = Position(0, 0)
end_position = Position(4, 4)

starting_position_ab = Position(1, 1)

starting_package = Package('p1', starting_position, Position(1, 3), 10)

starting_package_point = PackagePoint('pp1', starting_position, PACKAGE_POINT_START, 5)

end_package_point = PackagePoint('pp2', end_position, PACKAGE_POINT_END)

starting_obstacle = Obstacle('o1', Position(0, 1), 1, 1, 1, 2)

a = Agent('a', starting_position, starting_package, Perception(1))
# List of agents
agents = [a]
# Environment
#environment = Environment(5, 5, [a], [], [], [])
environment = Environment(10, 10, agents, [starting_package_point, end_package_point], [starting_obstacle], [starting_package])

m = environment.grid_as_matrix()
print('Initial state')
for i in range(len(m)):
    print(m[i])
print()

# List of agents and package for logging
iteration_data_agent = []
iteration_data_package = []

iterations = 5
for iteration in range(1, iterations+1):
    environment.step()
    print(f'Iteration {iteration}')
    m = environment.grid_as_matrix(mode='visualization')
    for i in range(len(m)):
        print(m[i])
    print()
    for agent in agents:
        # apeend list for logging
        iteration_data_agent.append([iteration, agent.id, agent.pos.x, agent.pos.y, agent.package.id])
        iteration_data_package.append([iteration, agent.package.id, agent.package.pos.x, agent.package.pos.y, agent.package.destination.x, agent.package.destination.y, agent.package.is_delayed])
    #print(environment.grid)

Save.save_to_csv_agent(iteration_data_agent)
Save.save_to_csv_package(iteration_data_package)
Merge.merge()

