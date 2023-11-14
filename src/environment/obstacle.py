from src.utils.position import Position



class Obstacle:
    def __init__(self, id: str, top_left_corner: Position, width: int, height: int) -> None:
        self.id = id
        self.top_left_corner = top_left_corner
        self.width = width
        self.height = height


    def is_in(self, position: Position) -> bool:
        """ Returns True if the position is inside the obstacle, False otherwise."""
        pass
