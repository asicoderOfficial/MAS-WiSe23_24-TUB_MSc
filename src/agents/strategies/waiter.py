import random

from typing import List
from src.agents.agent import Agent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.utils.position import Position
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_START
from src.constants.utility_functions import UTILITY_FUNCTIONS


class Waiter(Agent):
    def __init__(self, id: str, position: Position, package: List[Package], perception: Perception, movement_algorithm: str, utility_function:str, tips_function, max_packages:int=3, utility_kwargs:dict={}) -> None:
        super().__init__(id, position, package, perception, movement_algorithm)
        self.max_packages = max_packages
        self.speed = self.max_packages + 1
        self.utility_function = utility_function
        self.utility_function_kwargs = utility_kwargs
        self.current_action = ()
        self.collected_tips = 0
        self.tips_function = tips_function

    
    def step(self, grid) -> None:
        perception = self.perception.percept(self.pos, grid)
        if self.current_action:
            self.perform_action(self.current_action, grid, perception)
            action_completed = self.is_action_completed()
            if self.current_action[0] == 'pick' and not action_completed:
                # Corner case: the agent performed the pick action, but the package was already picked up by another agent just before, in the same iteration
                # We have to make the agent forget about the action and re-evaluate the possible actions, as if not, the agent will be stuck in the same pick action without being able to perform it
                self.current_action = ()
            elif action_completed:
                self.current_action = ()
        else:
            possible_actions = []

            # If the agent is not carrying the maximum number of packages and there are packages in the environment
            for cell, entities in perception.items():
                for entity in entities:
                    if entity.pos.x == self.pos.x and entity.pos.y == self.pos.y:
                        if isinstance(entity, Package) and not entity.picked and len(self.packages) < self.max_packages and entity not in self.packages:
                            # The agent can pick up the package, as no other agent has picked it up
                            # it is not carrying the maximum number of packages and the package is not already being carried by the agent itself
                            possible_actions.append(('pick', entity))
                        elif isinstance(entity, PackagePoint):
                            for package in self.packages:
                                if package.destination == entity.pos:
                                    # The agent can deliver a package to the package point
                                    possible_actions.append(('deliver', entity, package))
                    else:
                        if isinstance(entity, PackagePoint) and entity.point_type == PACKAGE_POINT_START:
                            # The agent can move to the starting point
                            possible_actions.append(('go-start', Position(cell[0], cell[1])))
                        elif isinstance(entity, PackagePoint) and entity.point_type == PACKAGE_POINT_END:
                            # The agent can move to the ending point
                            possible_actions.append(('go-end', Position(cell[0], cell[1])))
            
            if not possible_actions:
                possible_directions = self.algorithm.get_available_directions(self.pos, perception, grid)
                possible_positions = [self.pos + direction for direction in possible_directions]
                random_position = random.choice(possible_positions)
                best_action = ('go-random', random_position)
            else:
                # Evaluate the possible actions and pick the best one according to the utility function
                best_action = self.evaluate_actions(possible_actions, grid)

            # Perform the best action
            self.perform_action(best_action, grid, perception)
    

    def evaluate_actions(self, possible_actions: List, grid) -> tuple:
        return max([(action, UTILITY_FUNCTIONS[self.utility_function](action, grid, self)) for action in possible_actions], key=lambda x: x[1])[0]


    def perform_action(self, best_action: tuple, grid, perception:Perception) -> None:
        # Perform the best action
        if best_action[0] == 'pick':
            super().pick_package(best_action[1], grid)
            self.speed -= 1
            self.current_action = ()
        elif best_action[0] == 'deliver':
            self.deliver_package(best_action[2], best_action[1], grid)
            self.speed += 1
            self.current_action = ()
        else:
            steps_left = self.speed
            while steps_left > 0:
                if best_action[0] == 'go-random':
                    super().move(best_action[1], perception, grid)
                    self.current_action = ()
                elif 'go' in best_action[0] and (best_action[1].x, best_action[1].y) != (self.pos.x, self.pos.y):
                    next_position = super().get_next_position(grid, best_action[1])
                    super().move(next_position, perception, grid)
                    if self.pos.x == best_action[1].x and self.pos.y == best_action[1].y:
                        steps_left = 0
                    else:
                        # Continue moving towards the goal
                        self.current_action = best_action
                
                steps_left -= 1
                
                
    def deliver_package(self, package: Package, package_point: PackagePoint, grid) -> None:
        super().deliver_package(package, package_point, grid)
        
        # Collect tips
        self.collected_tips += self.tips_function(package)

    def is_action_completed(self) -> bool:
        if self.pos.x == self.current_action[1].x and self.pos.y == self.current_action[1].y:
            return True
        return False
