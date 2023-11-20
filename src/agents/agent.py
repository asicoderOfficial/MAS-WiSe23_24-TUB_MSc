from typing import Union, List
from copy import deepcopy

from mesa import Agent as MesaAgent
from mesa.space import MultiGrid

from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PackagePoint
from src.agents.perception import Perception
from src.environment.obstacle import Obstacle


class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception) -> None:
        """ Constructor.

        Args:
            id (str): The ID to identify the agent.
            position (Position): The position of the agent in the environment.
            origin (Union[Position, None]): Origin position of agent (assigned home), where agent should return if it is not carrying package. 
                                            If not defined, agent will return to first encountered package point
            package (Union[Package, None]): The package the agent is carrying. If the agent is not carrying any package, this value is None.
            package_point_type (str): Agent's goal package point type, agent will deliver package only to this type of package point.
            perception (Perception): The subgrid the agent is currently perceiving.
        
        Returns:
            None 
        """        
        self.id = id
        self.pos = position
        self.origin = position
        self.package = package
        self.perception = perception

    
    def step(self, grid) -> None:
        """ The agent performs an action.

        Args:
            grid (Environment): The current state of the grid.
        
        Returns:
            None 
        """        
        # TODO: Strategies (agents sub-classes)
        # TODO: Determine which action to perform (pick package, deliver package or move)
        # TODO: Determine movement with algorithm (Dijkstra, pheromones, etc.)
        # By now, the agent only moves down for demonstration purposes.
        perception = self.perception.percept(self.pos, grid)
       
        chosen_new_position = Position(self.pos.x + 1, self.pos.y)
        self.move(chosen_new_position, perception, grid)

    def can_move_to(self, chosen_new_position: Position, perception: List[List], grid_width: int, grid_height: int) -> bool:
        """ Checks if the agent can move to the chosen position.

        Args:
            chosen_new_position (Position): The position the agent wants to move to.
            perception (List[List]): The current state of the environment.

        Returns:
            bool: True if the agent can move to the chosen position, False otherwise.
        """        
        # Check if the chosen position is inside the grid of the environment.
        if chosen_new_position.x < 0 or chosen_new_position.x >= grid_width or \
           chosen_new_position.y < 0 or chosen_new_position.y >= grid_height:
            return False
        # Check if the chosen position is occupied by an obstacle.
        entities_in_chosen_new_position = perception[(chosen_new_position.x, chosen_new_position.y)]
        if entities_in_chosen_new_position:
            for entity in entities_in_chosen_new_position:
                if isinstance(entity, Obstacle):
                    return False

        return True        


    def move(self, chosen_new_position: Position, perception: List[List], grid: MultiGrid) -> None:
        """ Action of the agent: move to the chosen position.

        Args:
            chosen_new_position (Position): The position the agent wants to move to.
            perception (List[List]): The current state of the environment.
        
        Returns:
            None
        """        
        # By now, the agent only moves to the right.
        # TODO: Implement a more complex movement (strategies, Dijkstra, pheromones, check basic movement rules, etc.)
        if self.can_move_to(chosen_new_position, perception, grid.width, grid.height):
            grid.move_agent(self, chosen_new_position)
        else:
            raise Exception(f'The agent cannot move to the chosen position: {chosen_new_position}')


    def pick_package(self, package: Package, grid) -> None:
        """ Action of the agent: pick a package.

        Args:
            package (Package): The package the agent wants to pick.

        Raises:
            Exception: If the agent is already carrying a package.
            Exception: If the package is not in the same cell as the agent.
            Exception: If the agent is at a package point that is not an intermediate or starting point.
        
        Returns:
            None
        """        
        if self.package:
            raise Exception(f'The agent is already carrying a package with id: {self.package.id}')

        cell_entities_ids = [cell_entity.id for cell_entity in grid[self.pos.x][self.pos.y]]
        if package.id not in cell_entities_ids:
            raise Exception(f'The agent cannot pick package with id: {package.id}, as the package is not in the same cell as the agent.')

        cell_entities = [cell_entity for cell_entity in grid[self.pos.x][self.pos.y] if isinstance(cell_entity, PackagePoint) and cell_entity.point_type != 'ending-point']
        if not cell_entities:
            raise Exception(f'The agent cannot pick package with id: {package.id} at position {self.pos} as there are no intermediate or starting points in the cell.')

        self.package = package


    def deliver_package(self, package: Package, package_point: PackagePoint, grid) -> None:
        """ Action of the agent: deliver a package.

        Args:
            package (Package): The package the agent wants to deliver.
            package_point (PackagePoint): The package point the agent wants to deliver the package to.

        Returns:
            None
        """        
        # TODO: logic for case of intermediate point/end point
        cell_entities = [cell_entity for cell_entity in grid[self.pos.x][self.pos.y] if isinstance(cell_entity, PackagePoint)]
        if not cell_entities:
            raise Exception(f'The agent cannot deliver package with id: {package.id}, as the agent is is not in the same cell')

        if package_point.point_type == PACKAGE_POINT_END or package_point.point_type == PACKAGE_POINT_INTERMEDIATE:
            # The package has reached its destination! 
            # Therefore, now the agent is not carrying any package and the package has to disappear from the environment (so it is not visible anymore).
            grid.remove_agent(package)
            self.package = None
        else:
            raise Exception(f'The agent cannot deliver package with id: {package.id} with position {package.pos}, which is not an intermediate or ending point.')
