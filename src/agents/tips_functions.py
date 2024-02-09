from src.environment.package import Package


def constant_tips(package: Package):
    return 1

def linear_decreasing_time_tips(package: Package, after_time=0):
    return (1 - min(1, (package.iterations + after_time) / package.max_iterations_to_deliver)) * 10