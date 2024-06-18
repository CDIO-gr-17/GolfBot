from ComputerMain import ROBOT_POSITION, ROBOT_HEADING,BIG_FRAME,SMALL_FRAME,GRID
from computer_vision.CourseDetection import get_masks_from_frame, get_grid, find_clusters, find_clusters_center
from computer_vision.RobotDetection import get_robot_pos_and_heading
from pathfinding.Convert_to_node_grid import convert_to_grid
import cv2 as cv
import numpy as np

def update_positions():
    global ROBOT_POSITION,ROBOT_HEADING, GRID
    masks = get_masks_from_frame(SMALL_FRAME)
    grid_data = get_grid(masks)
    GRID = convert_to_grid(grid_data)
    robot_data = get_robot_pos_and_heading(BIG_FRAME)
    if robot_data is not None:
        ROBOT_HEADING, ROBOT_POSITION = robot_data
    print(ROBOT_HEADING)

