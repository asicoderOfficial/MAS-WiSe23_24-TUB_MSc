from typing import Tuple


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
    
    def __add__(self, direction_vector: Tuple[int, int]):
        """Shift position by direction vector

        Args:
            direction_vector (Tuple[int, int]): direction vector 

        Returns:
            Position: shifted position
        """
        x = self.x + direction_vector[0]
        y = self.y + direction_vector[1]
        return Position(x,y)
    
    def __sub__(self, direction_vector: Tuple[int, int]):
        """Shift position by direction vector

        Args:
            direction_vector (Tuple[int, int]): direction vector 

        Returns:
            Position: shifted position
        """
        x = self.x - direction_vector[0]
        y = self.y - direction_vector[1]
        return Position(x,y)
    

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)
