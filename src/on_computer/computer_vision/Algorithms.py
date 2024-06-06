import numpy as np

def ball_detector(grid):
  """
  Identifies clusters of ones in a 2D grid and counts the number of balls.

  Args:
      grid: A 2D numpy array representing the grid (0s and 1s).

  Returns:
      The number of balls (clusters) found in the grid.
  """

  rows, cols = grid.shape
  visited = np.zeros_like(grid, dtype=bool)  # Keep track of visited cells
  ball_count = 0

  for i in range(rows):
    for j in range(cols):
      if grid[i, j] == 1 and not visited[i, j]:
        # Found a new ball (unvisited 1)
        ball_count += 1

        # Use a stack for iterative exploration
        stack = [(i, j)]
        while stack:
          row, col = stack.pop()
          visited[row, col] = True

          # Explore neighbors (up, down, left, right) within grid boundaries
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1] and grid[new_row, new_col] == 1 and not visited[new_row, new_col]:
              stack.append((new_row, new_col))  # Add neighbor to stack for exploration

  return ball_count

def dfs(grid, visited, row, col):
  """
  Performs Depth-First Search to explore a cluster of connected ones.

  Args:
      grid: The 2D grid.
      visited: A boolean array to track visited cells.
      row: The current row index.
      col: The current column index.
  """

  # Mark current cell as visited
  visited[row, col] = True

  # Explore neighbors (up, down, left, right) within grid boundaries
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    new_row, new_col = row + dr, col + dc
    if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1] and grid[new_row, new_col] == 1 and not visited[new_row, new_col]:
      dfs(grid, visited, new_row, new_col)  # Recursive call for neighbor
