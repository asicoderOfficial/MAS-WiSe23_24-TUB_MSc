from typing import Union, List
from copy import deepcopy

from mesa import Agent as MesaAgent
from mesa.space import MultiGrid
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import MSG_PICKUP_RESPONSE, MSG_PACKAGE_DELIVERED, CommunicationLayer, Message

from src.agents.path_algorithms.pheromone import PheromonePath
from src.utils.position import Position
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_INTERMEDIATE, PackagePoint
from src.agents.perception import Perception
from src.environment.obstacle import Obstacle

from src.agents.path_algorithms.dijkstra import Dijkstra
from src.utils.grid2matrix import convert_grid_to_matrix
from src.visualization.save import Save

class Agent(MesaAgent):
    """ Parent class for all agents implemented in this project."""

    def __init__(self, id: str, position: Position, packages: List[Package], perception: Perception, algorithm_name: str) -> None:
        """ Constructor.

        Args:
            id (str): The ID to identify the agent.
            position (Position): The position of the agent in the environment.
            origin (Union[Position, None]): Origin position of agent (assigned home), where agent should return if it is not carrying package. 
                                            If not defined, agent will return to first encountered package point
            package (List[Package]): The packages the agent is carrying.
            perception (Perception): The subgrid the agent is currently perceiving.
            algorithm_name (str): Algorithm name to use for pathfinding. (Possible values: 'dijkstra', 'pheromone')
        
        Returns:
            None 
        """        
        self.id = id
        self.pos = position
        self.origin = position  # Origin (spawn) position 
        self.packages = packages
        self.perception = perception
        self.algorithm_name = algorithm_name
        self.goal_package_point_type = None
        if self.algorithm_name == 'dijkstra':
            self.algorithm = Dijkstra()
        elif self.algorithm_name == 'pheromones':
            self.algorithm = PheromonePath()
        else:
            raise Exception(f"Unknown algorithm: {self.algorithm_name}")

    
    def step(self, grid) -> None:
        """ The agent performs an action.

        Args:
            grid (Environment): The current state of the grid.
        
        Returns:
            None 
        """
        pass
    

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
        if self.can_move_to(chosen_new_position, perception, grid.width, grid.height):
            grid.move_agent(self, chosen_new_position)
        else:
            raise Exception(f'The agent cannot move to the chosen position: {chosen_new_position}')

    def get_next_position(self, grid, destination: Position) -> Position:
        perception = self.perception.percept(self.pos, grid)
        if self.algorithm_name == 'dijkstra':
            chosen_new_position = self.algorithm.get_next_position(self.pos, destination, grid.height, grid.width, convert_grid_to_matrix(grid))
        elif self.algorithm_name == 'pheromones':
            chosen_new_position = self.algorithm.get_next_position(self.pos, self.previous_point, self.previous_point_type, destination, self.goal_package_point_type, perception, grid, False, True)
        else:
            raise Exception(f"Unknown algorithm: {self.algorithm_name}")
        return chosen_new_position


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
        # if len(self.package) > 0:
        #     raise Exception(f'The agent is already carrying a package with id: {self.package.id}')
        if package.picked:
            raise Exception(f'Package {package.id} is already carried by another agent, but agent {self.id} is trying to pick it!')

        cell_entities_ids = [cell_entity.id for cell_entity in grid[self.pos.x][self.pos.y]]
        if package.id not in cell_entities_ids:
            raise Exception(f'The agent cannot pick package with id: {package.id}, as the package is not in the same cell as the agent.')

        cell_entities = [cell_entity for cell_entity in grid[self.pos.x][self.pos.y] if isinstance(cell_entity, PackagePoint) and cell_entity.point_type != 'ending-point']
        if not cell_entities:
            raise Exception(f'The agent cannot pick package with id: {package.id} at position {self.pos} as there are no intermediate or starting points in the cell.')

        self.append = self.packages.append(package)
        package.picked = True
        #printf"Agent {self.id}: Picked up package with ID {package.id} and position ({package.pos.x}, {package.pos.y})!")


    def deliver_package(self, package: Package, package_point: PackagePoint, grid) -> None:
        """ Action of the agent: deliver a package.

        Args:
            package (Package): The package the agent wants to deliver.
            package_point (PackagePoint): The package point the agent wants to deliver the package to.

        Returns:
            None
        """        
        cell_entities = [cell_entity for cell_entity in grid[self.pos.x][self.pos.y] if isinstance(cell_entity, PackagePoint)]
        if not cell_entities:
            raise Exception(f'The agent cannot deliver package with id: {package.id}, as the agent is is not in the same cell')
        
        if package.id not in [my_package.id for my_package in self.packages]:
            raise Exception(f'The agent cannot deliver package with id: {package.id}, as the agent is not carrying this package.')

        if package_point.point_type == PACKAGE_POINT_END:
            # The package has reached its destination! 
            # Therefore, now the agent is not carrying any package and the package has to disappear from the environment (so it is not visible anymore).
            package.picked = False
            Save.save_to_csv_package(package)
            # grid.remove_agent(package)
            self.packages.remove(package)
            # self.send_broker_message(Message(MSG_PACKAGE_DELIVERED, self.id, "broker", {f"Package: {package.id}, will deliver to the ending point"}))
        elif package_point.point_type == package_point.point_type == PACKAGE_POINT_INTERMEDIATE:
            package.picked = False
            self.packages.remove(package)
            # self.send_broker_message(Message(MSG_PACKAGE_DELIVERED, self.id, "broker",
            #                                  {f"Package: {package.id}, will deliver to the intermediate point"}))
        else:
            raise Exception(f'The agent cannot deliver package with id: {package.id} with position {package.pos}, which is not an intermediate or ending point.')
        
        #printf"Agent {self.id}: Delivered package {package.id} to package point of type {package_point.point_type}!")

    def receive_message(self, message) -> Message:
        #print"AGENT " + f"{self.id}: Received message: {message}")
        #Save.save_to_csv_messages(message, "Agent received message:")
        # TODO: message logic, what to do when a certain message is received
        # TODO: let's think about the logic what we should do after parcel was received and brokers knows about it
        return Message(MSG_PICKUP_RESPONSE, self.id, message.sender_id, {"response": "no"}) # placeholder

    def send_broker_message(self, message: Message):
        """Send message to a broker

        Args:
            message (Message): message to be sent
        """
        CommunicationLayer.send_to_broker(message)

 #   def send_agent_message(self, destination_agent_id: str, message: Message):
        """Send message to an agent

        Args:
            destination_agent_id (str) ID of the destination agent
            message (Message): message to be sent
        """
 #       CommunicationLayer.send_to_agent(destination_agent_id, message)
        