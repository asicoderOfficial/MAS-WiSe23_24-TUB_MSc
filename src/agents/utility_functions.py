
"""
Possible actions:
- pick
- deliver
- go-start
- go-deliver
- go-random
"""

from src.agents.tips_functions import linear_decreasing_time_tips


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
        elif action[0] == 'go-deliver':
            return 5
    else:
        return self.utility_function_kwargs[action[0]]


def naive_greedy(action:tuple, grid, self):
    """
    Main goal: to pick the most packages possible, and deliver them as soon as possible.
    """
    if self.max_packages > len(self.packages) and action[0] == 'pick':
        return 10
    elif action[0] == 'deliver':
        return 5
    elif action[0] == 'go-deliver':
        return 4
    elif action[0] == 'go-start':
        return 3
    elif action[0] == 'go-random':
        return 1
    return 0


def naive_fast(action:tuple, grid, self):
    """
    Main goal: to deliver the packages as soon as possible, always carrying only one package to maximize the speed.
    """
    if action[0] == 'pick':
        if len(self.packages) == 0:
            return 10
        else:
            return 0
    elif action[0] == 'deliver':
        return 5
    elif action[0] == 'go-deliver':
        return 4
    elif action[0] == 'go-start':
        return 3
    elif action[0] == 'go-random':
        return 1


def refined_greedy(possible_actions:list, grid, self):
    """
    Main goal: to pick the most packages possible sharing the same destination, and deliver them as soon as possible.
    """
    possible_packages_to_deliver = [action for action in possible_actions if action[0] == 'deliver']
    if possible_packages_to_deliver:
        return [(10, action[0], action[1], action[2]) for action in possible_packages_to_deliver] + [(0, action[0], action[1]) for action in possible_actions if action[0] != 'deliver']
    possible_actions_packages_to_pick = [action for action in possible_actions if action[0] == 'pick']
    if possible_actions_packages_to_pick:
        if not self.packages:
            destinations = {}
            for _, package in possible_actions_packages_to_pick:
                if package.destination not in destinations:
                    destinations[package.destination] = 1
                else:
                    destinations[package.destination] += 1
            # Select the destination with the most packages
            best_destination = max(destinations, key=destinations.get)
            # Select the packages that go to the best destination (closest to the agent's position)
            best_packages = [package for _, package in possible_actions_packages_to_pick if package.destination == best_destination]
            return [(10, 'pick', best_packages[0])] + [(0, action[0], action[1]) for action in possible_actions]
        else:
            same_destination_packages = [package for _, package in possible_actions_packages_to_pick if package.destination == self.packages[0].destination]
            if same_destination_packages:
                return [(10, 'pick', same_destination_packages[0])] + [(0, action[0], action[1]) for action in possible_actions]
            else:
                closest_to_starting_package_point = min([(package_action, self.starting_package_point_pos.dist_to(package_action[1].pos)) for package_action in possible_actions_packages_to_pick], key=lambda x: x[1])[0]
                return [(10, 'pick', closest_to_starting_package_point[1])] + [(0, action[0], action[1]) for action in possible_actions]
    else:
        if len(self.packages) > 0:
            return [(-self.pos.dist_to(self.packages[i].destination), action[0], action[1]) if action[0] == 'go-deliver' else (-1000, action[0], action[1]) for i, action in enumerate(possible_actions)]
        else:
            actions_values = []
            for action in possible_actions:
                if action[0] == 'go-start':
                    actions_values.append((10, action[0], action[1]))
                elif action[0] == 'go-random':
                    actions_values.append((1, action[0], action[1]))
                else:
                    actions_values.append((0, action[0], action[1]))
            return actions_values
    