import socket
import PathfindingAlgorithm
from PathfindingAlgorithm import grid, start, end, Node
import json

path = PathfindingAlgorithm.a_star(grid, start, end)

path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]

path_json = json.dumps(path_as_dictionaries)

path_from_json = json.loads(path_json)



print(path_from_json[0].)