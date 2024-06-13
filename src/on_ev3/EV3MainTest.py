import json
import EV3Connector
from RobotBuilder import Robot
from Heading import Heading

def test_navigation():
    robot = Robot() #setup
    currentHeading = robot.current_heading_degrees
    currentX, currentY = 1, 0  # Start position
    mock_path = [
    (1, 0),  # Start
    (2, 0),  # Move right
    (3, 0),  # Move right
    (4, 0),  # Turn, move up
    (5, 0),  # Move up
    (5, 1),  # Move up
    (5, 2),  # Turn, move right
    (5, 3),  # Move right
    (5, 4),  # Move right
    (5, 5)   # Move right
    ]
    #distance = robot.calculate_drive_factor(mock_path)
    #print (distance)
    #print(robot.moveToNeighbor(315,0,mock_path))
    #robot.moveToPoint(3,3,2,3,180,mock_path)

    for node in mock_path[1:]:  # Skip the starting node as it's the current position
        currentHeading = robot.moveToPoint(node[0], node[1], currentX, currentY, currentHeading, mock_path)
        currentX, currentY = node[0], node[1]  # Update current position


test_navigation() #run the test