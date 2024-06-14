import numpy as np

# Find the coordinates of the goals in the grid based on the position of the walls
# Returns a list of tuples [0]=west goal, [1]=east goal
def find_goal_coordinates(grid):
    # Find the number of rows and columns in the grid
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    # Calculate the middle row index
    middle_row = num_rows // 2

    # Initialize variables to store the indices of the first and last '1' in the middle row
    first_wall_index = -1
    last_wall_index = -1

    # Find the first and last '1' in the middle row
    for col in range(num_cols):
        if grid[middle_row][col] == 1:
            if first_wall_index == -1:
                first_wall_index = col
            last_wall_index = col

    # Check if both wall indices are found
    if first_wall_index != -1 and last_wall_index != -1:
        # Return the coordinates of the goals
        return [(middle_row, first_wall_index), (middle_row, last_wall_index)]
    else:
        # Return None if walls are not found
        return None

# Example usage
grid = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

goal_coordinates = find_goal_coordinates(grid)
print(goal_coordinates)  # Output should be [(2, 0), (2, 2)]
