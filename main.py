#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end
import math
import Heading.py

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = "0.0.0.0"
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

# Initialize the drive base.
WHEEL_DIAMETER = 52
AXLE_TRACK = 166
robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
#robot.settings(1000,100,90,45)
#settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)

def turnRight():
    robot.turn(-45)

def turnLeft():
    robot.turn(45)

def moveForward():
    robot.straight(-GRID_DISTANCE)

def moveForwardCross():
    robot.straight(-GRID_DISTANCE*1.414)

def moveBackward():
    robot.straight(100)

def moveToNeighbor(target : Heading , currentHeading: Heading):
    while currentHeading != target:
        if currentHeading < target:
            turnRight()
            currentHeading = currentHeading + 1
        else:
            turnLeft()
            currentHeading = currentHeading - 1
    if target % 2 == 0:
        moveForwardCross()
    else:
        moveForward()
    return currentHeading


def moveToPoint(x: int, y: int, currentX: int, currentY: int, currentHeading: Heading):
    while currentX != x or currentY != y:
        if x > currentX:
            if y > currentY:
                currentHeading = moveToNeighbor(Heading.NORTHEAST, currentHeading)
                currentX += 1
                currentY += 1
            elif y < currentY:
                currentHeading = moveToNeighbor(Heading.SOUTHEAST, currentHeading)
                currentX += 1
                currentY -= 1
            else:
                currentHeading = moveToNeighbor(Heading.EAST, currentHeading)
                currentX += 1
        elif x < currentX:
            if y > currentY:
                currentHeading = moveToNeighbor(Heading.NORTHWEST, currentHeading)
                currentX -= 1
                currentY += 1
            elif y < currentY:
                currentHeading = moveToNeighbor(Heading.SOUTHWEST, currentHeading)
                currentX -= 1
                currentY -= 1
            else:
                currentHeading = moveToNeighbor(Heading.WEST, currentHeading)
                currentX -= 1
        else:
            if y > currentY:
                currentHeading = moveToNeighbor(Heading.NORTH, currentHeading)
                currentY += 1
            elif y < currentY:
                currentHeading = moveToNeighbor(Heading.SOUTH, currentHeading)
                currentY -= 1
        print("ran")
    return currentHeading



while True:
    # Establish a connection
    clientsocket,addr = serversocket.accept()
    
    # Receive the command
    command = clientsocket.recv(1024).decode('utf-8')
    
    if command == 'MOVE':
        # Code to move the robot forward
        # Go forward for one meter.

        path = PathfindingAlgorithm.a_star(grid, start, end)

        node = path[1]

        newHeading = moveToPoint(node.x, node.y, currentX, currentY, NORTH)

        for node in path:
            newHeading = movetoPoint(node.x, node.y, currentX, currentY, newHeading)


        print(node.x, node.y)

        #for node in path:
        #    moveToPoint((node.x, node.y))
        #    print(node.x, node.y)
        pass

    clientsocket.close()