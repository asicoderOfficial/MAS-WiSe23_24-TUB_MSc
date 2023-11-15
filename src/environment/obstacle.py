from src.utils.position import Position



class Obstacle:
    def __init__(self, id: str, position: Position, width: int, height: int, starting_iteration: int, duration:int) -> None:
        self.id = id
        self.position = position
        self.width = width
        self.height = height
        self.iterations_left = duration
        self.starting_iteration = starting_iteration


    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        if self.iterations_left > 0:
            self.iterations_left -= 1


    def is_in(self, position: Position) -> bool:
        """ Returns True if the position is inside the obstacle, False otherwise."""
        pass
