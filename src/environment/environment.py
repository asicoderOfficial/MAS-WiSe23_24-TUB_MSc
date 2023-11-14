from typing import List, Union

from mesa import Model


from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.utils.position import Position
from src.utils.objects_parser import object_to_dict
from src.constants.environment import EMPTY_CELL


class Environment(Model):
    def __init__(self, grid_height: int, grid_width: int, agents: List[Agent], \
                 package_points: List[PackagePoint], obstacles: List[Obstacle], packages: List[Package]) -> None:
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = agents
        self.package_points = package_points
        self.obstacles = obstacles
        self.packages = packages

        # Create self.grid with grid_height rows and grid_width columns
        self.grid = [[EMPTY_CELL for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.update_grid()
    

    def _update_entity_position(self, entity: Union[Agent, Obstacle, Package]) -> None:
        if entity.id not in self.grid[entity.position.x][entity.position.y]:
            if isinstance(entity, Obstacle):
                if entity.duration == 0:
                    # The Obstacle does not appear anymore. Remove it from the grid.
                    del self.grid[entity.position.x][entity.position.y][entity.id]
            elif entity.id in self.grid[entity.previous_position.x][entity.previous_position.y]:
                # The entity (Agent or Package) has moved to another cell. Remove it from the previous cell, and update the grid with its new position.
                del self.grid[entity.previous_position.x][entity.previous_position.y][entity.id]
            self.grid[entity.position.x][entity.position.y][entity.id] = object_to_dict(entity)


    def update_grid(self) -> None:
        """ Updates the grid of the environment."""
        # Dynamic entities that move: Agents & Packages
        for agent in self.agents:
            self._update_entity_position(agent)
        
        for package in self.packages:
            self._update_entity_position(package)

        for obstacle in self.obstacles:
            self._update_entity_position(obstacle)
        


class Perception:
    def __init__(self, n_cells_around:int) -> None:
        self.n_cells_around = n_cells_around
    

    def percept(self, agent_position: Position, environment: Environment) -> Environment:
        """ Returns the list of packages in the agent's perception."""
        pass
