from src.utils.position import Position



class Package:
    """ A package that the agent can carry, or that can be stored in the PackagePoint."""
    def __init__(self, id: str, position: Position, destination: Position, max_iterations_to_deliver: int) -> None:
        """ Constructor.

        Args:
            id (str): ID to identify the package.
            position (Position): Position of the package in the environment.
            destination (Position): Position where the package has to be delivered. It is determined initially by the code that runs the experiment. It will not change. It is a PackagePoint.
            max_iterations_to_deliver (int): Maximum number of iterations the agent has to deliver the package.
        
        Returns:
            None
        """        
        self.id = id
        self.pos = position
        self.destination = destination
        self.max_iterations_to_deliver = max_iterations_to_deliver
        self.iterations = 0
        self.is_delayed = False
    

    def step(self, new_position: Position, grid) -> None:
        """ The package position and internal state are updated.

        Args:
            new_position (Position): The new position of the package in the environment.
        
        Returns:
            None
        """        
        grid.move_agent(self, new_position)
        self.iterations += 1
        if self.iterations >= self.max_iterations_to_deliver:
            self.is_delayed = True
