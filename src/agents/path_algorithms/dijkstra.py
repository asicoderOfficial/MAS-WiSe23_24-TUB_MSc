from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder

from src.utils.position import Position


class Dijkstra:

    def get_next_position(self, pos: Position, dest: Position, grid_height: int, grid_width: int, matrix) -> Position:
        """ Constructor.

        Args:
            pos (Position): Where the agent is at.
            dest (Position): Where the agent wants to go.
            grid_height (int): Height of the grid.
            grid_width (int): Width of the grid.
            matrix (_type_): Matrix of the grid for the Dijkstra algorithm. 
                Each element is a 0 or a 1. 0 means that the cell is free, 1 means that the cell is occupied by an obstacle.

        Returns:
            Position: The next cell the agent should go to.
        """        
        # create grid for dijkstra
        grid = Grid(width=grid_width, height=grid_height, matrix=matrix)
        # start and end points on the grid
        start = grid.node(pos.x, pos.y)
        end = grid.node(dest.x, dest.y)

        # runs a dijkstra
        finder = DijkstraFinder()
        path, runs = finder.find_path(start, end, grid)

        if len(path) > 1:
            new_position = Position(path[1].x, path[1].y)
        else:
            new_position = Position(path[0].x, path[0].y)

        return new_position
    