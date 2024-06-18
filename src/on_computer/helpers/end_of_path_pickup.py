
import math
from positions.Goals import find_goal_coordinates
from pathfinding.PathfindingAlgorithm import a_star
from computer_vision.ComputerVision import get_robot_pos_with_mask
from positions.Robot_direction import calculate_heading


def distance_between(point1, point2):
    a = point2[0] - point1[0]
    b = point2[1] - point1[1]
    return math.sqrt((a**2) + (b**2))


def get_target_heading_for_point(ball_position, mask_blue): #Whiches position to pickup ball
    robot_position = get_robot_pos_with_mask(mask_blue)
    if robot_position is None:
        return None
    return calculate_heading(robot_position, ball_position)

def adjust_heading(target_heading, current_heading):
    diff = target_heading - current_heading
    #Robot.turn(diff)


def get_path_to_goal(grid, mask_blue):
    goal = find_goal_coordinates(grid)
    if goal is None:
        return None
    goal_coordinates = goal[1]
    adjusted_goal = (goal_coordinates[0], goal_coordinates[1] - 2) # Adjust the goal coordinates later to fit grid
    robot_pos = get_robot_pos_with_mask(mask_blue)
    path = a_star(grid, robot_pos, adjusted_goal)       #Maybe need conversion to Nodes
    return path

def deposit(mask_blue):
    robot_pos = get_robot_pos_with_mask(mask_blue)
    #goal_heading = calculate_heading(robot_pos,)
    goal_heading = 90 #directly east
    #Send command containing the following:
        #Robot.turntoheading(goal_heading)
        #Robot.straight(5) #adjust lenght here
        #Robot.shootallballs()
