import numpy as np

# # Find the coordinates of the goals in the grid based on the position of the walls
# # Returns a list of tuples [0]=west goal, [1]=east goal
# def find_goal_coordinates(grid):
#     # Find the number of rows and columns in the grid
#     # print('GRID:', grid[0][0])
#     num_rows = len(grid)
#     num_cols = len(grid[0]) if num_rows > 0 else 0

#     # Calculate the middle row index
#     middle_row = num_rows // 2

#     # Initialize variables to store the indices of the first and last '1' in the middle row
#     first_wall_index = -1
#     last_wall_index = -1

#     # Find the first and last '1' in the middle row
#     for col in range(num_cols):
#         if grid[middle_row][col] == 1:
#             if first_wall_index == -1:
#                 first_wall_index = col
#             last_wall_index = col

#     # Check if both wall indices are found
#     if first_wall_index != -1 and last_wall_index != -1:
#         # Return the coordinates of the goals
#         # print('WE MADE IT!')
#         return [(middle_row, first_wall_index), (middle_row, last_wall_index)]
#     else:
#         # Return None if walls are not found
#         # print('NO GOALS FOUND!')
#         return None

# Example usage

# grid = [
#     [1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1],
#     [0, 1, 0, 0, 1],
#     [0, 0, 1, 0, 1],
#     [0, 0, 1, 1, 1]
# ]

# grid = convert_to_grid(grid)

# goal_coordinates = find_goal_coordinates(grid)
# print(goal_coordinates)  # Output should be [(2, 0), (2, 2)]



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

# Example usage
# grid = [
#     [1, 1, 1, 0, 0],
#     [1, 0, 0, 1, 1],
#     [0, 1, 0, 0, 1],
#     [0, 1, 1, 0, 1],
#     [0, 0, 1, 1, 1]
# ]
# start_pos, end_pos = find_edges_in_middle_row_of_ones(grid)
# print(f"Start position: {start_pos}, End position: {end_pos}")