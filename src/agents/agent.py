from typing import Union

import mesa

from src.utils.position import Position
from src.environment.package import Package
from src.agents.perception import Perception


class Agent(mesa.Agent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception) -> None:
        self.id = id
        self.position = position
        self.package = package
        self.perception = perception

    
    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        pass
