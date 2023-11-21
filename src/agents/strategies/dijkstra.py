#dijkstra
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder

from src.utils.position import Position

# TODO: Package point shouldn't be walkable right now we have problem at "e"
# TODO: Obstacles are not showing in my environment

# save path then iterate

class Dijkstra:

    def dijkstra_path(self, pos: Position, dest: Position, grid_height: int, grid_width: int, matrix, count: int) -> None:
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


        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))

        return new_position
    