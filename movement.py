#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

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


def moveToNeighbor(neighbor, heading):







def moveToPoint(point):
    # Define the grid size and the distance between grid points
    grid_size = 100  # Assuming each grid is 100 units wide
    distance_between_points = 20  # Assuming 20 units between each grid point

    # Calculate the target position in terms of motor rotations
    target_x = point[0] * distance_between_points
    target_y = point[1] * distance_between_points

    # Create a DriveBase object with the appropriate motor and wheel sizes
    wheel_diameter = 56  # Assuming the wheel diameter is 56 mm
    axle_track = 114  # Assuming the axle track is 114 mm
    robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

    # Calculate the target position in terms of motor rotations
    target_x_rotations = target_x / (wheel_diameter * math.pi)
    target_y_rotations = target_y / (wheel_diameter * math.pi)

    # Move the robot to the target position
    robot.drive(target_x_rotations, target_y_rotations)

# Call the moveToPoint function with the desired point coordinates
moveToPoint((2, 3))
