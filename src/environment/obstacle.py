from typing import List
import random

from src.utils.position import Position



class Obstacle:
    """ Dynamic obstacle in the environment."""
    def __init__(self, id: str, position: Position, width: int, height: int, starting_iteration: int, duration:int, position_determination:str='random') -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the obstacle.
            position (Position): Position of the obstacle in the environment. 
                It is determined initially by the code that runs the experiment.
                However, as the obstacle appears at starting_iteration, it may happen that the position is not valid anymore, so this could be changed automatically by then.
                Once the agent is created, it will not move until it disappears.
            width (int): Width of the obstacle.
            height (int): Height of the obstacle.
            starting_iteration (int): Iteration in which the obstacle appears in the environment.
            duration (int): Number of iterations the obstacle will be in the environment.
            position_determination (str, optional): How to determine the position automatically. Defaults to 'random'.
        
        Returns:
            None
        """        
        self.id = id
        self.pos = position
        self.width = width
        self.height = height
        self.iterations_left = duration
        self.starting_iteration = starting_iteration
        self.pos_determination = position_determination
        self.cells_with_obstacle = []


    def step(self, current_iteration: int, grid) -> None:
        """ The obstacle iterations left are updated.

        Args:
            current_iteration (int): The current iteration of the experiment.
        
        Returns:
            None
        """        
        if self.iterations_left == 0 and not self.pos is None:
            # The object has to disappear from the grid. It has already stayed in the environment for the required iterations.
            #grid.remove_agent(self)
            self._disappear(grid)
        elif current_iteration == self.starting_iteration:
            # The object has to appear in the grid now, it is the starting iteration.
            self._appear(grid)
        self.iterations_left -= 1


    def _is_position_valid(self, grid: list, x: int, y: int) -> bool:
        """ Checks if the position is valid for the obstacle in the environment to be placed.

        Args:
            grid (list): The current state of the environment.
            x (int): The top left x coordinate of the obstacle where it would be placed.
            y (int): The top left y coordinate of the obstacle where it would be placed.

        Returns:
            bool: True if the position is valid, False otherwise.
        """        
        if x < 0 or x + self.height > grid.height or y < 0 or y + self.width > grid.width:
            return False
        for i in range(x, x + self.height):
            for j in range(y, y + self.width):
                if not grid.is_cell_empty([i, j]):
                    return False

        return True


    def _cells(self) -> List[Position]:
        return [ObstacleCell(id=self.id, pos=Position(self.pos.x + j, self.pos.y + i)) for i in range(self.width) for j in range(self.height)]


    def _appear(self, grid: list) -> List[Position]:
        """ Determines the position of the obstacle in the environment.

        Args:
            grid (list): The current state of the environment.

        Raises:
            Exception: If no valid position exists for the obstacle in the environment.

        Returns:
            Position: The position of the obstacle in the environment.
        """        
        if self.pos.x < 0 or self.pos.x + self.width > grid.width or self.pos.y < 0 or self.pos.y + self.height > grid.height:
            raise Exception(f'The obstacle won\'t fit in the environment ever, as its width and height are {self.width} and {self.height}, respectively, and x and y are {self.pos.x} and {self.pos.y}, respectively, which exceed the grid dimensions, or has a <= 0 value in its dimensions.')

        if not self._is_position_valid(grid, self.pos.x, self.pos.y):
            if self.pos_determination == 'random':
                is_position_valid = False
                maximum_random_tries = 100
                while not is_position_valid:
                    random_x = random.randint(0, grid.width - 1)
                    random_y = random.randint(0, grid.height - 1)
                    is_position_valid = self._is_position_valid(grid, random_x, random_y)
                    if is_position_valid:
                        self.pos.x = random_x
                        self.pos.y = random_y
                        self.cells_with_obstacle = self._cells()
                    maximum_random_tries -= 1
                    if maximum_random_tries == 0:
                        # No random choice of coordinates was valid. Check for all possible coordinates.
                        for x in range(len(grid._grid)):
                            for y in range(len(grid._grid[0])):
                                if (x, y) != (self.pos.x, self.pos.y) and self._is_position_valid(grid, x, y):
                                    self.pos.x = x
                                    self.pos.y = y
                                    self.cells_with_obstacle = self._cells()
                                    is_position_valid = True
                                    break
                            else:
                                continue
                            break
                        # No valid position exists for the obstacle in the environment.
                        # TODO: This is a colision! Solve it in some way.
                        #raise Exception('No valid position exists for the obstacle in the environment.')
                        # By now, the obstacle is just no placed. A solution could be to shrink it, or to divide it in n smaller obstacles
        else:
            self.cells_with_obstacle = self._cells()
        
        for cell in self.cells_with_obstacle:
            grid.place_agent(cell, cell.pos)


    def _disappear(self, grid):
        """ Removes the obstacle from the environment.

        Args:
            grid (list): The current state of the environment.

        Returns:
            None
        """        
        
        for cell in self.cells_with_obstacle:
            obstacle_cell = [obs for obs in grid._grid[cell.pos.x][cell.pos.y] if isinstance(obs, ObstacleCell)][0]
            grid.remove_agent(obstacle_cell)


class ObstacleCell:
    def __init__(self, id: str, pos: Position) -> None:
        self.id = id
        self.pos = pos


    def __iter__(self):
        yield self.x
        yield self.y
