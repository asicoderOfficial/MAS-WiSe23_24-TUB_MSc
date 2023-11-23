import random
from typing import Union, List
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.environment.package import Package
from src.utils.position import Position
from src.utils.grid2matrix import convert_grid_to_matrix



class GreedyAgent(Agent):
    def __init__(self, id: str, position: Position, packages: List[Package], 
                 perception: Perception, algorithm_name: str, decision: int=0) -> None:
        """Chain Agent delivers package only to specific package point type and returns to origin position after delivering package.

        Args:
            id (str): The ID to identify the agent.
            position (Position): The position of the agent in the environment.
            origin (Union[Position, None]): Origin position of agent (assigned home), where agent should return if it is not carrying package. 
                                            If not defined, agent will return to first encountered package point
            package (Union[Package, None]): The package the agent is carrying. If the agent is not carrying any package, this value is None.
            perception (Perception): The subgrid the agent is currently perceiving.
            package_point_type (str): Agent's goal package point type, agent will deliver package only to this type of package point.
        """
        super().__init__(id, position, packages, perception, algorithm_name)
        self.goal_package = None
        self.decision = decision
        self.previous_point = None


    def step(self, grid) -> None:
        perception = self.perception.percept(self.pos, grid)
        if self.goal_package:
            if self.goal_package.destination.x == self.pos.x and self.goal_package.destination.y == self.pos.y:
                # We are in the destination, deliver package
                self.deliver_package(self.goal_package, self.goal_package.destination, grid)
                self.goal_package = None
            else:
                # We are carrying a package, but still did not reach the destination
                # Move towards the destination using the algorithm specified in the constructor
                print(self.goal_package)
                print(self.goal_package.destination)
                next_pos = self.get_next_position(grid, perception, self.goal_package.destination, '')
                self.move(next_pos, perception, grid)
        visible_packages_available = [item for items in perception.values() for item in items if isinstance(item, Package) and item.picked == False]
        if not visible_packages_available:
            # Do a random move
            self.random_move(grid, perception)
        else:
            # Select the package based on decision parameter:
            # 0 - closest package to the agent
            # 1 - closest package not delayed
            # 2 - package that is closer to be delayed (but still is not)
            # 3 - package closer to its destination
            if self.decision == 0:
                distances_to_agent = []
                for package in visible_packages_available:
                    distances_to_agent.append((package, package.pos.dist_to(self.pos)))
                distances_to_agent.sort(key=lambda x: x[1])
                self.goal_package = distances_to_agent[0][0]
            elif self.decision == 1:
                distances_to_agent = []
                for package in visible_packages_available:
                    if not package.is_delayed:
                        distances_to_agent.append((package, package.pos.dist_to(self.pos)))
                distances_to_agent.sort(key=lambda x: x[1])
                self.goal_package = distances_to_agent[0][0]
            elif self.decision == 2:
                iterations_to_be_delayed = []
                for package in visible_packages_available:
                    if not package.is_delayed:
                        iterations_to_be_delayed.append((package, package.max_iterations_to_deliver - package.iterations))
                iterations_to_be_delayed.sort(key=lambda x: x[1])
                self.goal_package = iterations_to_be_delayed[0][0]
            elif self.decision == 3:
                distances_to_destination = []
                for package in visible_packages_available:
                    distances_to_destination.append((package, package.pos.dist_to(package.destination.pos)))
                distances_to_destination.sort(key=lambda x: x[1])
                self.goal_package = distances_to_destination[0][0]
        
        if not self.goal_package:
            # Do a random move
            self.random_move(grid, perception)
         
    def random_move(self, grid, perception) -> None:
        if self.pos.x == 0 and self.pos.y == 0:
            self.move(Position(self.pos.x + random.randint(0, 1), self.pos.y + random.randint(0, 1)), perception, grid)
        elif self.pos.x == 0 and self.pos.y == grid.height - 1:
            self.move(Position(self.pos.x + random.randint(0, 1), self.pos.y + random.randint(-1, 0)), perception, grid)
        elif self.pos.x == grid.width - 1 and self.pos.y == 0:
            self.move(Position(self.pos.x + random.randint(-1, 0), self.pos.y + random.randint(0, 1)), perception, grid)
        elif self.pos.x == grid.width - 1 and self.pos.y == grid.height - 1:
            self.move(Position(self.pos.x + random.randint(-1, 0), self.pos.y + random.randint(-1, 0)), perception, grid)
        elif self.pos.x == 0:
            self.move(Position(self.pos.x + random.randint(0, 1), self.pos.y + random.randint(-1, 1)), perception, grid)
        elif self.pos.x == grid.width - 1:
            self.move(Position(self.pos.x + random.randint(-1, 0), self.pos.y + random.randint(-1, 1)), perception, grid)
        elif self.pos.y == 0:
            self.move(Position(self.pos.x + random.randint(-1, 1), self.pos.y + random.randint(0, 1)), perception, grid)
        elif self.pos.y == grid.height - 1:
            self.move(Position(self.pos.x + random.randint(-1, 1), self.pos.y + random.randint(-1, 0)), perception, grid)
        else:
            self.move(Position(self.pos.x + random.randint(-1, 1), self.pos.y + random.randint(-1, 1)), perception, grid)


    def get_next_position(self, grid, perception, destination: Position, destination_type: str) -> Position:
        if self.algorithm_name == 'dijkstra':
            chosen_new_position = self.algorithm.get_next_position(self.pos, destination, grid.height, grid.width, convert_grid_to_matrix(grid))
        elif self.algorithm_name == 'pheromones':
            chosen_new_position = self.algorithm.get_next_position(self.pos, self.previous_point, self.previous_point_type, destination, 
                                                                   destination_type, perception, grid, False, True)
        else:
            raise Exception(f"Unknown algorithm: {self.algorithm_name}")
        return chosen_new_position