from mesa import Agent as MesaAgent

from src.utils.position import Position


class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package_id: str) -> None:
        self.id = id
        self.position = position
        self.package_id = package_id
        self.previous_position = position

    
    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        self.previous_position = self.position
        self.move()
    

    def move(self) -> None:
        """ Moves the agent."""
        self.position = Position(self.position.x + 1)
