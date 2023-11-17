from abc import abstractmethod
from src.agents.perception import Perception
from src.utils.position import Position


class Strategy():
    
    @abstractmethod
    def get_next_position(position: Position, perception: Perception):
        """ Get next position, based on current position and perception
            
        Args:
            position (Position): _description_
            perception (Perception): _description_
        """
        pass