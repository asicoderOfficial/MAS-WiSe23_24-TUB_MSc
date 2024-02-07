from src.agents.utility_functions import naive, naive_greedy, naive_fast, refined_greedy


UTILITY_FUNCTIONS = {
    'naive' : naive,
    'naive_greedy' : naive_greedy,
    'naive_fast' : naive_fast,
    'refined_greedy' : refined_greedy
}

UTILITY_FUNCTIONS_WITH_ONLY_ONE_ACTION = ['naive', 'naive_greedy', 'naive_fast']
UTILITY_FUNCTIONS_WITH_ALL_POSSIBLE_ACTIONS = ['refined_greedy']
