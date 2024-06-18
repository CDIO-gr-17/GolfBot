import time
import socket, json
from sys import orig_argv
from computer_vision.ComputerVision import get_masks_from_camera, get_grid
from pathfinding.Convert_to_node_grid import convert_to_grid
from pathfinding.feedback import is_robot_position_correct
from pathfinding.PathfindingAlgorithm import a_star
from positions.Positions import find_start_node, find_first_ball, get_robot_angle
from helpers.end_of_path_pickup import distance_between, deegrees_to_heading
from positions.Robot_direction import calculate_heading


#Creates a socket object, and established a connection to the robot
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999
client_socket.connect((host, port))

def run_pickup(robot_pos, end_node):
 print('ball is close')
 command = 'PICK'
 client_socket.sendall(command.encode('utf-8'))
#calculate heading from robot, to ball, to send
 new_heading = str(calculate_heading(robot_pos,end_node))
 client_socket.sendall(new_heading.encode('utf-8'))
 distance = str(distance_between(robot_pos, end_node))
 client_socket.sendall(distance.encode('utf-8'))




counter = 0
while True:
        masks = get_masks_from_camera()
        raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
        grid = convert_to_grid(raw_grid_data)
        robot_position = masks['green']
        robot_heading = get_robot_angle(masks, grid)
        print('The robots heading: ', robot_heading)

        start_node = find_start_node(robot_position, grid)# Function for diffing the calculated robot position with the camera robot position
        end_node = find_first_ball(grid)

        
        
    
        command = 'PATH'
        client_socket.sendall(command.encode('utf-8'))

            # Send the path to the robot
        path = a_star(grid, start_node, end_node)

        if path != None:
            print('Path: OK')
            path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
            path_as_json = json.dumps(path_as_dictionaries)
        else: print('The algorithm could not find a path')

        if robot_heading == None:
            print('ERROR: No heading calcultated')
            exit()
        else:
            heading_as_string = str(robot_heading)
            client_socket.sendall(heading_as_string.encode('utf-8'))

            json_length = len(path_as_json)
            client_socket.sendall(json_length.to_bytes(4, 'big'))

            client_socket.sendall(path_as_json.encode('utf-8'))

        while(is_robot_position_correct(robot_heading, path, start_node)):
            print("correct")
            course_notice = 'KEEP'
            client_socket.sendall(course_notice.encode('utf-8'))
            response = client_socket.recv(7).decode('utf-8').strip()
            print(response)

            if response == 'ONGOING':
                masks = get_masks_from_camera()
                raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
                grid = convert_to_grid(raw_grid_data)
                robot_position = masks['green']
                start_node = find_start_node(robot_position, grid)

            if response == 'HEADING':
                masks = get_masks_from_camera()
                raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
                grid = convert_to_grid(raw_grid_data)
                robot_position = masks['green']
                robot_heading = get_robot_angle(masks, grid)
                client_socket.sendall(str(robot_heading).encode('utf-8'))

            if response == 'PICK':
               # if distance_to_ball <= 13 and counter == ball_array[counter] :
                masks = get_masks_from_camera()
                raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
                grid = convert_to_grid(raw_grid_data)

                robot_pos = masks['green']
                
                run_pickup(robot_pos, end_node)
                #counter += 1
                break



        
        # Send the stop command to the robot
        while True:
            course_notice = 'STOP'
            client_socket.sendall(course_notice.encode('utf-8'))
            response = client_socket.recv(7).decode('utf-8').strip()
            print(response)
            if response == 'STOPPED':
                break
