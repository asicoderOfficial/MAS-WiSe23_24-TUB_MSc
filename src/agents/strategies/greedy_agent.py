import random
from typing import Union
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.environment.package import Package
from src.utils.position import Position
from src.utils.grid2matrix import convert_grid_to_matrix



class GreedyAgent(Agent):
    def __init__(self, id: str, position: Position, package: Union[Package, None], 
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
        super().__init__(id, position, package, perception, algorithm_name)
        self.goal_package = None
        self.decision = decision
        self.previous_point = None


    def step(self, grid) -> None:
        if self.goal_package:
            if self.goal_package.destination.pos.x == self.pos.x and self.goal_package.destination.pos.y == self.pos.y:
                # We are in the destination, deliver package
                self.deliver_package(self.goal_package, self.goal_package.destination, grid)
                self.goal_package = None
            else:
                # We are carrying a package, but still did not reach the destination
                # Move towards the destination using the algorithm specified in the constructor
                next_pos = self.get_next_position(grid, perception, self.goal_package.destination.pos, self.origin_point)
                self.move(next_pos, perception, grid)
        perception = self.perception.percept(self.pos, grid)
        visible_packages_available = [package for package in perception.visible_packages if not package.picked]
        if not visible_packages_available:
            # Do a random move
            self.move(Position(self.pos.x + random.randint(-1, 1), self.pos.y + random.randint(-1, 1)), perception, grid)
        else:
            # Select the package based on decision parameter:
            # 0 - closest package to the agent
            # 1 - closest package not delayed
            # 2 - package that is closer to be delayed (but still is not)
            # 3 - package closer to its destination
            if self.decision == 0:
                distances_to_agent = []
                for package in visible_packages_available:
                    distances_to_agent.append((package, package.dist_to(self.pos)))
                distances_to_agent.sort(key=lambda x: x[1])
                self.chosen_package = distances_to_agent[0][0]
            elif self.decision == 1:
                distances_to_agent = []
                for package in visible_packages_available:
                    if not package.is_delayed:
                        distances_to_agent.append((package, package.dist_to(self.pos)))
                distances_to_agent.sort(key=lambda x: x[1])
                self.chosen_package = distances_to_agent[0][0]
            elif self.decision == 2:
                iterations_to_be_delayed = []
                for package in visible_packages_available:
                    if not package.is_delayed:
                        iterations_to_be_delayed.append((package, package.max_iterations_to_deliver - package.iterations))
                iterations_to_be_delayed.sort(key=lambda x: x[1])
                self.chosen_package = iterations_to_be_delayed[0][0]
            elif self.decision == 3:
                distances_to_destination = []
                for package in visible_packages_available:
                    distances_to_destination.append((package, package.dist_to(package.destination.pos)))
                distances_to_destination.sort(key=lambda x: x[1])
                self.chosen_package = distances_to_destination[0][0]
        
        if not self.chosen_package:
            # Do a random move
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