import random

from src.utils.position import Position



class Obstacle:
    def __init__(self, id: str, position: Position, width: int, height: int, starting_iteration: int, duration:int, position_determination:str='random') -> None:
        self.id = id
        self.position = position
        self.width = width
        self.height = height
        self.iterations_left = duration
        self.starting_iteration = starting_iteration
        self.position_determination = position_determination


    def step(self, current_iteration: int) -> None:
        """ Method called at each iteration of the simulation."""
        if self.iterations_left >= 0 and current_iteration >= self.starting_iteration:
            self.iterations_left -= 1


    def is_in(self, position: Position) -> bool:
        """ Returns True if the position is inside the obstacle, False otherwise."""
        pass

    
    def _is_position_valid(self, environment_grid: list, x: int, y: int) -> bool:
        environment_grid_keys = environment_grid[x][y].keys()
        for i in range(x, x + self.width):
            for j in range(y, y + self.height):
                for entity_id in environment_grid_keys:
                    if environment_grid[i][j][entity_id]:
                        return False

    
    def determine_position(self, environment_grid: list) -> Position:
        """ Determines the position of the obstacle in the environment."""
        if not self.position:
            if self.position_determination == 'random':
                is_position_valid = False
                maximum_random_tries = 100
                while not is_position_valid:
                    random_x = random.randint(0, len(environment_grid) - 1)
                    random_y = random.randint(0, len(environment_grid[0]) - 1)
                    is_position_valid = self._is_position_valid(environment_grid, random_x, random_y)
                    maximum_random_tries -= 1
                    if maximum_random_tries == 0:
                        # No random choice of coordinates was valid. Check for all possible coordinates.
                        for i in range(len(environment_grid)):
                            for j in range(len(environment_grid[0])):
                                if self._is_position_valid(environment_grid, i, j):
                                    self.position = Position(i, j)
                                    return
                        # No valid position exists for the obstacle in the environment.
                        # TODO: This is a colision! Solve it in some way.
                        raise Exception('No valid position exists for the obstacle in the environment.')
