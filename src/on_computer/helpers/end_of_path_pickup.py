
from ..positions.Goals import find_goal_coordinates




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


def go_to_goal(grid):
    goal = find_goal_coordinates(grid)
    print(goal)
    goal_coordinates = goal[1]
    print(goal_coordinates)
    adjusted_goal = (goal_coordinates[0] + 1, goal_coordinates[1])
    print(adjusted_goal)




