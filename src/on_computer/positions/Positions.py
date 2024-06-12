from positions.Displacement import move_point
from positions.Robot_direction import calculate_heading
from computer_vision.ComputerVision import get_grid, get_masks_from_camera, get_robot_pos_with_mask
from pathfinding.Convert_to_node_grid import convert_to_grid

masks = get_masks_from_camera()
raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
grid = convert_to_grid(raw_grid_data)

def find_start_node():
    robot_camera_position = get_robot_pos_with_mask(masks['blue'])
    robot_real_position = move_point(robot_camera_position, grid) #Accounting for displacement
    if (robot_real_position is None):
        print("Robot position is not found")
        return
    return grid[int(robot_real_position[0])][int(robot_real_position[1])]

def get_robot_angle():
    robot_camera_tail = get_robot_pos_with_mask(masks['green'])
    robot_real_tail = move_point(robot_camera_tail,grid)
    robot_angle = calculate_heading(robot_real_tail , find_start_node() )
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