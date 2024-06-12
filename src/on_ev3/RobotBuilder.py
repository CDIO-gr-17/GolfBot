from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from Heading import Heading
import time

class Robot:

    # Initialize the EV3 Brick.
    def __init__(self):
        self.ev3 = EV3Brick()

        # Initialize the motors.
        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.A)
        #self.front_motor = Motor(Port.C)

        # Initialize the drive base.
        self.WHEEL_DIAMETER = 55
        self.AXLE_TRACK = 140
        self.robot = DriveBase(self.left_motor, self.right_motor, self.WHEEL_DIAMETER, self.AXLE_TRACK)

        self.GRID_DISTANCE = 13
        self.current_heading_degrees = 0  # Initialize current heading in degrees

    def turn(self, degrees):
        self.robot.turn(degrees)
        self.current_heading_degrees = (self.current_heading_degrees + degrees) % 360

    def turn_to_heading(self, target_heading):
        target_degrees = target_heading
        turn_degrees = self.shortest_turn(self.current_heading_degrees, target_degrees)
        self.turn(turn_degrees)

    def shortest_turn(self, current_degrees, target_degrees):
        delta = (target_degrees - current_degrees) % 360
        if delta > 180:
            delta -= 360
        return delta

    def moveForward(self):
        self.robot.straight(self.GRID_DISTANCE)

    def moveForwardCross(self):
        self.robot.straight(self.GRID_DISTANCE * 1.414)

    def moveBackward(self):
        self.robot.straight(-100)

    def moveToNeighbor(self, target_heading):
        self.turn_to_heading(target_heading)
        if target_heading % 2 == 0:
            self.moveForwardCross()
        else:
            self.moveForward()

    def moveToPoint(self, x, y, currentX, currentY):
        while currentX != x or currentY != y:
            if x > currentX:
                if y > currentY:
                    self.moveToNeighbor(Heading.SOUTHEAST)
                    currentX += 1
                    currentY += 1
                elif y < currentY:
                    self.moveToNeighbor(Heading.NORTHEAST)
                    currentX += 1
                    currentY -= 1
                else:
                    self.moveToNeighbor(Heading.EAST)
                    currentX += 1
            elif x < currentX:
                if y > currentY:
                    self.moveToNeighbor(Heading.SOUTHWEST)
                    currentX -= 1
                    currentY += 1
                elif y < currentY:
                    self.moveToNeighbor(Heading.NORTHWEST)
                    currentX -= 1
                    currentY -= 1
                else:
                    self.moveToNeighbor(Heading.WEST)
                    currentX -= 1
            else:
                if y > currentY:
                    self.moveToNeighbor(Heading.SOUTH)
                    currentY += 1
                elif y < currentY:
                    self.moveToNeighbor(Heading.NORTH)
                    currentY -= 1
        return self.current_heading_degrees