import numpy as np


# Find the coordinates of the goals in the grid based on the position of the walls
# Returns a list of tuples [0]=west goal, [1]=east goal
def find_goal_coordinates(grid):
    rows_with_ones = []

    # Step 1: Identify all rows that contain `1`
    for row_index, row in enumerate(grid):
        if 1 in row:
            rows_with_ones.append(row_index)

    # Ensure there are rows with `1`s
    if not rows_with_ones:
        return None  # Or handle the case where no `1`s are found

    # Step 2: Find the middle row among these rows
    middle_row_index = rows_with_ones[len(rows_with_ones) // 2]
    middle_row = grid[middle_row_index]

    # Step 3: Within the middle row, find the first and last occurrence of `1`
    first_wall_index = np.where(middle_row == 1)[0][0]  # Correct usage for first_wall_index
    last_wall_index = np.where(middle_row == 1)[0][-1]

    return (middle_row_index, first_wall_index), (middle_row_index, last_wall_index)
