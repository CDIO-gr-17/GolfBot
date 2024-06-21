import Globals as G
from helpers.end_of_path_pickup import distance_between


def find_start_node():
    if G.GRID is None or G.ROBOT_POSITION is None:
        return None
    start_node = G.GRID[G.ROBOT_POSITION[1]][G.ROBOT_POSITION[0]]
    return start_node

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None

def sort_balls_by_distance():
    if G.ROBOT_POSITION is None or G.BALLS is None:
        return []
    balls = G.BALLS
    balls.sort(key=lambda ball: distance_between(G.ROBOT_POSITION, ball))
    return balls