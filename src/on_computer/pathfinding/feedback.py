def is_robot_position_correct(robot_path, camera_robot_position):

    slacked_path = []
    for node in robot_path:
        slacked_path.append((node.x, node.y)) # The node the robot should be on
        slacked_path.append((node.x, node.y-1)) # Directly aboe
        slacked_path.append((node.x, node.y+1)) # Directly below

        slacked_path.append((node.x+1, node.y)) # Directly to the right
        slacked_path.append((node.x+1, node.y-1)) # To the right and above
        slacked_path.append((node.x+1, node.y+1)) # To the right and below

        slacked_path.append((node.x-1, node.y)) # Directly to the left
        slacked_path.append((node.x-1, node.y-1)) # To the left and above
        slacked_path.append((node.x-1, node.y+1)) # To the left and below

    robot_position_coordinates = (camera_robot_position.x, camera_robot_position.y)

    #print ('The position is: ', robot_position_coordinates)
    #print(slacked_path)

    if(robot_position_coordinates in robot_path):
        print('Robot position is within margin of error @', robot_position_coordinates)
        return True
    else:
        return False