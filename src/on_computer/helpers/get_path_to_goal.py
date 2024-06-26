import copy
from pathfinding.PathfindingAlgorithm import a_star
import Globals as G
from positions.Goals import find_goal_coordinates


def get_path_to_goal():
    goal = find_goal_coordinates(G.GRID_DATA)
    if goal is None:
        print("goal is none")
        return None  # maybe do something else as failsafe here
    goal_coordinates = goal[1]
    adjusted_goal = (goal_coordinates[0], goal_coordinates[1] - 60)  # Adjust the goal coordinates later to fit grid
    print('THE GOAL COORDINATES ARE: ', adjusted_goal)
    if G.GRID is None:
        print('GRID IS NONE')
        return None
    grid_copy = copy.deepcopy(G.GRID)  # Taking snapshot of the grid | Taking long time to run
    end_node_copy = grid_copy[adjusted_goal[0]][adjusted_goal[1]]
    start_node_copy = grid_copy[G.ROBOT_POSITION[1]][G.ROBOT_POSITION[0]]
    path = a_star(grid_copy, start_node_copy, end_node_copy)
    return path
