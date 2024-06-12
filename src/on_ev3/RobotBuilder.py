import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from Heading import Heading
from on_computer.positions.Robot_direction import calculate_heading
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
        self.current_heading_degrees = 0 
        self.step = 0
        self.factor = 1

    def get_next_point(self,path):
        nextpoint = path[self.step+1]
        return nextpoint

    def get_prev_point(self,path):
        if (self.step == 0): #fix later?
            prevpoint = [0]

        if (self.step >=1):
            prevpoint = path[self.step-1]
        return prevpoint

    def get_current_point(self, path):
        currentpoint = path[self.step]
        return currentpoint


    def calculate_drive_factor(self, path):
        print ('-------------------------' + ' run of calculate_drive_factor ' + '-------------------------')
        print ('step in path: ' + str(self.step))
        print ('factor: ' + str(self.factor))
        print('current point: ' + str(self.get_current_point(path)))
        print('next point: ' + str(self.get_next_point(path)))
        # prev_point = self.get_prev_point(path)
        current_point = self.get_current_point(path)
        next_point = self.get_next_point(path)
        # prev_heading = calculate_heading(prev_point, current_point)
        next_heading = calculate_heading(current_point, next_point)
        if(self.current_heading_degrees == next_heading):
            self.step+=1
            self.factor+=1
            self.calculate_drive_factor(path)
        else: self.step+=1
        self.current_heading_degrees = next_heading
        return self.factor
        print('-------------------------')


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

    def moveForward(self, path):
        factor = self.calculate_drive_factor(path)
        self.robot.straight(self.GRID_DISTANCE*factor)
        print('distance driven: ' + str(self.GRID_DISTANCE*factor))

    def moveForwardCross(self):
        self.robot.straight(self.GRID_DISTANCE * 1.414)

    def moveBackward(self):
        self.robot.straight(-100)

    def moveToNeighbor(self, target: Heading, currentHeading: Heading, path):
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
            self.moveForward(path)
        return currentHeading

    def moveToPoint(self, x: int, y: int, currentX: int, currentY: int, currentHeading: Heading, path):
        while currentX != x or currentY != y:
            if x > currentX:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHEAST, currentHeading, path)
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

        return currentHeading



