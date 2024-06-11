import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, Node
import json
from ArrayGenerator import create_border_array
#from computer_vision.ComputerVision import get_grid

raw_grid_data = create_border_array(260, 140, 12)

def convert_to_grid(data):
    rows = len(data)
    cols = len(data[0])
    grid = []

    print(rows)
    print(cols)

    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            element = data[i][j]
            if element == 1:
                node.type = 'wall'
            elif element == 0:
                node.type = 'road'
            row_nodes.append(node)
        grid.append(row_nodes)

    return grid

grid = convert_to_grid(raw_grid_data)

# below, y is first and x is second as the grid is a matrix not a cartesian plane

start_node = grid[70][130]
end_node = grid[70][238]

#Creates a socket object, and established a connection to the robot

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.8.111"
port = 9999

client_socket.connect((host, port))

command = 'PATH'
client_socket.sendall(command.encode('utf-8'))

# Send the path to the robot
path = PathfindingAlgorithm.a_star(grid, start_node, end_node)
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
path_as_json = json.dumps(path_as_dictionaries)

print(path_as_dictionaries)


json_length = len(path_as_json)
client_socket.sendall(json_length.to_bytes(4, 'big'))

client_socket.sendall(path_as_json.encode('utf-8'))

# Close the connection
client_socket.close()
