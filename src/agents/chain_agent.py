from typing import Union
from agents.agent import Agent
from agents.perception import Perception
from agents.strategies.pheromone_strategy import PheromoneStrategy
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START, PackagePoint
from src.utils.position import Position


class ChainAgent(Agent):
    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception, goal_package_point: str) -> None:
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
        super().__init__(id, position, package, perception)
        self.goal_package_point = goal_package_point
        self.previous_destination = None
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
                if self.goal_package_point == PACKAGE_POINT_INTERMEDIATE and package_point.point_type == PACKAGE_POINT_INTERMEDIATE:
                    # Found searched intermediate package point, deliver package
                    if self.pos == package_point.pos:
                        self.previous_destination = self.package.destination
                        self.deliver_package(self.package, package_point, grid)
                        return
                elif self.goal_package_point == PACKAGE_POINT_END and package_point.point_type == PACKAGE_POINT_END and self.package.destination == package_point.pos:
                    # Found searched end package point, deliver package
                    if self.pos == package_point.pos:
                        self.previous_destination = self.package.destination
                        self.deliver_package(self.package, package_point, grid)
                        return              
            # Search for path to package point
            next_pos = PheromoneStrategy().find_path(self.pos, self.origin, self.origin_point, self.package.destination, self.goal_package_point, perception, grid)
            self.move(next_pos, perception, grid)
        else:
            if self.origin == self.pos:
                # Package point should be on current position, pick up package
                current_packages = [package for package in perception[self.pos.to_tuple()] if isinstance(package, Package) and not package.picked]
                if len(current_packages) > 0:
                    self.pick_package(current_packages[0], grid)
                else:
                    print("Agent is at package point, but there are no packages, resting...")
            else:
                # Search for path to origin
                next_pos = PheromoneStrategy().find_path(self.pos, self.previous_destination, self.goal_package_point, self.origin, self.origin_point, perception, grid)
                self.move(next_pos, perception, grid)

