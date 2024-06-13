from positions.Displacement import move_point
from positions.Robot_direction import calculate_heading
from computer_vision.ComputerVision import get_robot_pos_with_mask

def find_start_node(mask, grid):
    robot_camera_position = get_robot_pos_with_mask(mask)
    robot_real_position = move_point(robot_camera_position, grid) #Accounting for displacement
    if (robot_real_position is None):
        print("Robot position is not found")
        return
    return grid[int(robot_real_position[0])][int(robot_real_position[1])]

def get_robot_angle(masks, grid):
    robot_camera_tail = get_robot_pos_with_mask(masks['green'])
    robot_real_tail = move_point(robot_camera_tail,grid)
    robot_angle = calculate_heading(robot_real_tail , find_start_node(masks['blue'], grid) )
    if robot_angle is None:
        print("Robot angle is not found")
        return
    return robot_angle

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None