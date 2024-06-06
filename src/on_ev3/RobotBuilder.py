from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import Heading
import math

class Robot:

    # Initialize the EV3 Brick.
    ev3 = EV3Brick()

    # Initialize the motors.
    left_motor = Motor(Port.D)
    right_motor = Motor(Port.A)

    # Initialize the drive base.
    WHEEL_DIAMETER = 55
    AXLE_TRACK = 95
    robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
    #robot.settings(1000,100,90,45)
    #settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)

    GRID_DISTANCE = 50

    def turnRight():
        robot.turn(45)

    def turnLeft():
        robot.turn(-45)

    def moveForward():
        robot.straight(GRID_DISTANCE)

    def moveForwardCross():
        robot.straight(GRID_DISTANCE*1.414)

    def moveBackward():
        robot.straight(-100)

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
                    currentHeading = moveToNeighbor(Heading.SOUTHEAST, currentHeading)
                    currentX += 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = moveToNeighbor(Heading.NORTHEAST, currentHeading)
                    currentX += 1
                    currentY -= 1
                else:
                    currentHeading = moveToNeighbor(Heading.EAST, currentHeading)
                    currentX += 1
            elif x < currentX:
                if y > currentY:
                    currentHeading = moveToNeighbor(Heading.SOUTHWEST, currentHeading)
                    currentX -= 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = moveToNeighbor(Heading.NORTHWEST, currentHeading)
                    currentX -= 1
                    currentY -= 1
                else:
                    currentHeading = moveToNeighbor(Heading.WEST, currentHeading)
                    currentX -= 1
            else:
                if y > currentY:
                    currentHeading = moveToNeighbor(Heading.SOUTH, currentHeading)
                    currentY += 1
                elif y < currentY:
                    currentHeading = moveToNeighbor(Heading.NORTH, currentHeading)
                    currentY -= 1
            print("ran")
        return currentHeading