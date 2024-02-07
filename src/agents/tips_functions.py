from src.environment.package import Package


def constant_tips(package: Package):
    return 1

def linear_decreasing_time_tips(package: Package):
    return (1 - min(1, package.iterations / package.max_iterations_to_deliver)) * 10
