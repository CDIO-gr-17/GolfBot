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
        if (self.step == len(path)-1):
            nextpoint = [self.step] #fix later?
        else: nextpoint = path[self.step+1]
        return nextpoint

    def get_current_point(self, path):
        currentpoint = path[self.step]
        return currentpoint


    #def calculate_drive_factor(self, path):
    #    tempfactor = self.factor
    #    print ('-------------------------' + ' run of calculate_drive_factor ' + '-------------------------')
    #    print ('step in path: ' + str(self.step))
    #    print ('factor: ' + str(tempfactor))
    #    print('current point: ' + str(self.get_current_point(path)))
    #    print('next point: ' + str(self.get_next_point(path)))
        # prev_point = self.get_prev_point(path)
    #    current_point = self.get_current_point(path)
    #    next_point = self.get_next_point(path)
        # prev_heading = calculate_heading(prev_point, current_point)
    #    next_heading = calculate_heading(current_point, next_point)
    #    print ('self heading' + str(self.current_heading_degrees))
    #    print ('next heading' + str(next_heading))

    #   if(self.current_heading_degrees == next_heading):
    #        self.step+=1
    #        self.factor+=1
    #        self.calculate_drive_factor(path)
    #    self.step+=1
    #    self.current_heading_degrees = next_heading
        
    #    return tempfactor
       
    def calculate_drive_factor(self, heading, path):
        print("")
        print('-------------------------' + ' run of calculate_drive_factor: ' + str(path[self.step]) + '-------------------------')
        print("")
        acc_steps = 1
        new_heading = self.current_heading_degrees
        print('current heading in calculate_drive_factor: ' + str(heading))
        curr_pos = path[self.step]
        print('current position in calculate_drive_factor: ' + str(curr_pos))
        print('for loop starts')
        
        for nex_pos in path:
            nex_pos = path[self.step+1]
            heading = calculate_heading(nex_pos, curr_pos)
            print('     next position in calculate_drive_factor: ' + str(nex_pos))
            print('     heading in calculate_drive_factor: ' + str(heading))
            print('     if statement starts')
            if(heading == new_heading):
                print(          'heading: ' + str(heading) + ' == new_heading: ' + str(new_heading))
                acc_steps += 1
                new_heading = heading
                curr_pos = nex_pos
                print(          'curr_pos: ' + str(curr_pos) + ' == nex_pos: ' + str(nex_pos))
            else: 
                break
        print("")
        print('-------------------------' + ' end of calculate_drive_factor ' + '-------------------------')
        print("")
        
        return acc_steps
        

    def turn(self, degrees):
        self.robot.turn(degrees)
        self.current_heading_degrees = (self.current_heading_degrees + degrees) % 360
        print('turned ' + str(degrees) + ' degrees')

    def shortest_turn(self, current_degrees, target_degrees):
        delta = (target_degrees - current_degrees) % 360
        if delta > 180:
            delta -= 360
        return delta

    def turn_to_heading(self, target_heading):
        target_degrees = target_heading
        turn_degrees = self.shortest_turn(self.current_heading_degrees, target_degrees)
        self.turn(turn_degrees)
        return target_heading

    

    def moveForward(self, path):
        factor = self.calculate_drive_factor(self.current_heading_degrees, path)
        print('heading right before moveForward: ' + str(self.current_heading_degrees))
        self.robot.straight(self.GRID_DISTANCE*factor)
        print('moved forward ' + str(self.GRID_DISTANCE*factor) + ' cm')

    def moveForwardCross(self, path):
        factor = self.calculate_drive_factor(path)
        print('heading right before moveForward cross: ' + str(self.current_heading_degrees))
        self.robot.straight(self.GRID_DISTANCE * 1.414*factor)
        print('moved forward cross ' + str(self.GRID_DISTANCE * 1.414*factor) + ' cm')


    def moveBackward(self):
        self.robot.straight(-100)

    def moveToNeighbor(self, target: Heading, currentHeading: Heading, path):
        print("")
        print('----------------------------- Start of moveToNeighbor for path step ' + str(path[self.step]) + '-----------------------------')
        print("")
        if (currentHeading != target):
            print('current heading in moveToNeighbor before turn_to_heading: ' + str(currentHeading))
            print('target heading in moveToNeighbor before turn_to_heading: ' + str(target))
            currentHeading = self.turn_to_heading(target)
            print('current heading in moveToNeighbor after turn_to_heading: ' + str(currentHeading))
            print('target heading in moveToNeighbor after turn_to_heading: ' + str(target))
        
       # while currentHeading != target:
        #    if currentHeading < target:
        #        self.turnRight()
         #       currentHeading = currentHeading + 1
          #  else:
           #     self.turnLeft()
            #    currentHeading = currentHeading - 1
        if target == 45:
            self.moveForwardCross(path) #not pretty but works.
        if target % 90 != 0:
            self.moveForwardCross(path)
        else:
            self.moveForward(path)
        self.step += 1
        print("")
        print('----------------------------- End of moveToNeighbor -----------------------------')
        print("")
        return currentHeading

    def moveToPoint(self, x: int, y: int, currentX: int, currentY: int, currentHeading: Heading, path):
        while currentX != x or currentY != y:
            if x > currentX:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHEAST, currentHeading, path)
                    currentX += 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHEAST, currentHeading, path)
                    currentX += 1
                    currentY -= 1
                else:
                    currentHeading = self.moveToNeighbor(Heading.EAST, currentHeading, path)
                    currentX += 1
            elif x < currentX:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHWEST, currentHeading, path)
                    currentX -= 1
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHWEST, currentHeading, path)
                    currentX -= 1
                    currentY -= 1
                else:
                    currentHeading = self.moveToNeighbor(Heading.WEST, currentHeading, path)
                    currentX -= 1
            else:
                if y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTH, currentHeading, path)
                    currentY += 1
                elif y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTH, currentHeading, path)
                    currentY -= 1

        return currentHeading



