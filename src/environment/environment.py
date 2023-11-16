from typing import List, Union
from copy import deepcopy

from mesa import Model


from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PackagePoint
from src.environment.obstacle import Obstacle
from src.utils.position import Position
from src.utils.objects_parser import object_to_dict
from src.constants.environment import EMPTY_CELL, ENTITIES_TO_KEYS, AGENT_KEY, PACKAGE_KEY, OBSTACLE_KEY, PACKAGE_POINT_KEY


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


    def step(self, current_iteration: int) -> None:
        """ Method called at each iteration of the simulation."""
        previous_agents_positions = {agent.id: agent.position for agent in self.agents.values()}
        previous_packages_positions = {package.id: package.position for package in self.packages.values()}
        for _, agent_object in self.agents.items():
            agent_object.step(self.grid)
            if agent_object.package.id:
                # The agent package_id != '', so the agent is carrying the package. So wherever the agent goes, the package goes too.
                self.packages[agent_object.package.id].step(agent_object.position)
        
        for _, obstacle_object in self.obstacles.items():
            obstacle_object.step(current_iteration)
        
        self.update_grid(previous_agents_positions, previous_packages_positions, current_iteration)


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


    def update_grid(self, previous_agents_positions: dict, previous_packages_positions: dict, current_iteration: int) -> None:
        """ Updates the grid of the environment."""
        # Dynamic entities that move: Agents & Packages
        for agent_id, agent_object in self.agents.items():
            self._update_entity_position(agent_object, previous_agents_positions[agent_id])
        
        for package_id, package_object in self.packages.items():
            self._update_entity_position(package_object, previous_packages_positions[package_id])
        
        # Dynamic entities that do not move, but can disappear: Obstacles
        for obstacle_id, obstacle_object in self.obstacles.items():
            if obstacle_object.iterations_left == -1 and obstacle_id in self.grid[obstacle_object.position.x][obstacle_object.position.y][ENTITIES_TO_KEYS[Obstacle]]:
                # The object has to disappear from the grid.
                del self.grid[obstacle_object.position.x][obstacle_object.position.y][ENTITIES_TO_KEYS[Obstacle]][obstacle_id]
            elif current_iteration == obstacle_object.starting_iteration:
                # The object has to appear in the grid now.
                obstacle_object.determine_position(self.grid)
                self.grid[obstacle_object.position.x][obstacle_object.position.y][ENTITIES_TO_KEYS[Obstacle]][obstacle_id] = object_to_dict(obstacle_object)
            

    def init_grid(self) -> None:
        for entity in [self.agents, self.package_points, self.packages]:
            for entity_key, entity_object in entity.items():
                type_key = next((value for key, value in ENTITIES_TO_KEYS.items() if isinstance(entity_object, key)), None)
                self.grid[entity_object.position.x][entity_object.position.y][type_key][entity_key] = object_to_dict(entity_object).copy()
        
        for obstacle_key, obstacle_object in self.obstacles.items():
            if obstacle_object.starting_iteration == 1:
                obstacle_object.determine_position(self.grid)
                self.grid[obstacle_object.position.x][obstacle_object.position.y][ENTITIES_TO_KEYS[Obstacle]][obstacle_key] = object_to_dict(obstacle_object).copy()


    def grid_as_matrix(self, mode:str='dijkstra') -> List[List]:
        matrix_grid = []
        if mode == 'dijkstra':
            return [
                [0 if self.grid[i][j][PACKAGE_POINT_KEY] or self.grid[i][j][OBSTACLE_KEY] else 1
                for j in range(self.grid_width)]
                for i in range(self.grid_height)
            ]
        if mode == 'visualization':
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    if self.grid[i][j][PACKAGE_POINT_KEY]:
                        column.append('x')
                    elif self.grid[i][j][OBSTACLE_KEY]:
                        column.append('o')
                    elif self.grid[i][j][PACKAGE_KEY]:
                        column.append('p')
                    elif self.grid[i][j][AGENT_KEY]:
                        column.append('a')
                    else:
                        column.append(' ')
                matrix_grid.append(column)

            return matrix_grid
        