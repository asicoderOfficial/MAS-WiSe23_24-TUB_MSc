from typing import Union, List
from copy import deepcopy

from mesa import Agent as MesaAgent

from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.agents.perception import Perception


class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception) -> None:
        self.id = id
        self.position = position
        self.package = package
        self.perception = perception

    
    def step(self, environment_grid: List[List]) -> None:
        """ Method called at each iteration of the simulation."""
        # TODO: Strategy
        # TODO: Determine movement with algorith (Dijkstra, pheromones, etc.)
        chosen_new_position = Position(self.position.x + 1, self.position.y)
        self.move(chosen_new_position, environment_grid)
    

    def can_move_to(self, chosen_new_position: Position, environment_grid: List[List]) -> bool:
        """ Returns True if the agent can move to the chosen_new_position, False otherwise."""
        # Check if the chosen position is inside the grid of the environment.
        if chosen_new_position.x < 0 or chosen_new_position.x >= len(environment_grid) or \
           chosen_new_position.y < 0 or chosen_new_position.y >= len(environment_grid[0]):
            return False
        # Check if the chosen position is occupied by an obstacle.
        if environment_grid[chosen_new_position.x][chosen_new_position.y]['obstacles']:
            return False
        # Check if the chosen position is occupied by a package point.
        if environment_grid[chosen_new_position.x][chosen_new_position.y]['package_points']:
            return False

        return True        



    def move(self, chosen_new_position: Position, environment_grid: List[List]) -> None:
        """ Moves the agent."""
        # By now, the agent only moves to the right.
        # TODO: Implement a more complex movement (strategies, Dijkstra, pheromones, check basic movement rules, etc.)
        if self.can_move_to(chosen_new_position, environment_grid):
            self.position = chosen_new_position


    def pick_package(self, package: Package) -> None:
        if self.package:
            raise Exception(f'The agent is already carrying a package with id: {self.package.id}')
        self.package = package


    def deliver_package(self, package: Package, package_point: PackagePoint) -> None:
        package.position = deepcopy(package_point.position)
        self.package = None
