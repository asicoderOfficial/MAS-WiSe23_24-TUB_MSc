from src.utils.position import Position



class Package:
    def __init__(self, id: str, position: Position, max_iterations_to_deliver: int) -> None:
        self.id = id
        self.position = position
        self.max_iterations_to_deliver = max_iterations_to_deliver
        self.iterations = 0
        self.is_delayed = False
        self.previous_position = position
    

    def step(self, new_position: Position) -> None:
        """ Method called at each iteration of the simulation."""
        self.previous_position = self.position
        self.position = new_position
