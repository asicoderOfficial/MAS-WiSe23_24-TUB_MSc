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


    def step(self, current_iteration: int, grid) -> None:
        """ The obstacle iterations left are updated.

        Args:
            current_iteration (int): The current iteration of the experiment.
        
        Returns:
            None
        """        
        if self.iterations_left == -1 and not self.pos is None:
            # The object has to disappear from the grid. It has already stayed in the environment for the required iterations.
            grid.remove_agent(self)
        elif current_iteration == self.starting_iteration:
            # The object has to appear in the grid now, it is the starting iteration.
            self.determine_position(grid)
            grid.place_agent(self, self.pos)
        if self.iterations_left >= 0 and current_iteration >= self.starting_iteration:
            self.iterations_left -= 1


    def is_in(self, position: Position) -> bool:
        """ Returns True if the position is inside the obstacle, False otherwise."""
        pass


    def _obstacles_overlap(self, obstacle1_x: int, obstacle1_y: int, obstacle1_width: int, obstacle1_height: int,
                      obstacle2_x: int, obstacle2_y: int, obstacle2_width: int, obstacle2_height: int) -> bool:
        """
        Check if two obstacles (rectangles) in a grid share any common cells.

        Args:
            obstacle1_x (int): The x-coordinate of the top-left corner of the first obstacle.
            obstacle1_y (int): The y-coordinate of the top-left corner of the first obstacle.
            obstacle1_width (int): The width of the first obstacle.
            obstacle1_height (int): The height of the first obstacle.
            obstacle2_x (int): The x-coordinate of the top-left corner of the second obstacle.
            obstacle2_y (int): The y-coordinate of the top-left corner of the second obstacle.
            obstacle2_width (int): The width of the second obstacle.
            obstacle2_height (int): The height of the second obstacle.

        Returns:
            bool: True if the obstacles overlap, False otherwise.
        """
        # Calculate the coordinates of the right-bottom corners of the obstacles
        obstacle1_right = obstacle1_x + obstacle1_width
        obstacle1_bottom = obstacle1_y + obstacle1_height
        obstacle2_right = obstacle2_x + obstacle2_width
        obstacle2_bottom = obstacle2_y + obstacle2_height

        # Check for horizontal overlap
        overlap_x = (obstacle1_x < obstacle2_right) and (obstacle1_right > obstacle2_x)

        # Check for vertical overlap
        overlap_y = (obstacle1_y < obstacle2_bottom) and (obstacle1_bottom > obstacle2_y)

        # Return True if there is both horizontal and vertical overlap
        return overlap_x and overlap_y
    

    def _is_position_valid(self, grid: list, x: int, y: int) -> bool:
        """ Checks if the position is valid for the obstacle in the environment to be placed.

        Args:
            grid (list): The current state of the environment.
            x (int): The top left x coordinate of the obstacle where it would be placed.
            y (int): The top left y coordinate of the obstacle where it would be placed.

        Returns:
            bool: True if the position is valid, False otherwise.
        """        
        for i in range(grid.width):
            for j in range(grid.height):
                if grid._grid[i][j]:
                    for entity in grid._grid[i][j]:
                        if isinstance(entity, Obstacle):
                            if self._obstacles_overlap(x, y, self.width, self.height, i, j, entity.width, entity.height):
                                return False
                        elif i == x and j == y:
                            return False

        return True

    
    def determine_position(self, grid: list) -> Position:
        """ Determines the position of the obstacle in the environment.

        Args:
            grid (list): The current state of the environment.

        Raises:
            Exception: If no valid position exists for the obstacle in the environment.

        Returns:
            Position: The position of the obstacle in the environment.
        """        
        if not self._is_position_valid(grid, self.pos.x, self.pos.y):
            if self.pos_determination == 'random':
                is_position_valid = False
                maximum_random_tries = 100
                while not is_position_valid:
                    random_x = random.randint(0, grid.width - 1)
                    random_y = random.randint(0, grid.height - 1)
                    is_position_valid = self._is_position_valid(grid, random_x, random_y)
                    maximum_random_tries -= 1
                    if maximum_random_tries == 0:
                        # No random choice of coordinates was valid. Check for all possible coordinates.
                        for i in range(len(grid)):
                            for j in range(len(grid[0])):
                                if self._is_position_valid(grid, i, j):
                                    self.pos = Position(i, j)
                                    return
                        # No valid position exists for the obstacle in the environment.
                        # TODO: This is a colision! Solve it in some way.
                        raise Exception('No valid position exists for the obstacle in the environment.')
