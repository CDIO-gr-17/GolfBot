
import math
from positions.Goals import find_goal_coordinates

from src.on_computer.computer_vision.ComputerVision import get_robot_pos_with_mask
from src.on_computer.positions.Robot_direction import calculate_heading


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


def go_to_goal(grid):
    goal = find_goal_coordinates(grid)
    if goal is None:
        return None
    goal_coordinates = goal[1]
    adjusted_goal = (goal_coordinates[0], goal_coordinates[1] - 2) # Adjust the goal coordinates later to fit grid
    #move_to_point(adjusted_goal)
    goal_heading = get_target_heading_for_point(adjusted_goal)
    adjust_heading(goal_heading, 180)   # Should use get_robot_angle() instead of 180
    deposit()
    return "Goal reached!"

def deposit():
    Robot.straight(5) #adjust lenght here
    Robot.shoot_all_balls

def robot_is_close_to_ball():





