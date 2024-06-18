from ComputerMain import ROBOT_POSITION, ROBOT_HEADING,BIG_FRAME,SMALL_FRAME,GRID
from computer_vision.CourseDetection import get_masks_from_frame, get_grid
from computer_vision.RobotDetection import get_robot_pos_and_heading
from pathfinding.Convert_to_node_grid import convert_to_grid


def update_positions():
    global ROBOT_POSITION,ROBOT_HEADING,BIG_FRAME,SMALL_FRAME, GRID
    robot_data = get_robot_pos_and_heading(BIG_FRAME)
    if robot_data is not None:
        ROBOT_POSITION, ROBOT_HEADING = robot_data

    masks = get_masks_from_frame(SMALL_FRAME)
    grid_data = get_grid(masks)
    GRID = convert_to_grid(grid_data)
    print(ROBOT_HEADING)
