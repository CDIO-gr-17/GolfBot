import json
from RobotController import RobotController
from EV3Connector import establish_socket
from .on_computer.pathfinding.PathfindingAlgorithm import a_star

#socket = establish_socket()

def test_handle_command():
    # Create a RobotController instance
    #r = RobotController(socket)

    # Define a command and a path
    command = 'PATH'
    path = a_star(1,1,2,2)
    path_as_tuples = [(node.x, node.y) for node in path]

    #path_as_tuples = ((1,1),(2,2))

    # Convert the path to a JSON string
    path_as_json = json.dumps(path_as_tuples)
    print (path_as_json)

    path_as_tuples = json.loads(path_as_json)
    print (path_as_tuples)

    # Handle the command
    print (RobotController.handle_command(command, path_as_json))

    # Verify that the path was correctly converted to a list of tuples
    #assert r.robot.path == list(path_as_tuples), "Path was not correctly converted to a list of tuples"

# Run the test
test_handle_command()