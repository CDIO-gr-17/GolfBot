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
    (5, 5),   # Move right
    (4, 5),  # Move right
    (3, 5),  # Move right
    (2, 4),
    (1, 3)
    ]

    path_length = len(mock_path)
    #distance = robot.calculate_drive_factor(mock_path)
    #print (distance)
    #print(robot.moveToNeighbor(315,0,mock_path))
    #robot.moveToPoint(3,3,2,3,180,mock_path)
    forCounter  = 0 
    #for node in mock_path[1:]:  # Skip the starting node as it's the current position
    #    currentHeading = robot.moveToPoint(node[0], node[1], currentX, currentY, currentHeading, mock_path)
    #    currentX, currentY = node[0], node[1]  # Update current position
    #    forCounter +=1
    #    node+= robot.
    #    print("/////////////////////////////// For Counter: " + str(forCounter))
    path_length = len(mock_path)

    robot.move_through_path(mock_path[0],mock_path[path_length-1],currentHeading, mock_path)
        
    #if(currentX != mock_path[path_length-1][0] and currentY != mock_path[path_length-1][1]):
     #   currentHeading = robot.moveToPoint(mock_path[0][0], mock_path[1], currentX, currentY, currentHeading, mock_path)


test_navigation() #run the test