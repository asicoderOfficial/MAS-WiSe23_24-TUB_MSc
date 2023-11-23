from typing import List, Union
from src.agents.agent import Agent
from src.agents.perception import Perception
from agents.strategies.pheromone import PheromonePath
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START
from src.utils.position import Position
from src.utils.grid2matrix import convert_grid_to_matrix


class ChainAgent(Agent):
    def __init__(self, id: str, position: Position, package: List[Package], perception: Perception, goal_package_point: str, algorithm_name: str) -> None:
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
        self.goal_package_point_type = goal_package_point
        self.previous_point = None
        if goal_package_point == PACKAGE_POINT_INTERMEDIATE:
            self.origin_point_type = PACKAGE_POINT_START
        elif goal_package_point == PACKAGE_POINT_END:
            self.origin_point_type = PACKAGE_POINT_INTERMEDIATE
        
    def step(self, grid) -> None:
        perception = self.perception.percept(self.pos, grid)
        
        if len(self.packages) > 0:
            valid_package_points = [pp for pp in self.perception.visible_package_points if pp.point_type == self.goal_package_point_type and pp.pos == self.pos]
            if len(valid_package_points) > 0:
                package_point = valid_package_points[0]
                # Correct package point on current position, deliver package
                if self.goal_package_point_type == package_point.point_type \
                    and (package_point.point_type == PACKAGE_POINT_INTERMEDIATE and (self.packages[0].destination != None or self.packages[0].destination == package_point.pos) \
                         or (self.goal_package_point_type == PACKAGE_POINT_END and self.packages[0].destination == package_point.pos)):
                    # Found searched package point, deliver package
                    if self.pos == package_point.pos:
                        self.previous_point = self.packages[0].destination
                        self.previous_point_type = self.goal_package_point_type
                        for package in self.packages:
                            self.deliver_package(package, package_point, grid)
                        return   
            # Search for path to package point
            if self.goal_package_point_type == PACKAGE_POINT_INTERMEDIATE and self.packages[0].intermediate_point_pos != None:
                destination = self.packages[0].intermediate_point_pos
            else:
                destination = self.packages[0].destination
            next_pos = self.get_next_position(grid, perception, destination, self.goal_package_point_type)
            self.move(next_pos, perception, grid)
        else:
            if self.origin == self.pos:
                # Package point should be on current position, pick up package
                current_packages = [package for package in perception[self.pos.to_tuple()] if isinstance(package, Package) and not package.picked]
                if len(current_packages) > 0:
                    package_order = self.get_biggest_package_order(current_packages, self.goal_package_point_type)
                    self.previous_point = self.origin
                    self.previous_point_type = self.origin_point_type
                    for package in package_order:
                        self.pick_package(package, grid)
                    print("Picked up", len(current_packages), "packages")
                else:
                    print("Agent is at package point, but there are no packages, resting...")
            else:
                # Search for path to origin
                next_pos = self.get_next_position(grid, perception, self.origin, self.origin_point_type)
                self.move(next_pos, perception, grid)

    
    def get_biggest_package_order(self, current_packages, goal_package_point) -> List[Package]:
        destinations = {}
        for package in current_packages:
            if goal_package_point == PACKAGE_POINT_INTERMEDIATE and package.intermediate_point_pos != None:
                # collect based on intermediate point
                if destinations.get(package.intermediate_point_pos) == None:
                    destinations[package.intermediate_point_pos] = [package]
                else: 
                    destinations[package.intermediate_point_pos].append(package)
            else:
                # collect based on end destination
                if destinations.get(package.destination) == None:
                    destinations[package.destination] = [package]
                else: 
                    destinations[package.destination].append(package)
        biggest_order = max(destinations.values(), key=lambda x: len(x))
        return biggest_order
                
    
    def get_next_position(self, grid, perception, destination: Position, destination_type: str) -> Position:
        if self.algorithm_name == 'dijkstra':
            chosen_new_position = self.algorithm.get_next_position(self.pos, destination, grid.height, grid.width, convert_grid_to_matrix(grid))
        elif self.algorithm_name == 'pheromones':
            chosen_new_position = self.algorithm.get_next_position(self.pos, self.previous_point, self.previous_point_type, destination, destination_type, perception, grid, False, True)
        else:
            raise Exception(f"Unknown algorithm: {self.algorithm_name}")
        return chosen_new_position