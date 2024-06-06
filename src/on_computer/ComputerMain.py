import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end, Node
import json

# Creates a socket object, and established a connection to the robot
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

socket.connect((host, port))

# Send the path to the robot
path = PathfindingAlgorithm.a_star(grid, start, end)
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
path_as_json = json.dumps(path_as_dictionaries)

command = 'PATH'
socket.send(command.encode('utf-8'))
socket.send(path_as_json.encode('utf-8'))

# Close the connection
socket.close()
