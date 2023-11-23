from typing import List
from src.agents.strategies.path_algorithm import PathAlgorithm
from src.environment.obstacle import Obstacle
from src.utils.position import Position
import random

class Pheromone:
    def __init__(self, id: str, pos: Position, strength=1) -> None:
        self.id = id
        self.pos = pos
        self.strength = strength

class PheromonePath(PathAlgorithm):
    def __init__(self, pheromone_decrease_rate:int=0.01) -> None:
        self.previous_pheromone = None
        self.pheromone_decrease_rate = pheromone_decrease_rate
    
    def get_next_position(self, pos: Position, previous_pos: Position, previous_point_type, destination_pos: Position, destination_point_type, visible_cells: List[List], grid, enable_random_walk=True, decrease_pheromone:bool=True) -> Position:       
        
        search_pheromone_id = str(destination_pos) if not destination_point_type else f"{destination_pos}-{destination_point_type}"
        drop_pheromone_id = str(previous_pos) if not previous_point_type else f"{previous_pos}-{previous_point_type}"
        possible_directions = self.get_available_directions(pos, visible_cells, grid)
        pheromone_position = self.get_pheromone_direction(pos, visible_cells, search_pheromone_id)
        
        if pheromone_position != None:
            # get move to pheromone, for example if it is further then agent can move or on diagonal
            chosen_new_position = self.get_move_to_pheromone_position(pos, pheromone_position, visible_cells, grid)
        else:
            if enable_random_walk:
                # Random walk
                if (destination_pos - pos.to_tuple()).to_tuple() in possible_directions:
                    # destination in movement radius, go there
                    chosen_new_position = destination_pos
                else:
                    # no destination can be seen, random walk
                    chosen_new_position = pos + random.choice(possible_directions)
            else:
                # Go in direction of destination
                direction = self.get_normalized_vector_to_dest(pos, destination_pos)
                chosen_new_position = pos + direction
                
        # Handle obstacles if there are any
        # Try different directions until there are no options
        while any([isinstance(entity, Obstacle) for entity in visible_cells[chosen_new_position.to_tuple()]]):
            if len(possible_directions) > 0:
                # random walk
                direction = random.choice(possible_directions)
                chosen_new_position = pos + direction
            else: # No more options, stay at the same cell
                direction = (0,0)
                chosen_new_position = pos
                break

        # if not any([entity.pos == pos for entity in visible_cells[pos.to_tuple()] if isinstance(entity, PackagePoint)]):
            # If there is no package point on current position, drop pheromone
            # Dropping pheromone on package point can lead to problems
        self.drop_pheromone(pos, drop_pheromone_id, grid, decrease_pheromone)
        return chosen_new_position
    
    def get_move_to_pheromone_position(self, pos: Position, pheromone_position: Position, perception: List[List], grid) -> Position:
        vector_to_pheromone = (pheromone_position - pos.to_tuple()).to_tuple()
        if vector_to_pheromone in self.get_available_directions(pos, perception, grid):
            return pheromone_position
        else:
            return pos + self.get_normalized_vector_to_dest(pos, pheromone_position)
    
    def get_normalized_vector_to_dest(self, pos: Position, destination_pos: Position) -> Position:
        vector_to_destination = (destination_pos.x - pos.x, destination_pos.y - pos.y)
        # Normalize direction
        if vector_to_destination != (0,0): 
            if abs(vector_to_destination[0]) > abs(vector_to_destination[1]):
                direction = (int(vector_to_destination[0] / abs(vector_to_destination[0])), 0)
            else:
                direction = (0, int(vector_to_destination[1] / abs(vector_to_destination[1])))
        else:
            direction = vector_to_destination
        return direction
        
    def get_pheromone_direction(self, pos: Position, visible_cells, pheromone_id) -> Position:
        
        # Find visible pheromone with highest strength
        highest_pheromone_position = None # default value, in case no pheromone found
        highest_pheromone_value = 0
        for position, entities in visible_cells.items():
            # Check pheromones cell by cell
            if position == pos.to_tuple():
                # Skip pheromones on agent position, they should not affect the path finding
                continue
            
            pheromones = [entity for entity in entities if isinstance(entity, Pheromone)]
            
            for pheromone in pheromones:
                if pheromone.id == pheromone_id and pheromone.strength > highest_pheromone_value:
                    highest_pheromone_position = position
                    highest_pheromone_value = pheromone.strength
        
        if highest_pheromone_position != None:
            highest_pheromone_position = Position(highest_pheromone_position[0], highest_pheromone_position[1])
        return highest_pheromone_position
    
    def drop_pheromone(self, pos: Position, pheromone_id: str, grid, decrease_pheromone: bool):
        """Add pheromone to current cell. If there is pheromone with same id, increase its strength.

        Args:
            pheromone_id (str): id of pheromone that should be dropped
            grid: grid of the environment
        """
        
        cell_pheromones = [entity for entity in grid.get_cell_list_contents(pos.to_tuple()) if isinstance(entity, Pheromone) and entity.id == pheromone_id]
        if len(cell_pheromones) == 0:
            if self.previous_pheromone and self.previous_pheromone.id == pheromone_id and decrease_pheromone:
                pheromone = Pheromone(pheromone_id, pos, self.previous_pheromone.strength - self.pheromone_decrease_rate)
            else:
                pheromone = Pheromone(pheromone_id, pos)
            self.previous_pheromone = pheromone
            grid.place_agent(pheromone, pos)
            
    