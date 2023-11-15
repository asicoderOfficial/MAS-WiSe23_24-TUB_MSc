from typing import List, Union
from copy import deepcopy

from mesa import Model


from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.utils.position import Position
from src.utils.objects_parser import object_to_dict
from src.constants.environment import EMPTY_CELL, ENTITIES_TO_KEYS


class Environment(Model):
    def __init__(self, grid_height: int, grid_width: int, agents: List[Agent], \
                 package_points: List[PackagePoint], obstacles: List[Obstacle], packages: List[Package]) -> None:
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = {agent.id: agent for agent in agents}
        self.package_points = {package_point.id: package_point for package_point in package_points}
        self.obstacles = {obstacle.id: obstacle for obstacle in obstacles}
        self.packages = {package.id: package for package in packages}

        # Create self.grid with grid_height rows and grid_width columns
        self.grid = [[deepcopy(EMPTY_CELL) for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.init_grid()


    def step(self) -> None:
        """ Method called at each iteration of the simulation."""
        previous_agents_positions = {agent.id: agent.position for agent in self.agents.values()}
        previous_packages_positions = {package.id: package.position for package in self.packages.values()}
        for _, agent_object in self.agents.items():
            agent_object.step()
            if agent_object.package_id:
                # The agent package_id != '', so the agent is carrying the package. So wherever the agent goes, the package goes too.
                self.packages[agent_object.package_id].step(agent_object.position)
        
        for _, obstacle_object in self.obstacles.items():
            obstacle_object.step()
        
        self.update_grid(previous_agents_positions, previous_packages_positions)


    def _update_entity_position(self, entity: Union[Agent, Package], previous_position: Position) -> None:
        entity_key = next((value for key, value in ENTITIES_TO_KEYS.items() if isinstance(entity, key)), None)
        current_position_cell = self.grid[entity.position.x][entity.position.y][entity_key]
        if entity.id not in current_position_cell:
            # The Agent / Package has moved to a new cell. Update the grid with its new position. Remove it from the cell it was in before.
            previous_position_cell = self.grid[previous_position.x][previous_position.y][entity_key]
            # Remove the entity from the previous cell it was in.
            del previous_position_cell[entity.id]
            # Add the entity to the new cell it is in.
        self.grid[entity.position.x][entity.position.y][entity_key][entity.id] = object_to_dict(entity)


    def update_grid(self, previous_agents_positions: dict, previous_packages_positions: dict) -> None:
        """ Updates the grid of the environment."""
        # Dynamic entities that move: Agents & Packages
        for agent_id, agent_object in self.agents.items():
            self._update_entity_position(agent_object, previous_agents_positions[agent_id])
        
        for package_id, package_object in self.packages.items():
            self._update_entity_position(package_object, previous_packages_positions[package_id])
        
        # Dynamic entities that do not move, but can disappear: Obstacles
        for obstacle_id, obstacle_object in self.obstacles.items():
            if obstacle_object.iterations_left == 0:
                # The object has to disappear from the grid.
                del self.grid[obstacle_object.position.x][obstacle_object.position.y][ENTITIES_TO_KEYS[Obstacle]][obstacle_id]
            

    def init_grid(self) -> None:
        for entity in [self.agents, self.package_points, self.obstacles, self.packages]:
            for entity_key, entity_object in entity.items():
                type_key = next((value for key, value in ENTITIES_TO_KEYS.items() if isinstance(entity_object, key)), None)
                self.grid[entity_object.position.x][entity_object.position.y][type_key][entity_key] = object_to_dict(entity_object).copy()


class Perception:
    def __init__(self, n_cells_around:int) -> None:
        self.n_cells_around = n_cells_around
    

    def percept(self, agent_position: Position, environment: Environment) -> Environment:
        """ Returns the list of packages in the agent's perception."""
        pass
