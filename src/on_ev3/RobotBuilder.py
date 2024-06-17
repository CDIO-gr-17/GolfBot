import math
import socket
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

from Heading import Heading


def calculate_heading(current_position, next_position):
    if next_position == None or current_position == None:
        print("Tail or head is not found")
        return None
    # Calculate differences

    dx = next_position[0] - current_position[0]
    dy = next_position[1] - current_position[1]


    # Calculate the angle in radians from the positive x-axis
    angle_radians = math.atan2(dy, dx)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Adjust the angle so that 0 degrees is north (up), 90 is east, 180 is south, and 270 is west
    heading = (90 + angle_degrees) % 360

    print("the calculated heading: ", heading)

    return heading


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

        self.GRID_DISTANCE = 7.5
        self.current_heading = None 
        self.step = 0

    def get_next_point(self,path):
        if (self.step == len(path)-1):
            nextpoint = [self.step] #fix later?
        else: nextpoint = path[self.step+1]
        return nextpoint

    def get_current_point(self, path):
        currentpoint = path[self.step]
        return currentpoint

    def get_current_point_x(self, path):
        currentpoint = path[self.step][0]
        return currentpoint
        
    def get_current_point_y(self, path):
        currentpoint = path[self.step][1]
        return currentpoint
       
    def calculate_drive_factor(self, heading, path):
        print("")
        print('-------------------------' + ' run of calculate_drive_factor: ' + str(path[self.step]) + '-------------------------')
        print("")
        acc_steps = 0
        loop_counter = self.step
        
        print('current heading in calculate_drive_factor: ' + str(heading))
        curr_pos = path[loop_counter]
        print('current position in calculate_drive_factor: ' + str(curr_pos))
        print('The for loop starts')
        for nex_pos in path:

            if loop_counter == len(path)-1:
                    break
            nex_pos = path[loop_counter+1]
            print('next position in calculate_drive_factor: ' + str(nex_pos))

            calc_heading = calculate_heading(curr_pos, nex_pos)
            print('     if statement starts: if heading (' + str(heading) + ') == new_heading (' + str(heading) + ')')
            print('     heading in calculate_drive_factor: ' + str(heading))
            if(calc_heading == heading):
                print(          'heading: ' + str(heading) + ' == new_heading: ' + str(heading))
                acc_steps += 1
                heading = calc_heading
                curr_pos = nex_pos
                print(          'curr_pos: ' + str(curr_pos) + ' == nex_pos: ' + str(nex_pos))
                if loop_counter == len(path)-1:
                    break
                loop_counter += 1
                self.step += 1
            else: 
                break
        print("")
        print('-------------------------' + ' end of calculate_drive_factor ' + '-------------------------')
        print("")
        
        return acc_steps
        

    def turn(self, degrees):
        self.robot.turn(degrees)
        self.current_heading = (self.current_heading + degrees) % 360
        print('turned ' + str(degrees) + ' degrees')

    def shortest_turn(self, current_degrees, target_degrees):
        delta = (target_degrees - current_degrees) % 360
        print('The calculated delta is: ', delta)
        if delta > 180:
            delta -= 360
        return delta

    def turn_to_heading(self, target_heading):
        turn_degrees = self.shortest_turn(self.current_heading, target_heading)
        self.turn(turn_degrees)
        return target_heading

    def moveForward(self, path):
        factor = self.calculate_drive_factor(self.current_heading, path)
        print('heading right before moveForward: ' + str(self.current_heading))
        self.robot.straight(self.GRID_DISTANCE*factor)
        print('moved forward ' + str(self.GRID_DISTANCE*factor) + ' mm')

    def moveForwardCross(self, path):
        factor = self.calculate_drive_factor(self.current_heading, path)
        print('heading right before moveForward cross: ' + str(self.current_heading))
        self.robot.straight(self.GRID_DISTANCE * 1.414*factor)
        print('moved forward cross ' + str(self.GRID_DISTANCE * 1.414*factor) + ' mm')


    def moveBackward(self):
        self.robot.straight(-100)

    def moveToNeighbor(self, target: Heading, currentHeading: Heading, path):
        print("")
        print('----------------------------- Start of moveToNeighbor for path step ' + str(path[self.step]) + '-----------------------------')
        print("")
        print('current heading in moveToNeighbor before turn_to_heading: ' + str(currentHeading))
        print('target heading in moveToNeighbor before turn_to_heading: ' + str(target))
        if (currentHeading != target):
            
            currentHeading = self.turn_to_heading(target)
            print('current heading in moveToNeighbor after turn_to_heading: ' + str(currentHeading))
            print('target heading in moveToNeighbor after turn_to_heading: ' + str(target))
        
        if target == 45:
            self.moveForwardCross(path) #not pretty but works.
        if target % 90 != 0:
            self.moveForwardCross(path)
        else:
            self.moveForward(path)
        
        print("")
        print('----------------------------- End of moveToNeighbor -----------------------------')
        print("")
        return currentHeading

    def moveToPoint(self, target_x: int, target_y: int, currentX: int, currentY: int, currentHeading: Heading, path):
        print("")
        print('--------------- Start of moveToPoint for path step ' + str(path[self.step]) + '---------------')
        print("")

        print('current heading in moveToPoint: ' + str(currentHeading))
        print('current position in moveToPoint: ' + str(currentX) + ', ' + str(currentY))
        print('target position in moveToPoint: ' + str(target_x) + ', ' + str(target_y))
        
        if currentX != target_x or currentY != target_y:
            if target_x > currentX:
                if target_y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHEAST, currentHeading, path)
                    print('current heading after moveToPoint: ' + str(currentHeading))
                elif target_y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHEAST, currentHeading, path)
             
                    print('current heading after moveToPoint: ' + str(currentHeading))
                else:
                    currentHeading = self.moveToNeighbor(Heading.EAST, currentHeading, path)
                    
                    print('current heading after moveToPoint: ' + str(currentHeading))
            elif target_x < currentX:
                if target_y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTHWEST, currentHeading, path)
                   
                    print('current heading after moveToPoint: ' + str(currentHeading))
                elif target_y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTHWEST, currentHeading, path)
                   
                    print('current heading after moveToPoint: ' + str(currentHeading))
                else:
                    currentHeading = self.moveToNeighbor(Heading.WEST, currentHeading, path)
                    print('current heading after moveToPoint: ' + str(currentHeading))
            else:
                if target_y > currentY:
                    currentHeading = self.moveToNeighbor(Heading.SOUTH, currentHeading, path)
                    print('current heading after moveToPoint: ' + str(currentHeading))
                elif target_y < currentY:
                    currentHeading = self.moveToNeighbor(Heading.NORTH, currentHeading, path)
                    print('current heading after moveToPoint: ' + str(currentHeading))
        
        print("")
        print('--------------- End of moveToPoint for path step ' + str(path[self.step]) +  '---------------')
        print("")
        return currentHeading

    def move_through_path(self, start_node, end_node, current_heading, path, socket):
        path_length = len(path)
        start_x = start_node[0]
        start_y = start_node[1]
        clientsocket = socket

        self.current_heading = current_heading

        while(start_node != end_node):
            print('step before while loop: ' + str(self.step) + 'with node ' + str(path[self.step]))
            print('before ', start_x, ' ' + str(start_y))
            print('before ' + str(path[path_length-1][0]) + ' ' + str(path[path_length-1][1]))
            self.current_heading = self.moveToPoint(path[self.step+1][0], path[self.step+1][1], start_x, start_y, current_heading, path)
            start_node = path[self.step]
            start_x = start_node[0]
            start_y = start_node[1]

            off_course_notice = clientsocket.recv(4).decode('utf-8').strip()
            if off_course_notice == 'STOP':
                checkin = 'STOPPED'
                clientsocket.send(checkin.encode('utf-8'))
                print('Stopped due to drift')
                self.step = 0
                return
        
        



