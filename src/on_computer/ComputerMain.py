import socket, json
from sys import orig_argv
from computer_vision.ComputerVision import get_masks_from_camera
from pathfinding.PathfindingAlgorithm import grid, a_star
from positions.Positions import find_start_node, find_first_ball

# below, y is first and x is second as the grid is a matrix not a cartesian plane

start_node = find_start_node()# Function for diffing the calculated robot position with the camera robot position

end_node = find_first_ball(grid)

# Here handling the case where robot or ball is not found
if start_node is None or end_node is None:
    exit()

print(start_node.x, start_node.y)
print(end_node.x, end_node.y)

#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

command = 'PATH'
client_socket.sendall(command.encode('utf-8'))

# Send the path to the robot
path = a_star(grid, start_node, end_node)
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
path_as_json = json.dumps(path_as_dictionaries)

#print(path_as_dictionaries)


json_length = len(path_as_json)
client_socket.sendall(json_length.to_bytes(4, 'big'))

client_socket.sendall(path_as_json.encode('utf-8'))

# Close the connection
client_socket.close()
