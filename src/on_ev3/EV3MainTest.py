import json
import EV3Connector
from RobotBuilder import Robot
from Heading import Heading



robot = Robot()
path = path = [
    {"x": 1, "y": 2},
    {"x": 3, "y": 4},
    {"x": 5, "y": 6},
    {"x": 7, "y": 8},
    {"x": 9, "y": 10}
]
distance = robot.calculate_drive_factor(path)
print (distance)
print(robot.moveForward(path))