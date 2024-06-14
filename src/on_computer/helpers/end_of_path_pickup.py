from Positions import get_robot_angle
from enum import Enum
import math
from on_ev3.RobotBuilder import Robot




def distance_between(point1, point2):
    a = point2[0] - point1[0]
    b = point2[1] - point1[1]
    return math.sqrt((a**2) + (b**2))


def get_target_heading(ball_position):
    robot_position = get_robot_position()
    if robot_position is None:
        return None
    return calculate_heading(robot_position, ball_position)

def adjust_heading(target_heading, current_heading):
    diff = target_heading - current_heading
    Robot.turn(diff)



    



print (distance_between((1,1), (2,2)))