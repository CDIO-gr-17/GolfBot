"""This is for doing somehting"""
import Globals as G
import time
import cv2 as cv

from computer_vision.CourseDetection import get_masks_from_frame, get_grid
from computer_vision.RobotDetection import get_robot_pos_and_heading
from pathfinding.Convert_to_node_grid import convert_to_grid


def update_positions():

    while True:
        masks = get_masks_from_frame(G.SMALL_FRAME)
        cv.imwrite('ImageWindow.jpg', masks['balls'])
        grid_data = get_grid(masks)
        robot_data = get_robot_pos_and_heading(G.BIG_FRAME)
        G.GRID = convert_to_grid(grid_data)
        if robot_data is not None:
            G.ROBOT_HEADING, G.ROBOT_POSITION = robot_data
            print('Robot Heading: ', G.ROBOT_HEADING)
        # time.sleep(0.1)
