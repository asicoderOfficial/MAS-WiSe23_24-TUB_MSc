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
        self.position = position
        self.width = width
        self.height = height
        self.iterations_left = duration
        self.starting_iteration = starting_iteration
        self.position_determination = position_determination


    def step(self, current_iteration: int) -> None:
        """ The obstacle iterations left are updated.

        Args:
            current_iteration (int): The current iteration of the experiment.
        
        Returns:
            None
        """        
        if self.iterations_left >= 0 and current_iteration >= self.starting_iteration:
            self.iterations_left -= 1


    def is_in(self, position: Position) -> bool:
        """ Returns True if the position is inside the obstacle, False otherwise."""
        pass

    
    def _is_position_valid(self, environment_grid: list, x: int, y: int) -> bool:
        """ Checks if the position is valid for the obstacle in the environment to be placed.

        Args:
            environment_grid (list): The current state of the environment.
            x (int): The top left x coordinate of the obstacle where it would be placed.
            y (int): The top left y coordinate of the obstacle where it would be placed.

        Returns:
            bool: True if the position is valid, False otherwise.
        """        
        environment_grid_keys = environment_grid[x][y].keys()
        for i in range(x, x + self.width):
            for j in range(y, y + self.height):
                for entity_id in environment_grid_keys:
                    if environment_grid[i][j][entity_id]:
                        return False

    
    def determine_position(self, environment_grid: list) -> Position:
        """ Determines the position of the obstacle in the environment.

        Args:
            environment_grid (list): The current state of the environment.

        Raises:
            Exception: If no valid position exists for the obstacle in the environment.

        Returns:
            Position: The position of the obstacle in the environment.
        """        
        if not self._is_position_valid(environment_grid, self.position.x, self.position.y):
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
