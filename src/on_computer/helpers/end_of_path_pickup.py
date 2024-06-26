import math
from positions.Goals import find_goal_coordinates
from pathfinding.PathfindingAlgorithm import a_star
import Globals as G


def distance_between(point1, point2):
    a = point2[0] - point1[0]
    b = point2[1] - point1[1]
    return math.sqrt((a**2) + (b**2))