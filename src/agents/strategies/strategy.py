from typing import List

from utils.position import Position
from environment.obstacle import Obstacle


class Strategy():
    def find_path():
        pass
    
    def get_available_moves(self, perception: List[List], grid):
        available_moves = [(1,0), (0,1), (-1,0), (0,-1)] # add (0,0) for staying in place?
        return [move for move in available_moves if self.can_move_to(self.pos + move, perception, grid.width, grid.height)]
            

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