import random
import math
from typing import List

from mesa import Model
from mesa.space import MultiGrid
from src.agents.chain_agent import ChainAgent
from src.agents.strategies.greedy_agent import GreedyAgent

from src.agents.agent import Agent
from src.environment.package import Package
from src.environment.package_point import PACKAGE_POINT_END, PACKAGE_POINT_START, PackagePoint, PACKAGE_POINT_INTERMEDIATE
from src.constants.environment import MAX_PERC_PACKAGE_POINTS
from src.utils.position import Position
from src.environment.obstacle import Obstacle, ObstacleCell
from src.constants.agents import AGENT_TYPES



class Environment(Model):
    """ The environment where the agents interact."""
    def __init__(self, grid_height: int, grid_width: int, agents_distribution: dict, \
                 starting_package_point: PackagePoint, n_intermediate_package_points: int, n_ending_package_points: int, 
                 obstacles: List[Obstacle], agents_distribution_strategy:str='strategic') -> None:

        """ Constructor.

        Args:
            grid_height (int): Height of the grid (number of rows)
            grid_width (int): Width of the grid (number of columns)
            agents (List[Agent]): Agents in the environment.
            obstacles (List[Obstacle]): Obstacles in the environment.
        Returns:
            None
        """        
        if n_intermediate_package_points + n_ending_package_points > grid_height * grid_width * MAX_PERC_PACKAGE_POINTS:
            raise Exception(f'Too many package points. The maximum number of package points is {grid_height * grid_width * MAX_PERC_PACKAGE_POINTS} for a {grid_height}x{grid_width} grid ({MAX_PERC_PACKAGE_POINTS * 100}% of the grid).')
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents_distribution_strategy = agents_distribution_strategy

        self.n_intermediate_package_points = n_intermediate_package_points
        self.n_ending_package_points = n_ending_package_points

        self.obstacles = obstacles
        self.agents_distribution = agents_distribution
        self.agents = []
        self.starting_package_point = starting_package_point
        self.intermediate_package_points = []
        self.ending_package_points = []

        
        self.current_iteration = 1

        # Create self.grid with grid_height rows and grid_width columns
        self.grid = MultiGrid(width=self.grid_width, height=self.grid_height, torus=False)
        self.init_grid()


    def step(self) -> None:
        """ Main method of the environment. It is called every iteration.
        
        Returns:
            None 
        """        
        for i, agent in enumerate(self.agents):
            agent.step(self.grid)
            if len(agent.packages) > 0:
                for package in agent.packages:
                    # The agent package_id != '', so the agent is carrying the package. So wherever the agent goes, the package goes too.
                    package.step(agent.pos, self.grid)
            # self.agents.pop(i)
            # self.agents.append(agent)
        
        for obstacle in self.obstacles:
            obstacle.step(self.current_iteration, self.grid)
            
        self.starting_package_point.step(self.current_iteration, self.grid, self.intermediate_package_points, self.ending_package_points)

        self.current_iteration += 1
            

    def init_grid(self) -> None:
        """ Initializes the grid with the static entities (Package Points, Obstacles and Packages).
        Called only once, at the beginning of the experiment.
        """        
        # Place static objects for the first time: package points
        # Starting package point
        self.grid.place_agent(self.starting_package_point, self.starting_package_point.pos) 
        # Intermediate and ending package points
        # Place them dynamically according to the starting package point position which is supposed to be in the center of the grid
        # They are created in 'circles', having the most inner circles more probability to have an intermediate package point, and the most outer circles more probability to have an ending package point
        n_subrectangles = int(math.ceil((self.n_intermediate_package_points + self.n_ending_package_points) / 8))

        n_intermediate_points_by_subrectangle = {}
        n_ending_points_by_subrectangle = {}

        total_placed_intermediate_points = 0
        total_placed_ending_points = 0

        for subrectangle in range(1, n_subrectangles + 1):
            # Randomly decide to place an intermediate package point, so that it is more probable to place it in the first subrectangles (inner part of the grid, closer to starting package point)
            if total_placed_intermediate_points == self.n_intermediate_package_points and total_placed_ending_points == self.n_ending_package_points:
                break
            added_intermediate_points = 0
            added_ending_points = 0
            while added_intermediate_points + added_ending_points < 8 and (total_placed_ending_points < self.n_ending_package_points or total_placed_intermediate_points < self.n_intermediate_package_points):
                intermediate_point_probability = 1 - (subrectangle / n_subrectangles) if subrectangle != n_subrectangles else 0.9
                ending_point_probability = subrectangle / n_subrectangles if subrectangle != n_subrectangles else 0.1
                if random.random() < intermediate_point_probability and total_placed_intermediate_points < self.n_intermediate_package_points:
                    if subrectangle in n_intermediate_points_by_subrectangle:
                        n_intermediate_points_by_subrectangle[subrectangle] += 1
                    else:
                        n_intermediate_points_by_subrectangle[subrectangle] = 1
                    added_intermediate_points += 1
                    total_placed_intermediate_points += 1
                elif random.random() < ending_point_probability and total_placed_ending_points < self.n_ending_package_points:
                    if subrectangle in n_ending_points_by_subrectangle:
                        n_ending_points_by_subrectangle[subrectangle] += 1
                    else:
                        n_ending_points_by_subrectangle[subrectangle] = 1
                    added_ending_points += 1
                    total_placed_ending_points += 1

        for subrectangle in range(1, n_subrectangles + 1):
            # Randomly decide to place an ending package point, so that it is more probable to place it in the last subrectangles (outer part of the grid)
            if total_placed_ending_points == self.n_ending_package_points:
                # All ending package points have been placed
                break
            added_ending_points = 0
            while n_intermediate_points_by_subrectangle[subrectangle] + added_ending_points < 8:
                probability = subrectangle / n_subrectangles if subrectangle != n_subrectangles else 0.1
                if total_placed_ending_points < self.n_ending_package_points:
                    break
                if probability:
                    if subrectangle in n_ending_points_by_subrectangle:
                        n_ending_points_by_subrectangle[subrectangle] += 1
                    else:
                        n_ending_points_by_subrectangle[subrectangle] = 1
                    added_ending_points += 1
                    total_placed_ending_points += 1

        subrectangles_height = int(math.ceil(self.starting_package_point.pos.x / n_subrectangles))
        subrectangles_width = int(math.ceil(self.starting_package_point.pos.y / n_subrectangles))
        for subrectangle in range(1, n_subrectangles + 1):
            subrectangles_height = subrectangles_height * subrectangle
            subrectangles_width = subrectangles_width * subrectangle
            # Generate 8 points in the subrectangle where a package point can be placed, taking as reference the starting package point
            # Top left
            top_left = (self.starting_package_point.pos.x - subrectangles_height, self.starting_package_point.pos.y - subrectangles_width)
            # Upper middle
            upper_middle = (self.starting_package_point.pos.x - subrectangles_height, self.starting_package_point.pos.y)
            # Top right
            top_right = (self.starting_package_point.pos.x - subrectangles_height, self.starting_package_point.pos.y + subrectangles_width)
            # Middle right
            middle_right = (self.starting_package_point.pos.x, self.starting_package_point.pos.y + subrectangles_width)
            # Bottom right
            bottom_right = (self.starting_package_point.pos.x + subrectangles_height, self.starting_package_point.pos.y + subrectangles_width)
            # Bottom middle
            bottom_middle = (self.starting_package_point.pos.x + subrectangles_height, self.starting_package_point.pos.y)
            # Bottom left
            bottom_left = (self.starting_package_point.pos.x + subrectangles_height, self.starting_package_point.pos.y - subrectangles_width)
            # Middle left
            middle_left = (self.starting_package_point.pos.x, self.starting_package_point.pos.y - subrectangles_width)
            # All the points in the subrectangle
            subrectangle_points = [top_left, upper_middle, top_right, middle_right, bottom_right, bottom_middle, bottom_left, middle_left]
            # Place the package points in the subrectangle
            n_intermediate_points_in_current_subrectangle = n_intermediate_points_by_subrectangle[subrectangle]
            # Pick n_intermediate_points_in_current_subrectangle random indices from subrectangle_points list
            intermediate_points_indices = random.sample(range(len(subrectangle_points)), n_intermediate_points_in_current_subrectangle)
            # Pick n_ending_points_in_current_subrectangle random indices from subrectangle_points list that are not in intermediate_points_indices
            ending_points_indices = random.sample([i for i in range(len(subrectangle_points)) if i not in intermediate_points_indices], n_ending_points_by_subrectangle[subrectangle])
            # Place the package points in the grid
            for i in range(len(subrectangle_points)):
                if i in intermediate_points_indices:
                    # Intermediate package point
                    pp = PackagePoint(id=f'pp_ss{subrectangle}_{i}', position=Position(subrectangle_points[i][0], subrectangle_points[i][1]), point_type=PACKAGE_POINT_INTERMEDIATE)
                    self.grid.place_agent(pp, pp.pos)
                    self.intermediate_package_points.append(pp)
                elif i in ending_points_indices:
                    # Ending package point
                    pp = PackagePoint(id=f'pp_ss{subrectangle}_{i}', position=Position(subrectangle_points[i][0], subrectangle_points[i][1]), point_type=PACKAGE_POINT_END)
                    self.grid.place_agent(pp, pp.pos)
                    self.ending_package_points.append(pp)

        intermediate_package_point_index = 0
        package_points_by_distance = [(pp, pp.pos.dist_to(self.starting_package_point.pos)) for pp in self.intermediate_package_points]
        package_points_by_distance.sort(key=lambda x: x[1])
        package_points_by_distance = [pp[0] for pp in package_points_by_distance]
        for agent_class_id, distribution in self.agents_distribution.items():
            for num_agents, parameters in distribution.items():
                for _ in range(num_agents):
                    if parameters['pos'] is None:
                        if self.agents_distribution_strategy == 'random':
                            # Place it in a random intermediate package point, as the position has not been specified (and we assume it will be the starting package point position)
                            parameters['pos'] = random.choice([pp.pos for pp in self.intermediate_package_points])
                        elif self.agents_distribution_strategy == 'strategic':
                            # Strategically place the agent in an intermediate point as close as possible to the starting package point,
                            # equally distributing agents among the intermediate points by traversing the list of intermediate points
                            # sorted by distance to the starting package point in a circular way
                            agent_position = package_points_by_distance[intermediate_package_point_index % len(package_points_by_distance)].pos
                            parameters['pos'] = agent_position
                            intermediate_package_point_index += 1
                    if agent_class_id.lower() == 'greedyagent':
                        self.agents.append(GreedyAgent(**parameters))
                    elif agent_class_id.lower() == 'chainagent':
                        self.agents.append(ChainAgent(**parameters))

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
                            if isinstance(entity, PackagePoint):
                                cell += 'x'
                            if isinstance(entity, Package):
                                cell += 'p'
                            if isinstance(entity, (Agent, ChainAgent)):
                                cell += 'a'
                            if isinstance(entity, ObstacleCell):
                                cell += 'o'
                        column.append(cell)
                    else:
                        column.append(' ')
                matrix_grid.append(column)

        return matrix_grid
        
