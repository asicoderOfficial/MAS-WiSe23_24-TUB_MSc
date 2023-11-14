from src.utils.position import Position
from src.environment.environment import Environment



class Perception:
    def __init__(self, n_cells_around:int) -> None:
        self.n_cells_around = n_cells_around
    

    def percept(self, agent_position: Position, environment: Environment) -> Environment:
        """ Returns the list of packages in the agent's perception."""
        pass
