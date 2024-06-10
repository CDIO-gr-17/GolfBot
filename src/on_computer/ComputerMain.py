import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, Node
import json
from computer_vision.ComputerVision import get_grid

raw_grid_data = get_grid()
index = ()
ball_node = PathfindingAlgorithm.node
end_node = type(Node)
def convert_to_grid(data):
    rows = len(data[0])
    cols = len(data)
    grid = []
    print(rows)
    print(cols)

    for i in range(cols):
        row_nodes = []
        for j in range(rows):
            node = Node(grid, i, j)
            element = data[i][j]
            if element == 1:
                node.type = 'wall'
            elif element == 0:
                node.type = 'road'
            elif element == 2:
                node.type = 'road'
                ball_node.x = i
                ball_node.y = j
            row_nodes.append(node)
        grid.append(row_nodes)

    

    return grid

grid = convert_to_grid(raw_grid_data)

start_node = grid[36][83]
end_node = grid[ball_node.x][ball_node.y]
print(end_node.x, end_node.y)
print(ball_node.x, ball_node.y)

# Get this from the computer vision of the balls
#end_node = get_ball_position(grid)

print("Start: ", start_node.x, start_node.y, "End: ", end_node.x, end_node.y)

# Creates a socket object, and established a connection to the robot
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
