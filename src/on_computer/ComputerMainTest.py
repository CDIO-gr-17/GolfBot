import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end, Node
import json
from computer_vision.ComputerVision import get_grid


grid = get_grid()
print("1")
path = PathfindingAlgorithm.a_star(grid, start, end)
print("2")
path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
print("3")
path_as_json = json.dumps(path_as_dictionaries)
print("4")

print(path_as_dictionaries)
