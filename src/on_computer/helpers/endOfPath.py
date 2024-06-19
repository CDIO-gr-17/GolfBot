

def run_pickup(robot_pos, end_node): #Function for picking up the ball, when it has reached the end of the path
    print('ball is close')
    command = 'PICK'
    client_socket.sendall(command.encode('utf-8'))
    #calculate heading from robot, to ball, to send
    new_heading = str(calculate_heading(robot_pos,end_node))
    client_socket.sendall(new_heading.encode('utf-8'))
    distance = str(distance_between(robot_pos, end_node))
    client_socket.sendall(distance.encode('utf-8'))

def score_balls():
    command = 'DEPO'
    client_socket.sendall(command.encode('utf-8')) #sends DEPO command to robot
    masks = get_masks_from_camera()
    raw_grid_data = get_grid(masks['red'], masks['orange'], masks['white'])
    grid = convert_to_grid(raw_grid_data)
    path = get_path_to_goal(grid,masks['green']) #gets path to goal, from a new grid.
    path_as_dictionaries = [{'x': node.x, 'y': node.y} for node in path]
    path_as_json = json.dumps(path_as_dictionaries)
    json_length = len(path_as_json)
    client_socket.sendall(json_length.to_bytes(4, 'big'))
    client_socket.sendall(path_as_json.encode('utf-8'))
    counter = 0