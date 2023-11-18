

class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def dist_to(self, another_position) -> int:
        """Get Manhattan distance to another position

        Args:
            another_position (Position): another position object

        Returns:
            int: Manhattan distance to passed position
        """
        return abs(self.x - another_position.x) + abs(self.y - another_position.y)
        
    def __iter__(self):
        yield self.x
        yield self.y
