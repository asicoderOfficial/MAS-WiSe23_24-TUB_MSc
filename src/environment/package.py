from src.utils.position import Position



class Package:
    def __init__(self, id: str, position: Position, destination: Position, max_iterations_to_deliver: int) -> None:
        self.id = id
        self.position = position
        self.destination = destination
        self.max_iterations_to_deliver = max_iterations_to_deliver
        self.iterations = 0
        self.is_delayed = False
    

    def step(self, new_position: Position) -> None:
        """ Method called at each iteration of the simulation."""
        self.position = new_position
