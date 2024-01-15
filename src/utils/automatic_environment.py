import random
import math

from src.agents.strategies.communication_chain_agent import CommunicationChainAgent
from src.agents.strategies.roaming_agent import RoamingAgent
from src.utils.position import Position
from src.environment.package_point import PACKAGE_POINT_END, PackagePoint, PACKAGE_POINT_INTERMEDIATE, PACKAGE_POINT_START

ENV_PP_UNIFORM_SQUARES = "uniform_squares"
ENV_PP_RANDOM_SQUARES = "random_squares"
ENV_PP_MANUAL = None


def generate_random_strategy_allocation(total_n_agents, n_strategies_to_test):
    # Initialize the array with zeros
    strategy_allocation = [0] * (2 * n_strategies_to_test)

    # Generate random integers for each strategy
    for i in range(n_strategies_to_test * 2 - 1):
        strategy_allocation[i] = random.randint(1, total_n_agents - sum(strategy_allocation) - (n_strategies_to_test * 2 - 1 - i))

    # The last element is the remaining balance to ensure the sum is total_n_agents
    strategy_allocation[-1] = total_n_agents - sum(strategy_allocation)

    return strategy_allocation


def distribute_agents(total_n_agents: int, strategies_to_test: list, n_configurations_to_test: int):
    """
    Example of call:

        total_n_agents = 4
        n_shuffles = 1
        algorithm = 'dijkstra'
        agents_configurations = distribute_agents(total_n_agents, 
                                                {'CommunicationChainAgent' :
                                                [
                                                    {'id':'gre1', 'position':None, 'packages':[], 'perception':Perception(1), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':algorithm},
                                                    {'id':'gre2', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(1), 'goal_package_point_type': PACKAGE_POINT_INTERMEDIATE, 'algorithm_name':algorithm}
                                                ],
                                                'RoamingAgent' : 
                                                [
                                                    {'id':'cha1', 'position':None, 'packages':[], 'perception':Perception(1), 'algorithm_name':'dijkstra'},
                                                    {'id':'cha2', 'position':starting_package_point_pos, 'packages':[], 'perception':Perception(1), 'algorithm_name':'dijkstra'}, 
                                                ] 
                                                },
                                                n_shuffles)
    """
    n_strategies_to_test = len(strategies_to_test)
    if total_n_agents < n_strategies_to_test * 2:
        raise Exception(f"Too low number of agents ({total_n_agents}) for {n_strategies_to_test} strategies. \
                        The minimum number of total agents to place would be {n_strategies_to_test * 2}")

    agents_distribution = []

    for n in range(n_configurations_to_test):
        strategies_allocations = generate_random_strategy_allocation(total_n_agents, n_strategies_to_test)
        cnt = 0
        ith_configuration = []
        for agent_strategy_id, parameters in strategies_to_test.items():
            for n_agents in range(strategies_allocations[cnt * 2]):
                if agent_strategy_id == 'CommunicationChainAgent':
                    agent = CommunicationChainAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'RoamingAgent':
                    agent = RoamingAgent(**parameters[0])
                    agent.id = f'{agent_strategy_id}-{parameters[0]["id"]}-{n}-{cnt * 2}-{n_agents}'
                    ith_configuration.append(agent)
            for n_agents in range(strategies_allocations[cnt * 2 + 1]):
                if agent_strategy_id == 'CommunicationChainAgent':
                    agent = CommunicationChainAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}'
                    ith_configuration.append(agent)
                elif agent_strategy_id == 'RoamingAgent':
                    agent = RoamingAgent(**parameters[1])
                    agent.id = f'{agent_strategy_id}-{parameters[1]["id"]}-{n}-{cnt * 2 + 1}-{n_agents}'
                    ith_configuration.append(agent)
            cnt += 1
        agents_distribution.append(ith_configuration)
    
    return agents_distribution


def distribute_package_points_random_squares(intermediate_package_points, ending_package_points, starting_package_point, 
                              grid, intermediate_package_points_l, ending_package_points_l):
    n_subrectangles = int(math.ceil((intermediate_package_points + ending_package_points) / 8))

    n_intermediate_points_by_subrectangle = {}
    n_ending_points_by_subrectangle = {}

    total_placed_intermediate_points = 0
    total_placed_ending_points = 0

    for subrectangle in range(1, n_subrectangles + 1):
        # Randomly decide to place an intermediate package point, so that it is more probable to place it in the first subrectangles (inner part of the grid, closer to starting package point)
        if total_placed_intermediate_points == intermediate_package_points and total_placed_ending_points == ending_package_points:
            break
        added_intermediate_points = 0
        added_ending_points = 0
        while added_intermediate_points + added_ending_points < 8 and (total_placed_ending_points < ending_package_points or total_placed_intermediate_points < intermediate_package_points):
            intermediate_point_probability = 1 - (subrectangle / n_subrectangles) if subrectangle != n_subrectangles else 0.9
            ending_point_probability = subrectangle / n_subrectangles if subrectangle != n_subrectangles else 0.1
            if random.random() < intermediate_point_probability and total_placed_intermediate_points < intermediate_package_points:
                if subrectangle in n_intermediate_points_by_subrectangle:
                    n_intermediate_points_by_subrectangle[subrectangle] += 1
                else:
                    n_intermediate_points_by_subrectangle[subrectangle] = 1
                added_intermediate_points += 1
                total_placed_intermediate_points += 1
            elif random.random() < ending_point_probability and total_placed_ending_points < ending_package_points:
                if subrectangle in n_ending_points_by_subrectangle:
                    n_ending_points_by_subrectangle[subrectangle] += 1
                else:
                    n_ending_points_by_subrectangle[subrectangle] = 1
                added_ending_points += 1
                total_placed_ending_points += 1

    for subrectangle in range(1, n_subrectangles + 1):
        # Randomly decide to place an ending package point, so that it is more probable to place it in the last subrectangles (outer part of the grid)
        if total_placed_ending_points == ending_package_points:
            # All ending package points have been placed
            break
        added_ending_points = 0
        while n_intermediate_points_by_subrectangle[subrectangle] + added_ending_points < 8:
            probability = subrectangle / n_subrectangles if subrectangle != n_subrectangles else 0.1
            if total_placed_ending_points < ending_package_points:
                break
            if probability:
                if subrectangle in n_ending_points_by_subrectangle:
                    n_ending_points_by_subrectangle[subrectangle] += 1
                else:
                    n_ending_points_by_subrectangle[subrectangle] = 1
                added_ending_points += 1
                total_placed_ending_points += 1

    subrectangles_height = int(math.ceil(starting_package_point.pos.x / n_subrectangles))
    subrectangles_width = int(math.ceil(starting_package_point.pos.y / n_subrectangles))
    if starting_package_point.pos.y + subrectangles_width == grid.height:
        subrectangles_width -= 1
    if starting_package_point.pos.x + subrectangles_height == grid.width:
        subrectangles_height -= 1
    for subrectangle in range(1, n_subrectangles + 1):
        subrectangles_height = subrectangles_height * subrectangle
        subrectangles_width = subrectangles_width * subrectangle
        # Generate 8 points in the subrectangle where a package point can be placed, taking as reference the starting package point
        # Top left
        top_left = (starting_package_point.pos.x - subrectangles_height, starting_package_point.pos.y - subrectangles_width)
        # Upper middle
        upper_middle = (starting_package_point.pos.x - subrectangles_height, starting_package_point.pos.y)
        # Top right
        top_right = (starting_package_point.pos.x - subrectangles_height, starting_package_point.pos.y + subrectangles_width)
        # Middle right
        middle_right = (starting_package_point.pos.x, starting_package_point.pos.y + subrectangles_width)
        # Bottom right
        bottom_right = (starting_package_point.pos.x + subrectangles_height, starting_package_point.pos.y + subrectangles_width)
        # Bottom middle
        bottom_middle = (starting_package_point.pos.x + subrectangles_height, starting_package_point.pos.y)
        # Bottom left
        bottom_left = (starting_package_point.pos.x + subrectangles_height, starting_package_point.pos.y - subrectangles_width)
        # Middle left
        middle_left = (starting_package_point.pos.x, starting_package_point.pos.y - subrectangles_width)
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
                grid.place_agent(pp, pp.pos)
                intermediate_package_points_l.append(pp)
            elif i in ending_points_indices:
                # Ending package point
                pp = PackagePoint(id=f'pp_ss{subrectangle}_{i}', position=Position(subrectangle_points[i][0], subrectangle_points[i][1]), point_type=PACKAGE_POINT_END)
                grid.place_agent(pp, pp.pos)
                ending_package_points_l.append(pp)

    return grid, intermediate_package_points_l, ending_package_points_l

def distribute_package_points_uniform_squares(grid, intermediate_pp_num, ending_pp_num):
    center = grid.width // 2
    outer_points_per_side = math.ceil(math.sqrt(ending_pp_num))
    inner_points_per_side = math.ceil(math.sqrt(intermediate_pp_num))

    # Calculate distances for inner and outer squares
    outer_distance = center - 1  # One unit away from the edge
    inner_distance = outer_distance // 2

    def get_square_points(center, distance, points_per_side):
        points = []
        for i in range(points_per_side):
            offset = i * (distance * 2) // (points_per_side - 1) - distance
            points.append(Position(center + offset, center - distance))  # Top side
            points.append(Position(center + offset, center + distance))  # Bottom side
            if i != 0 and i != points_per_side - 1:  # Avoid duplicating corners
                points.append(Position(center - distance, center + offset))  # Left side
                points.append(Position(center + distance, center + offset))  # Right side
        return points

    # Generate points for the outer and inner squares
    outer_square_points = get_square_points(center, outer_distance, outer_points_per_side)
    inner_square_points = get_square_points(center, inner_distance, inner_points_per_side)

    ending_pps = []
    for i, point in enumerate(outer_square_points):
        pp = PackagePoint(id=f'pp_ep_{i}', position=point, point_type=PACKAGE_POINT_END)
        grid.place_agent(pp, pp.pos)
        ending_pps.append(pp)
        
    intermediate_pps = []
    for i, point in enumerate(inner_square_points):
        pp = PackagePoint(id=f'pp_ip_{i}', position=point, point_type=PACKAGE_POINT_INTERMEDIATE)
        grid.place_agent(pp, pp.pos)
        intermediate_pps.append(pp)

    return grid, intermediate_pps, ending_pps
