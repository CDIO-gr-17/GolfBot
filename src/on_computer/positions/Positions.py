from positions.Displacement import move_point
from positions.Robot_direction import calculate_heading
from computer_vision.Test import get_robot_pos_with_mask

def find_start_node():

    return grid[int(robot_real_position[1])][int(robot_real_position[0])]

def get_robot_angle(masks, grid):
    robot_camera_tail = get_robot_pos_with_mask(masks['blue'])
    robot_real_tail = move_point(robot_camera_tail,grid)
    start_node = find_start_node(masks['green'], grid)
    start_node_coordinates = [start_node.x, start_node.y]
    robot_angle = calculate_heading(robot_real_tail, start_node_coordinates)
    if robot_angle is None:
        print("Robot angle is not found")
        return
    robot_angle = int(robot_angle)
    print("Robot angle: ", robot_angle)
    return robot_angle

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None