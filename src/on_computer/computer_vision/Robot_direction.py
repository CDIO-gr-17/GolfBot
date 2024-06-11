import math

def calculate_heading(tail, head):
    # Calculate differences
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    # Calculate the angle in radians from the positive x-axis
    angle_radians = math.atan2(dy, dx)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    print(angle_degrees)

    # Adjust the angle so that 0 degrees is north (up), 90 is east, 180 is south, and 270 is west
    heading = (90 + angle_degrees) % 360

    return heading

# Example usage
tail = [2, 2]
head = [1,1 ]

heading = calculate_heading(tail, head)
print(heading)  # Output should be 180 (south)
