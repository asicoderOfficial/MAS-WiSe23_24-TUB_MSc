from random import shuffle
from typing import List, Union
from src.agents.perception import Perception
from src.environment.package import Package
from src.environment.obstacle import Obstacle
from src.agents.agent import Agent
from utils.position import Position
import random

class Pheromone:
    def __init__(self, id: str, pos: Position) -> None:
        self.id = id
        self.pos = pos
        self.strength = 1

class PheromoneStrategy():

    def step(self, pos: Position, previous_pos: Position, destination_pos: Position, visible_cells: List[List], grid) -> Position:       
        # if self.package:
        #     # Delivering package, drop pheromones of the previous point and move to destination
        #     # TODO: get correct pheromone for intermediate points
        #     search_pheromone_id = str(self.package.destination)
        #     drop_pheromone_id = str(self.origin)
        #     destination = self.package.destination
        # else:
        #     # TODO: Manage roaming and picking up packages in case of greedy agent
        #     search_pheromone_id = str(self.origin)
        #     drop_pheromone_id = str(self.previous_destination) if self.previous_destination is not None else None
        
        search_pheromone_id = str(destination_pos)
        drop_pheromone_id = str(previous_pos)
            
        pheromone_direction = self.get_pheromone_direction(visible_cells, search_pheromone_id)
        if pheromone_direction != (0,0):
            direction = pheromone_direction
        else:
            # Go in direction of destination
            # TODO: Use random movement or direction to destination?
            vector_to_destination = (destination_pos.x - pos.x, destination_pos.y - pos.y)
            # Normalize direction
            if vector_to_destination != (0,0): 
                if abs(vector_to_destination[0]) > abs(vector_to_destination[1]):
                    direction = (int(vector_to_destination[0] / abs(vector_to_destination[0])), 0)
                else:
                    direction = (0, int(vector_to_destination[1] / abs(vector_to_destination[1])))
            else:
                direction = vector_to_destination
    
        chosen_new_position = pos + direction
        
        # Handle obstacles if there are any
        # Try different directions until there are no options
        possible_directions = self.get_available_moves(visible_cells, grid)
        while any([isinstance(entity, Obstacle) for entity in visible_cells[chosen_new_position.to_tuple()]]):
            if len(possible_directions) > 0:
                direction = random.choice(possible_directions)
                chosen_new_position = pos + direction
            else: # No more options, stay at the same cell
                direction = (0,0)
                chosen_new_position = pos
                break

        self.drop_pheromone(drop_pheromone_id, grid)
        
    def get_pheromone_direction(self, visible_cells, pheromone_id):
        
        # Find visible pheromone with highest strength
        highest_pheromone_direction = (0,0) # default value, in case no pheromone found
        highest_pheromone_value = 0
        for direction, entities in visible_cells.items():
            # Check pheromones cell by cell
            if direction == (0,0):
                # Skip pheromones on agent position, they should not affect the path finding
                continue
            
            pheromones = [entity for entity in entities if isinstance(entity, Pheromone)]
            
            for pheromone in pheromones:
                if pheromone.id == pheromone_id and pheromone.strength > highest_pheromone_value:
                    highest_pheromone_direction = direction
                    highest_pheromone_value = pheromone.strength
        
        return highest_pheromone_direction
    
    def drop_pheromone(self, pheromone_id: str, grid):
        """Add pheromone to current cell. If there is pheromone with same id, increase its strength.

        Args:
            pheromone_id (str): id of pheromone that should be dropped
            grid: grid of the environment
        """
        
        cell_pheromones = [entity for entity in grid.get_cell_list_contents(self.pos.to_tuple()) if isinstance(entity, Pheromone) and entity.id == pheromone_id]
        if len(cell_pheromones) == 0:
            pheromone = Pheromone(pheromone_id, self.pos)
            grid.place_agent(pheromone, self.pos)
        else:
            cell_pheromones[0].strength += 1
            
    