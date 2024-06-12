def is_robot_position_correct(robot_path, camera_robot_position):
        if(camera_robot_position in robot_path):
            robot_path.remove(camera_robot_position) # Kan jeg fjerne et element fra robot_path sådan her?
            if len(robot_path) == 0:
                return True
        else:
            return False