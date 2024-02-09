import random

from typing import List
from src.agents.agent import Agent
from src.agents.agent import Agent
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.utils.position import Position
from src.constants.utility_functions import UTILITY_FUNCTIONS, UTILITY_FUNCTIONS_WITH_ONLY_ONE_ACTION, UTILITY_FUNCTIONS_WITH_ALL_POSSIBLE_ACTIONS


class Waiter(Agent):
    def __init__(self, id: str, position: Position, package: List[Package], perception: Perception, movement_algorithm: str, 
                 utility_function:str, tips_function, starting_package_point_pos:Position, max_packages:int=3, utility_kwargs:dict={}) -> None:
        super().__init__(id, position, package, perception, movement_algorithm)
        self.max_packages = max_packages
        self.speed = self.max_packages + 1
        self.utility_function = utility_function
        self.utility_function_kwargs = utility_kwargs
        self.current_action = ()
        self.collected_tips = 0
        self.table_served = 0
        self.tips_function = tips_function
        self.starting_package_point_pos = starting_package_point_pos

    
    def step(self, grid) -> None:
        if self.current_action:
            self.perform_action(self.current_action, grid)
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
            perception = self.perception.percept(self.pos, grid)
            for _, entities in perception.items():
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

            # If the agent is carrying packages, it can move to the delivery point
            if self.packages:
                for package in self.packages:
                    if package.destination.x != self.pos.x and package.destination.y != self.pos.y:
                        possible_actions.append(('go-deliver', package.destination)) 

            # If the agent is not at the starting package point where packages spawn, it can move to it
            if self.pos.x != self.starting_package_point_pos.x and self.pos.y != self.starting_package_point_pos.y:
                possible_actions.append(('go-start', self.starting_package_point_pos))

            if not possible_actions:
                possible_directions = self.algorithm.get_available_directions(self.pos, perception, grid)
                possible_positions = [self.pos + direction for direction in possible_directions]
                random_position = random.choice(possible_positions)
                best_action = ('go-random', random_position)
            else:
                # Evaluate the possible actions and pick the best one according to the utility function
                best_action = self.evaluate_actions(possible_actions, grid)

            # Perform the best action
            self.perform_action(best_action, grid)
    

    def evaluate_actions(self, possible_actions: List, grid) -> tuple:
        if self.utility_function in UTILITY_FUNCTIONS_WITH_ONLY_ONE_ACTION:
            return max([(action, UTILITY_FUNCTIONS[self.utility_function](action, grid, self)) for action in possible_actions], key=lambda x: x[1])[0]
        else:
            return max(UTILITY_FUNCTIONS[self.utility_function](possible_actions, grid, self), key=lambda x: x[0])


    def perform_action(self, best_action: tuple, grid) -> None:
        print(best_action)
        if len(best_action) == 3 and best_action[0] != 'deliver':
            best_action = (best_action[1], best_action[2])
        elif len(best_action) == 4:
            best_action = (best_action[1], best_action[2], best_action[3])
        print('best action', best_action)
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
                perception = self.perception.percept(self.pos, grid)
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
        self.table_served += 1

    def is_action_completed(self) -> bool:
        if self.pos.x == self.current_action[1].x and self.pos.y == self.current_action[1].y:
            return True
        return False
