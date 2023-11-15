from typing import Union
from copy import deepcopy

from mesa import Agent as MesaAgent

from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PackagePoint


class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package: Union[Package, None]) -> None:
        self.id = id
        self.position = position
        self.package = package

    
    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        self.move()
    

    def move(self) -> None:
        """ Moves the agent."""
        # By now, the agent only moves to the right.
        # TODO: Implement a more complex movement (strategies, Dijkstra, pheromones, check basic movement rules, etc.)
        self.position = Position(self.position.x + 1, self.position.y)


    def pick_package(self, package: Package) -> None:
        if self.package:
            raise Exception(f'The agent is already carrying a package with id: {self.package.id}')
        self.package = package


    def deliver_package(self, package: Package, package_point: PackagePoint) -> None:
        package.position = deepcopy(package_point.position)
        self.package = None
