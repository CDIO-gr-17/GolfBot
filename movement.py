#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.ev3devices import Motor  # Added import statement
from enum import Enum

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


class Heading(Enum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8



# Create your objects here.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
robot.settings()
#settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)


def turnRight():
    robot.turn(45)

def turnLeft():
    robot.turn(-45)

def moveForward():
    robot.straight(100)

def moveBackward():
    robot.straight(-100)
    robot.stop()


def moveToNeighbor(target : Heading , currentHeading : Heading):
    while currentHeading != target:
        if currentHeading < target:
            turnRight()
            currentHeading = currentHeading + 1  # Fixed variable name
        else:
            turnLeft()
            currentHeading = currentHeading - 1  # Fixed variable name
    moveForward()