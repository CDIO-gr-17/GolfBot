def is_robot_position_correct(robot_path, camera_robot_position):

    slacked_path = []
    for node in robot_path:
        slacked_path.append((node.x, node.y))
        slacked_path.append((node.x+1, node.y+1))
        slacked_path.append((node.x+1, node.y-1))
        slacked_path.append((node.x-1, node.y+1))
        slacked_path.append((node.x-1, node.y-1))
        slacked_path.append((node.x, node.y+1))
        slacked_path.append((node.x, node.y-1))
        slacked_path.append((node.x+1, node.y))
        slacked_path.append((node.x-1, node.y))
        slacked_path.append((node.x+2, node.y+2))
        slacked_path.append((node.x+2, node.y-2))
        slacked_path.append((node.x-2, node.y+2))
        slacked_path.append((node.x-2, node.y-2))
        slacked_path.append((node.x-1, node.y+2))
        slacked_path.append((node.x+1, node.y-2))
        slacked_path.append((node.x+2, node.y))
        slacked_path.append((node.x-2, node.y))
    
    print ('The position is: ', camera_robot_position)
    print(slacked_path)

    if(camera_robot_position.x in slacked_path and camera_robot_position.y in slacked_path):
        print('Robot position is within margin of error')
        return True
    else:
        return False

def remove_position_from_path(robot_path, camera_robot_position):
    temp_path = robot_path
    result = is_robot_position_correct(temp_path, camera_robot_position)
    if result:
        robot_path.remove(camera_robot_position)
        print("Robot position removed from path")
        return True
    else:
        print("Robot position not found in path")
        return False