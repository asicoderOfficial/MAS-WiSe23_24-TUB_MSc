from typing import Union
from src.agents.agent import Agent
from src.agents.perception import Perception
from agents.strategies.pheromone import PheromonePath
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START
from src.utils.position import Position
from utils.grid2matrix import convert_grid_to_matrix


class ChainAgent(Agent):
    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception, goal_package_point: str, algorithm_name: str) -> None:
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
        self.goal_package_point = goal_package_point
        self.previous_point = None
        if goal_package_point == PACKAGE_POINT_INTERMEDIATE:
            self.origin_point = PACKAGE_POINT_START
        elif goal_package_point == PACKAGE_POINT_END:
            self.origin_point = PACKAGE_POINT_INTERMEDIATE
        
    def step(self, grid) -> None:
        perception = self.perception.percept(self.pos, grid)
        
        if self.package:
            valid_package_points = [pp for pp in self.perception.visible_package_points if pp.point_type == self.goal_package_point]
            for package_point in valid_package_points:
                # Correct package point on current position, deliver package
                if self.goal_package_point == package_point.point_type \
                    and (package_point.point_type == PACKAGE_POINT_INTERMEDIATE or (self.goal_package_point == PACKAGE_POINT_END and self.package.destination == package_point.pos)):
                    # Found searched package point, deliver package
                    if self.pos == package_point.pos:
                        self.previous_point = self.package.destination
                        self.previous_point_type = self.goal_package_point
                        self.deliver_package(self.package, package_point, grid)
                        return   
            # Search for path to package point
            if self.goal_package_point == PACKAGE_POINT_INTERMEDIATE and self.package.intermediate_point_pos != None:
                destination = self.package.intermediate_point_pos
            else:
                destination = self.package.destination
            next_pos = self.get_next_position(grid, perception, destination, self.goal_package_point)
            self.move(next_pos, perception, grid)
        else:
            if self.origin == self.pos:
                # Package point should be on current position, pick up package
                current_packages = [package for package in perception[self.pos.to_tuple()] if isinstance(package, Package) and not package.picked]
                if len(current_packages) > 0:
                    self.previous_point = self.origin
                    self.previous_point_type = self.origin_point
                    self.pick_package(current_packages[0], grid)
                else:
                    print("Agent is at package point, but there are no packages, resting...")
            else:
                # Search for path to origin
                next_pos = self.get_next_position(grid, perception, self.origin, self.origin_point)
                self.move(next_pos, perception, grid)

    
    def get_next_position(self, grid, perception, destination: Position, destination_type: str) -> Position:
        if self.algorithm_name == 'dijkstra':
            chosen_new_position = self.algorithm.get_next_position(self.pos, destination, grid.height, grid.width, convert_grid_to_matrix(grid))
        elif self.algorithm_name == 'pheromones':
            chosen_new_position = self.algorithm.get_next_position(self.pos, self.previous_point, self.previous_point_type, destination, destination_type, perception, grid, False, True)
        else:
            raise Exception(f"Unknown algorithm: {self.algorithm_name}")
        return chosen_new_position