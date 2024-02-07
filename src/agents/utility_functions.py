
def naive(action:tuple, grid, self):
    """
    Simply return a number, depending on the kwargs.
    Possible kwargs: {}
    """
    if not self.utility_function_kwargs:
        if action[0] == 'pick':
            return 3
        elif action[0] == 'deliver':
            return 4
        elif action[0] == 'go-start':
            return 1
        elif action[0] == 'go-end':
            return 2
    else:
        return self.utility_function_kwargs[action[0]]

