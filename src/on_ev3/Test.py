import math
def move_robot_smoothly(path, heading, robot):
    i = 0
    while i < len(path) - 1:
        current_position = path[i]
        next_position = path[i + 1]

        # Calculate the necessary heading to move to the next position
        necessary_heading = calculate_heading(current_position, next_position)

        # If the necessary heading is the same as the current heading, count the number of consecutive cells with the same heading
        if necessary_heading == heading:
            steps = 1
            while i + steps < len(path) - 1:
                next_next_position = path[i + steps + 1]
                next_necessary_heading = calculate_heading(next_position, next_next_position)
                if next_necessary_heading == necessary_heading:
                    steps += 1
                    next_position = next_next_position
                else:
                    break

            # Move the robot forward by the number of steps
            distance =
            robot.move_forward(steps)
            i += steps
        else:
            # Calculate the difference in heading
            heading_difference = necessary_heading - heading

            # Turn the robot to the necessary heading
            robot.turn(heading_difference)

            # Move the robot forward
            robot.move_forward()

            i += 1

        # Update the current heading
        heading = necessary_heading



def calculate_heading(current_position, next_position):
    dx = next_position[0] - current_position[0]
    dy = next_position[1] - current_position[1]

    # Calculate the heading in degrees
    heading = math.degrees(math.atan2(dy, dx))

    # Normalize the heading to be between 0 and 359
    heading = (heading + 360) % 360

    return heading