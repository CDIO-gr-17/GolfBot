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

start_node = grid[2][2]

end_node = grid[7][7]

print(raw_grid_data)
print("1")
path = PathfindingAlgorithm.a_star(grid, start_node, end_node)
print(path)
print("2")
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
print("3")
path_as_json = json.dumps(path_as_dictionaries)
print("4")

print(path_as_dictionaries)
