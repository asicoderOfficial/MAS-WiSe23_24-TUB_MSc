from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder

from src.utils.position import Position


class Dijkstra:

    def get_next_position(self, pos: Position, dest: Position, grid_height: int, grid_width: int, matrix) -> None:
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
    