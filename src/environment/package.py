from src.utils.position import Position



class Package:
    def __init__(self, id: str, position: Position, max_iterations_to_deliver: int) -> None:
        self.id = id
        self.position = position
        self.max_iterations_to_deliver = max_iterations_to_deliver
        self.iterations = 0
        self.is_delayed = False
    

    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        pass
