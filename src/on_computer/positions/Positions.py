import Globals as G
def find_start_node():
    if G.GRID is None or G.ROBOT_POSITION is None:
        return None
    start_node = G.GRID[G.ROBOT_POSITION[1]][G.ROBOT_POSITION[0]]
    return start_node

def find_first_ball(grid):
    for row in grid:
        for node in row:
            if node.type == 'ball':
                return node
    return None