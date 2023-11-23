from typing import List

from src.utils.position import Position
from src.environment.obstacle import Obstacle


class PathAlgorithm():
    def get_next_position(self):
        pass
    
    def get_available_directions(self, pos: Position, perception: List[List], grid):
        available_moves = [(1,0), (0,1), (-1,0), (0,-1)]
        available_moves = [move for move in available_moves if self.can_move_to(pos + move, perception, grid.width, grid.height)]
        if available_moves == []:
            return [(0,0)] # stay in place, if no other options
        else:
            return available_moves
            

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