from ComputerMain import GRID, ROBOT_POSITION

def find_start_node():
    if GRID is None or ROBOT_POSITION is None:
        return None
    start_node = GRID[ROBOT_POSITION[1]][ROBOT_POSITION[0]]
    return start_node

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None