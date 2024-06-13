from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from Heading import Heading

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
        self.AXLE_TRACK = 110
        self.robot = DriveBase(self.left_motor, self.right_motor, self.WHEEL_DIAMETER, self.AXLE_TRACK)

        self.GRID_DISTANCE = 13
        self.current_heading_degrees = 0 

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

    def moveToNeighbor(self, target: Heading, currentHeading: Heading):
        while currentHeading != target:
            if currentHeading < target:
                self.turnRight()
                currentHeading = currentHeading + 1
            else:
                self.turnLeft()
                currentHeading = currentHeading - 1
        if target % 2 == 0:
            self.moveForwardCross()
        else:
            self.moveForward()
        return currentHeading

    def moveToPoint(self, x: int, y: int, currentX: int, currentY: int, currentHeading: Heading):
        while currentX != x or currentY != y:
            if x > currentX:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHEAST, currentHeading)
                    currentX += 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHEAST, currentHeading)
                    currentX += 1
                    currentY -= 1
                else:
                    currentHeading = self.moveToNeighbor(Heading.EAST, currentHeading)
                    currentX += 1
            elif x < currentX:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHWEST, currentHeading)
                    currentX -= 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHWEST, currentHeading)
                    currentX -= 1
                    currentY -= 1
                else:
                    currentHeading = self.moveToNeighbor(Heading.WEST, currentHeading)
                    currentX -= 1
            else:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTH, currentHeading)
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTH, currentHeading)
                    currentY -= 1
            print("ran")
        return currentHeading