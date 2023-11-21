#dijkstra
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder


class Dijkstra:

    def dijkstra_path(self, grid_height: int, grid_width: int, matrix) -> None:
        # create grid for dijkstra
        grid = Grid(width=grid_width, height=grid_height, matrix=matrix)
        # start and end points on the grid
        start = grid.node(self.position.x, self.position.y)
        end = grid.node(self.package.position.x, self.package.position.y)
        
        # runs a dijkstra
        finder = DijkstraFinder()
        path, runs = finder.find_path(start, end, grid)

        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))