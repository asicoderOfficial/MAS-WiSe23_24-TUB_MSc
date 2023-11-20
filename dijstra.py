#dijkstra
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder

from src.utils.position import Position

# TODO: Package point shouldn't be walkable right now we have problem at "e"
# TODO: Obstacles are not showing in my environment

# save path then iterate
class PathManager:
    _listPath = []

    @staticmethod
    def initialize_path(path):
        PathManager._listPath.extend(path)

    @staticmethod
    def get_path():
        return PathManager._listPath.copy()

class Dijkstra:

    def dijkstra_path(self, grid_height: int, grid_width: int, matrix, count: int) -> None:
        # create grid for dijkstra
        grid = Grid(width=grid_width, height=grid_height, matrix=matrix)
        # start and end points on the grid
        start = grid.node(self.pos.x, self.pos.y)
        end = grid.node(self.package.pos.x, self.package.pos.y)

        # runs a dijkstra
        finder = DijkstraFinder()
        path, runs = finder.find_path(start, end, grid)

        PathManager.initialize_path(path)
        listPath = PathManager.get_path()

        # iterating path
        if count < len(listPath):
            new_position = Position(listPath[count].x, listPath[count].y)


        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))

        return new_position
    