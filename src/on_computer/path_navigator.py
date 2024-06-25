import math
import time
import Globals as G

from Heading import Heading
from helpers.end_of_path_pickup import distance_between

WHEEL_DIAMETER = 55
AXLE_TRACK = 98

GRID_DISTANCE = 7.5
G.STEP = 0
settings = (1000, 200, 50, 25)


def calculate_heading(current_position, next_position):
    if next_position is None or current_position is None:
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


# Helper function to send the robot instructions on how to move
def send_instruction(instruction, degrees=None, distance=None):
    if degrees is not None:
        degrees = int(degrees)
    if distance is not None:
        distance = int(distance)

    print('sending instruction: ' + instruction)

    match instruction:
        case 'DRIVE':
            payload = f"{instruction} {0} {distance}"
            G.CLIENT_SOCKET.send(payload.encode('utf-8'))
            print("The robot should drive straight for: ", distance)
            if distance:
                timer = distance/GRID_DISTANCE*0.1
            else:
                timer = 1
            time.sleep(timer)
        case 'REVERSE':
            payload = f"{instruction} {0} {distance}"
            G.CLIENT_SOCKET.send(payload.encode('utf-8'))
            time.sleep(1)
        case 'TURN':
            payload = f"{instruction} {degrees} {0}"
            G.CLIENT_SOCKET.send(payload.encode('utf-8'))
            time.sleep(1)
        case 'PICKUP':
            payload = f"{instruction} {degrees} {distance}"
            G.CLIENT_SOCKET.send(payload.encode('utf-8'))
            time.sleep(4)
        case 'EJECT':
            payload = f"{instruction} {degrees} {distance}"
            G.CLIENT_SOCKET.send(payload.encode('utf-8'))
            time.sleep(10)


# def shoot_one_ball(self, distance):
#     robot.front_motor.run(-1200)
#     robot.drivebase.straight(-distance)
#     wait(2000)
#     self.robot.straight(distance)
#     wait(2000)

# def shoot_all_balls(self):
#     self.robot.settings(100, 200)
#     wiggle = 40
#     for i in range(3):
#         self.shoot_one_ball(wiggle)
#         wiggle += 40
#     self.front_motor.stop()

# def deposit(self):
#     goal_heading = 90  # directly east
#     # Send command containing the following:
#     self.turn_to_heading(goal_heading)
#     self.shoot_all_balls()


def pickup_ball(distance, heading):
    send_instruction('PICKUP', heading, distance * GRID_DISTANCE)


def calculate_drive_factor(path):
    print("")
    print('-------------------------' + ' run of calculate_drive_factor: ' + str(path[G.STEP]) + '-------------------------')
    print("")
    acc_steps = 0
    loop_counter = G.STEP

    curr_pos = path[loop_counter]
    for nex_pos in path:
        if loop_counter == len(path)-1:
            break
        nex_pos = path[loop_counter+1]
        calc_heading = calculate_heading(curr_pos, nex_pos)
        if calc_heading < G.ROBOT_HEADING + 10 and calc_heading > G.ROBOT_HEADING - 10:
            acc_steps += 1
            curr_pos = nex_pos
            if loop_counter == len(path)-1:
                break
            loop_counter += 1
            G.STEP += 1
        else:
            break
    print("")
    print('-------------------------' + ' end of calculate_drive_factor ' + '-------------------------')
    print("")

    return acc_steps


def shortest_turn(current_degrees, target_degrees):
    delta = (target_degrees - current_degrees) % 360
    if delta > 180:
        delta -= 360
    return delta


def turn_to_heading(target_heading):
    turn_degrees = shortest_turn(G.ROBOT_HEADING, target_heading)
    send_instruction('TURN', turn_degrees)
    G.ROBOT_HEADING = (G.ROBOT_HEADING + turn_degrees) % 360
    print('turned ' + str(turn_degrees) + ' degrees')
    return target_heading


def moveForward(path):
    factor = calculate_drive_factor(path)
    send_instruction('DRIVE', 0, GRID_DISTANCE * factor)
    print('moved forward ' + str(GRID_DISTANCE) + ' mm')


def moveForwardCross(path):
    factor = calculate_drive_factor(path)
    send_instruction('DRIVE', 0, GRID_DISTANCE * 1.414 * factor)
    print('moved forward cross ' + str(GRID_DISTANCE * 1.414) + ' mm')


def moveBackward():
    send_instruction('REVERSE', None, GRID_DISTANCE)


def moveToNeighbor(target: Heading, currentHeading: Heading, path):
    print('The observed heading is:', G.ROBOT_HEADING)
    if (G.ROBOT_HEADING != target - 10 or G.ROBOT_HEADING != target + 10):
        G.ROBOT_HEADING = turn_to_heading(target)

    if target == 45:
        moveForwardCross(path)  # not pretty but works.
    if target % 90 != 0:
        moveForwardCross(path)
    else:
        moveForward(path)

    print("")
    print('----------------------------- End of moveToNeighbor -----------------------------')
    print("")
    return currentHeading


def moveToPoint(target_x: int, target_y: int, currentX: int, currentY: int, currentHeading: Heading, path):
    if currentX != target_x or currentY != target_y:
        if target_x > currentX:
            if target_y > currentY:
                moveToNeighbor(Heading.SOUTHEAST, G.ROBOT_HEADING, path)
            elif target_y < currentY:
                moveToNeighbor(Heading.NORTHEAST, G.ROBOT_HEADING, path)
            else:
                moveToNeighbor(Heading.EAST, G.ROBOT_HEADING, path)
        elif target_x < currentX:
            if target_y > currentY:
                moveToNeighbor(Heading.SOUTHWEST, G.ROBOT_HEADING, path)
            elif target_y < currentY:
                moveToNeighbor(Heading.NORTHWEST, G.ROBOT_HEADING, path)
            else:
                moveToNeighbor(Heading.WEST, G.ROBOT_HEADING, path)
        else:
            if target_y > currentY:
                moveToNeighbor(Heading.SOUTH, G.ROBOT_HEADING, path)
            elif target_y < currentY:
                moveToNeighbor(Heading.NORTH, G.ROBOT_HEADING, path)

    print("")
    print('--------------- End of moveToPoint for path step ' + str(path[G.STEP]) +  '---------------')
    print("")
    return currentHeading


def move_through_path(start_coordinate, end_coordinate, path, robot_mode):
    start_x = start_coordinate[0]
    start_y = start_coordinate[1]

    while (G.STEP < len(path)):
        moveToPoint(path[G.STEP][0], path[G.STEP][1], start_x, start_y, G.ROBOT_HEADING, path)
        start_node = path[G.STEP]
        start_x = start_node[0]
        start_y = start_node[1]
        G.STEP += 1

        #  if not is_robot_position_correct(path, start_node):
        #  return False

    if robot_mode == 'BALL':
        required_heading = calculate_heading(G.ROBOT_POSITION, end_coordinate)
        distance_to_ball = distance_between(G.ROBOT_POSITION, end_coordinate)

        degrees_delta = required_heading - G.ROBOT_HEADING
        if degrees_delta > 180:
            degrees_delta -= 360

        pickup_ball(distance_to_ball, degrees_delta)
        G.STEP = 0
        return True

    if robot_mode == 'GOAL':
        end_coordinate_as_touple = (end_coordinate[0]+ 70, end_coordinate[1])
        required_heading = calculate_heading(G.ROBOT_POSITION, end_coordinate_as_touple)
        degrees_delta = required_heading - G.ROBOT_HEADING
        if degrees_delta > 180:
            degrees_delta -= 360

        distance = 0
        send_instruction('EJECT', degrees_delta, distance)
        return True