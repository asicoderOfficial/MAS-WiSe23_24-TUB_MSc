import random

from src.agents.strategies.communication_chain_agent import CommunicationChainAgent
from src.agents.strategies.roaming_agent import RoamingAgent


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