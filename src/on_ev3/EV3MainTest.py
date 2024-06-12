import json
import EV3Connector
from RobotBuilder import Robot
from Heading import Heading




robot = Robot()
mock_path = [
    {"x": 0, "y": 0},
    {"x": 1, "y": 1},
    {"x": 2, "y": 2},
    {"x": 3, "y": 3},
    {"x": 4, "y": 4}
]

path = ((0, 0), (1, 1), (2, 2), (3, 4), (4, 4))
distance = robot.calculate_drive_factor(path)
#print (distance)
print(robot.moveForward(path))