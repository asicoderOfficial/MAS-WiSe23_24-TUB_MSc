from src.agents.agent import Agent

from src.environment.package import Package
from src.environment.obstacle import Obstacle
from src.environment.package_point import PackagePoint

EMPTY_CELL = {
    'agents' : {},
    'obstacles' : {},
    'package_points' : {},
    'packages' : {}
}

ENTITIES_TO_KEYS = {
    Agent: 'agents',
    Obstacle: 'obstacles',
    Package: 'packages',
    PackagePoint: 'package_points'
}
