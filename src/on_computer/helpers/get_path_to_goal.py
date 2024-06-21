

def get_path_to_goal():
    goal = find_goal_coordinates(G.GRID)
    if goal is None:
        return None
    goal_coordinates = goal[1]
    adjusted_goal = (goal_coordinates[0], goal_coordinates[1] - 2) # Adjust the goal coordinates later to fit grid
    path = a_star(G.GRID, G.ROBOT_POSITION, adjusted_goal)       #Maybe need conversion to Nodes
    return path