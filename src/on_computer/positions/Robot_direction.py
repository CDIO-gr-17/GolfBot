import math

def calculate_heading(tail, head):
    if tail == None or head == None:
        print("Tail or head is not found")
        return None
    # Calculate differences

    print(tail[0], tail[1])
    print(head[0], head[1])

    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    print(dx)
    print(dy)

    # Calculate the angle in radians from the positive x-axis
    angle_radians = math.atan2(dy, dx)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Adjust the angle so that 0 degrees is north (up), 90 is east, 180 is south, and 270 is west
    heading = (90 + angle_degrees) % 360

    return heading

