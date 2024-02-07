import random
import math
from typing import List, Union

from mesa import Model
from mesa.space import MultiGrid
from src.environment.communication.recruiter import Recruiter
from src.environment.communication.broker import Broker
from src.environment.communication.communication_layer import CommunicationLayer
from src.agents.strategies.chain_agent import ChainAgent
from src.agents.strategies.greedy_agent import GreedyAgent
from src.agents.strategies.roaming_agent import RoamingAgent
from src.agents.strategies.waiter import Waiter

from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PackagePoint, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START
from src.constants.environment import MAX_PERC_PACKAGE_POINTS
from src.utils.position import Position
from src.utils.automatic_environment import ENV_PP_RANDOM_SQUARES, ENV_PP_UNIFORM_SQUARES, distribute_package_points_random_squares, distribute_package_points_uniform_squares
from src.environment.obstacle import Obstacle, ObstacleCell
from src.visualization.save import Save



class Environment(Model):
    """ The environment where the agents interact."""
    def __init__(self, grid_height: int, 
                 grid_width: int, 
                 agents:list, 
                 starting_package_point: PackagePoint, 
                 intermediate_package_points: Union[int, List[Position]], 
                 ending_package_points: Union[int, List[Position]], 
                 obstacles: List[Obstacle], 
                 pp_distribution_strategy:str=ENV_PP_UNIFORM_SQUARES,
                 agents_distribution_strategy:str='strategic',
                 broker_optimality_criteria:str='naive',
                 communication_mechanism:str='broker'
                 ) -> None:

        """ Constructor.

        Args:
            grid_height (int): Height of the grid (number of rows)
            grid_width (int): Width of the grid (number of columns)
            agents_distribution (list): List of agents to be distributed in the environment. 
                Some of them may have a position specified, some of them may not and will automatically be placed according to the agents_distribution_strategy parameter.
            starting_package_point (PackagePoint): The starting package point where packages are generated from.
            n_intermediate_package_points (int): Number of intermediate package points in the environment.
            n_ending_package_points (int): Number of ending package points in the environment.
            obstacles (List[Obstacle]): Obstacles in the environment. Initially, they are placed in the specified position, but if it is not possible, they are placed in a random position,
                or at whichever position is possible. If there is no position available, the obstacle is finally not placed.
            agents_distribution_strategy (str, optional): Strategy to distribute the agents in the environment. Possible values: 'strategic' or 'random'. Defaults to 'strategic'.
                - 'strategic': Agents are distributed in the intermediate package points in a strategic way, so that the agents are equally distributed among the intermediate package points,
                    and the agents are placed in the intermediate package points that are closer to the starting package point.
                - 'random': Agents are distributed in the intermediate package points in a random way.

        Returns:
            None
        """        
        # if isinstance(intermediate_package_points, int) and isinstance(ending_package_points, int) and \
        #     intermediate_package_points + ending_package_points > grid_height * grid_width * MAX_PERC_PACKAGE_POINTS:
        #     raise Exception(f'Too many package points. The maximum number of package points is {grid_height * grid_width * MAX_PERC_PACKAGE_POINTS} for a {grid_height}x{grid_width} grid ({MAX_PERC_PACKAGE_POINTS * 100}% of the grid).')
        
        # Grid size
        self.grid_height = grid_height
        self.grid_width = grid_width
        # Create self.grid with grid_height rows and grid_width columns
        self.grid = MultiGrid(width=self.grid_width, height=self.grid_height, torus=False)

        # Package points
        self.starting_package_point = starting_package_point
        self.intermediate_package_points = intermediate_package_points
        self.ending_package_points = ending_package_points
        self.agents_distribution_strategy = agents_distribution_strategy
        self.intermediate_package_points_list = []
        self.ending_package_points_list = []
        self.pp_distribution_strategy = pp_distribution_strategy
        
        self.agents_l = agents
        self.obstacles = obstacles

        # Communication
        self.communication_mechanism = communication_mechanism
        self.broker_optimality_criteria = broker_optimality_criteria

        self.current_iteration = 0
        self.init_grid()
        self.init_communication_layer()
        Save.save_agent_init_state(self.agents_l)


    def step(self) -> None:
        """ Main method of the environment. It is called every iteration.
        
        Returns:
            None 
        """        
        for i, agent in enumerate(self.agents_l):
            agent.step(self.grid)
            if len(agent.packages) > 0:
                for package in agent.packages:
                    # Wherever the agent goes, the package goes too.
                    package.step(agent.pos, self.grid)
                    
        for package in self.starting_package_point.packages:    
            if package.pos is None:
                del package
                continue
            if not package.picked: # Only packages that weren't called in the previous loop
                package.step(package.pos, self.grid)
        
        for obstacle in self.obstacles:
            obstacle.step(self.current_iteration, self.grid)
            
        self.starting_package_point.step(self.current_iteration, self.grid, self.intermediate_package_points_list, self.ending_package_points_list)

        self.current_iteration += 1
            
    def init_communication_layer(self) -> None:
        if self.communication_mechanism == "broker":
            self.broker = Broker("broker", self.broker_optimality_criteria)
        elif self.communication_mechanism == "recruiter":
            self.broker = Recruiter("recruiter", self.broker_optimality_criteria)
        else:
            raise ValueError(f"Not a valid communication mechanism: {self.communication_mechanism}")
        CommunicationLayer.init(self.agents_l, self.broker)

    def init_grid(self) -> None:
        """ Initializes the grid with the static entities (Package Points, Obstacles and Packages).
        Called only once, at the beginning of the experiment.
        """        
        # Place static objects for the first time: package points
        # Starting package point
        self.grid.place_agent(self.starting_package_point, self.starting_package_point.pos) 

        if self.pp_distribution_strategy == ENV_PP_RANDOM_SQUARES:
            # Intermediate and ending package points automatic placement
            # Place them dynamically according to the starting package point position which is supposed to be in the center of the grid
            # They are created in 'circles', having the most inner circles more probability to have an intermediate package point, and the most outer circles more probability to have an ending package point
            self.grid, self.intermediate_package_points_list, self.ending_package_points_list = distribute_package_points_random_squares(self.intermediate_package_points, self.ending_package_points, self.starting_package_point, 
                                                                                                                    self.grid, self.intermediate_package_points_list, self.ending_package_points_list)
        elif self.pp_distribution_strategy == ENV_PP_UNIFORM_SQUARES:
            self.grid, self.intermediate_package_points_list, self.ending_package_points_list = distribute_package_points_uniform_squares(self.grid, self.intermediate_package_points, self.ending_package_points)
        else:
            # Intermediate and ending package points placement determined by the user, fixed
            for i in range(len(self.intermediate_package_points)):
                pp = PackagePoint(id=f'pp_i{i}', position=self.intermediate_package_points[i], point_type=PACKAGE_POINT_INTERMEDIATE)
                self.grid.place_agent(pp, pp.pos)
                self.intermediate_package_points_list.append(pp)
            for i in range(len(self.ending_package_points)):
                pp = PackagePoint(id=f'pp_e{i}', position=self.ending_package_points[i], point_type=PACKAGE_POINT_END)
                self.grid.place_agent(pp, pp.pos)
                self.ending_package_points_list.append(pp)

        # Spawn initial packages
        self.starting_package_point.step(self.current_iteration, self.grid, self.intermediate_package_points_list, self.ending_package_points_list)

        # Agents
        intermediate_package_point_index = 0
        package_points_by_distance = [(pp, pp.pos.dist_to(self.starting_package_point.pos)) for pp in self.intermediate_package_points_list]
        package_points_by_distance.sort(key=lambda x: x[1])
        package_points_by_distance = [pp[0] for pp in package_points_by_distance]
        agents_updated = []
        for agent in self.agents_l:
            if agent.pos is None:
                if self.agents_distribution_strategy == 'random':
                    # Place it in a random intermediate package point, as the position has not been specified (and we assume it will be the starting package point position)
                    random_pos = random.choice([pp.pos for pp in self.intermediate_package_points_list])
                    agent.pos = random_pos
                    agent.origin = random_pos
                elif self.agents_distribution_strategy == 'strategic':
                    # Strategically place the agent in an intermediate point as close as possible to the starting package point,
                    # equally distributing agents among the intermediate points by traversing the list of intermediate points
                    # sorted by distance to the starting package point in a circular way
                    agent_position = package_points_by_distance[intermediate_package_point_index % len(package_points_by_distance)].pos
                    agent.pos = agent_position
                    agent.origin = agent_position
                    intermediate_package_point_index += 1
            self.grid.place_agent(agent, agent.pos)
            agents_updated.append(agent)
        self.agents_l = agents_updated

        # Place dynamic objects for the first time
        for obstacle in self.obstacles:
            obstacle.step(self.current_iteration, self.grid)

        self.current_iteration += 1


    def grid_as_matrix(self, mode:str='dijkstra') -> List[List]:
        """ Convert the grid to a matrix of dimensions self.grid_height x self.grid_width.

        Args:
            mode (str, optional): How to create the matrix, depending on the purpose. Defaults to 'dijkstra'.

        Returns:
            List[List]: The grid as a matrix.
        """        
        matrix_grid = []
        if mode == 'dijkstra':
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    if self.grid._grid[i][j]:
                        # check if there is some instance of ObstacleCell in the cell
                        if any(isinstance(entity, ObstacleCell) for entity in self.grid._grid[i][j]):
                            column.append(0)
                        else:
                            column.append(1)
                    else:
                        column.append(1)
                matrix_grid.append(column)
        elif mode == 'visualization':
            for i in range(self.grid_height):
                column = []
                for j in range(self.grid_width):
                    cell = ''
                    if self.grid[i][j]:
                        for entity in self.grid[i][j]:
                            # Package points
                            if isinstance(entity, PackagePoint):
                                if entity.point_type == PACKAGE_POINT_START:
                                    cell += 's'
                                elif entity.point_type == PACKAGE_POINT_INTERMEDIATE:
                                    cell += 'i'
                                elif entity.point_type == PACKAGE_POINT_END:
                                    cell += 'e'
                            # Packages
                            if isinstance(entity, Package):
                                cell += 'p'
                            # Agents
                            if isinstance(entity, ChainAgent):
                                cell += 'c'
                            if isinstance(entity, GreedyAgent):
                                cell += 'g'
                            if isinstance(entity, RoamingAgent):
                                cell += 'r'
                            if isinstance(entity, Waiter):
                                cell += 'w'
                            # Obstacles
                            if isinstance(entity, ObstacleCell):
                                cell += 'o'
                        column.append(cell)
                    else:
                        column.append(' ')
                matrix_grid.append(column)

        return matrix_grid
        