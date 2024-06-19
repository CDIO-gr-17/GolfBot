
import math
from positions.Goals import find_goal_coordinates
from pathfinding.PathfindingAlgorithm import a_star
import Globals as G


def distance_between(point1, point2):
    a = point2[0] - point1[0]
    b = point2[1] - point1[1]
    return math.sqrt((a**2) + (b**2))


# def get_target_heading_for_point(ball_position, mask_blue): #Whiches position to pickup ball
#     robot_position = get_robot_pos_with_mask(mask_blue)
#     if robot_position is None:
#         return None
#     return calculate_heading(robot_position, ball_position)

def adjust_heading(target_heading, current_heading):
    diff = target_heading - current_heading
    #Robot.turn(diff)


def get_path_to_goal():
    goal = find_goal_coordinates(G.GRID)
    if goal is None:
        return None
    goal_coordinates = goal[1]
    adjusted_goal = (goal_coordinates[0], goal_coordinates[1] - 2) # Adjust the goal coordinates later to fit grid
    path = a_star(G.GRID, G.ROBOT_POSITION, adjusted_goal)       #Maybe need conversion to Nodes
    return path


