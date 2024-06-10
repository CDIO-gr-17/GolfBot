import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end, Node
import json
from computer_vision.ComputerVision import get_grid



raw_grid_data = get_grid()

def convert_to_grid(data):
    rows = len(data)
    cols = len(data[0])
    grid = []

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

def get_ball_position(data):
    rows = len(data)
    cols = len(data[0])

    for i in range(rows):
        for j in range(cols):
            if data[i][j] == 2:
                return grid[i][j] # Skal jeg returnere convert_to_grid(data)[i][j] i stedet?

    return None # No ball found

start_node = grid[2][2]

# Get this from the computer vision of the balls
end_node = get_ball_position(raw_grid_data)

print(raw_grid_data)
path = PathfindingAlgorithm.a_star(grid, start_node, end_node)
print(path)
print("Start: ", start_node.x, start_node.y, "End: ", end_node.x, end_node.y)
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
path_as_json = json.dumps(path_as_dictionaries)

print(path_as_dictionaries)
