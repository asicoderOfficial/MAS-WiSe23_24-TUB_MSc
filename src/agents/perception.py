from typing import List


from src.utils.position import Position


class Perception:
    """ What the agent can perceive from the environment."""
    def __init__(self, n_cells_around:int) -> None:
        """ Constructor.

        Args:
            n_cells_around (int): The number of cells around the agent that it can perceive forming a square.
        
        Returns:
            None
        """        
        self.n_cells_around = n_cells_around
        self.visible_packages = []
        self.visible_obstacles = []
        self.visible_package_points = []
    

    def percept(self, agent_position: Position, grid) -> List[List]:
        """ The agent perceives the environment.

        Args:
            agent_position (Position): The position of the agent in the environment.
            environment (Environment): The current state of the environment.

        Returns:
            List[List]: The subgrid the agent can perceive.
        """        
        visible_cells_positions = grid.get_neighborhood(agent_position, moore=True, include_center=True, radius=self.n_cells_around)
        visible_cells_entities = {}
        for cell_position in visible_cells_positions:
            visible_cells_entities[cell_position] = grid.get_cell_list_contents(cell_position)
        
        return visible_cells_entities
