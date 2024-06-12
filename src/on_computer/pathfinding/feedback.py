def is_robot_position_correct(robot_path, camera_robot_position):
        if(camera_robot_position in robot_path):
            remove_position_from_path(robot_path, camera_robot_position)
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