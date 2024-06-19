"""This is for doing somehting"""
from computer_vision.CourseDetection import get_masks_from_frame, get_grid
from computer_vision.RobotDetection import get_robot_pos_and_heading
from pathfinding.Convert_to_node_grid import convert_to_grid
import Globals as G

def update_positions():
    while True:
        masks = get_masks_from_frame(G.SMALL_FRAME)
        grid_data = get_grid(masks)
        G.GRID = convert_to_grid(grid_data)
        robot_data = get_robot_pos_and_heading(G.BIG_FRAME)
        if robot_data is not None:
            G.ROBOT_HEADING, G.ROBOT_POSITION = robot_data

