from src.agents.agent import Agent

from src.environment.package import Package
from src.environment.obstacle import Obstacle
from src.environment.package_point import PackagePoint

AGENT_KEY = 'agents'
PACKAGE_KEY = 'packages'
OBSTACLE_KEY = 'obstacles'
PACKAGE_POINT_KEY = 'package_points'

PACKAGE_POINT_INTERMIDIATE = "intermidiate-point"
PACKAGE_PONT_END = "end-point"

EMPTY_CELL = {
    AGENT_KEY : {},
    OBSTACLE_KEY : {},
    PACKAGE_POINT_KEY : {},
    PACKAGE_KEY : {}
}

ENTITIES_TO_KEYS = {
    Agent : AGENT_KEY,
    Package : PACKAGE_KEY,
    Obstacle : OBSTACLE_KEY,
    PackagePoint : PACKAGE_POINT_KEY
}
