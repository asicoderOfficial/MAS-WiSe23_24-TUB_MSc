from typing import Union, List
from copy import deepcopy

from mesa import Agent as MesaAgent

from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.agents.perception import Perception
from src.constants.environment import OBSTACLE_KEY, PACKAGE_POINT_KEY


class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, package: Union[Package, None], perception: Perception) -> None:
        """ Constructor.

        Args:
            id (str): The ID to identify the agent.
            position (Position): The position of the agent in the environment.
            package (Union[Package, None]): The package the agent is carrying. If the agent is not carrying any package, this value is None.
            perception (Perception): The subgrid the agent is currently perceiving.
        
        Returns:
            None 
        """        
        self.id = id
        self.position = position
        self.package = package
        self.perception = perception

    
    def step(self, environment_grid: List[List]) -> None:
        """ The agent performs an action.

        Args:
            environment_grid (List[List]): The current state of the environment.
        
        Returns:
            None 
        """        
        # TODO: Strategies (agents sub-classes)
        # TODO: Determine which action to perform (pick package, deliver package or move)
        # TODO: Determine movement with algorithm (Dijkstra, pheromones, etc.)
        # By now, the agent only moves down for demonstration purposes.
        chosen_new_position = Position(self.position.x + 1, self.position.y)
        perception = self.perception.percept(self.position, environment_grid)
        self.move(chosen_new_position, perception)
    

    def can_move_to(self, chosen_new_position: Position, perception: List[List]) -> bool:
        """ Checks if the agent can move to the chosen position.

        Args:
            chosen_new_position (Position): The position the agent wants to move to.
            perception (List[List]): The current state of the environment.

        Returns:
            bool: True if the agent can move to the chosen position, False otherwise.
        """        
        # Check if the chosen position is inside the grid of the environment.
        if chosen_new_position.x < 0 or chosen_new_position.x >= len(perception) or \
           chosen_new_position.y < 0 or chosen_new_position.y >= len(perception[0]):
            return False
        # Check if the chosen position is occupied by an obstacle.
        if perception[chosen_new_position.x][chosen_new_position.y][OBSTACLE_KEY]:
            return False
        # Check if the chosen position is occupied by a package point.
        if perception[chosen_new_position.x][chosen_new_position.y][PACKAGE_POINT_KEY]:
            return False

        return True        


    def move(self, chosen_new_position: Position, perception: List[List]) -> None:
        """ Action of the agent: move to the chosen position.

        Args:
            chosen_new_position (Position): The position the agent wants to move to.
            perception (List[List]): The current state of the environment.
        
        Returns:
            None
        """        
        # By now, the agent only moves to the right.
        # TODO: Implement a more complex movement (strategies, Dijkstra, pheromones, check basic movement rules, etc.)
        if self.can_move_to(chosen_new_position, perception):
            self.position = chosen_new_position


    def pick_package(self, package: Package) -> None:
        """ Action of the agent: pick a package.

        Args:
            package (Package): The package the agent wants to pick.

        Raises:
            Exception: If the agent is already carrying a package.
        
        Returns:
            None
        """        
        if self.package:
            raise Exception(f'The agent is already carrying a package with id: {self.package.id}')
        self.package = package


    def deliver_package(self, package: Package, package_point: PackagePoint) -> None:
        """ Action of the agent: deliver a package.

        Args:
            package (Package): The package the agent wants to deliver.
            package_point (PackagePoint): The package point the agent wants to deliver the package to.

        Returns:
            None
        """        
        package.position = deepcopy(package_point.position)
        self.package = None
