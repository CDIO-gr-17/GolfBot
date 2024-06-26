from pathfinding.PathfindingAlgorithm import Node


def convert_to_grid(data):
    rows = len(data)
    cols = len(data[0])
    grid = []

    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            element = data[i][j]
            if element == 1:
                node.type = 'wall'
            elif element == 0:
                node.type = 'road'
            elif element == 2:
                node.type = 'ball'
            row_nodes.append(node)
        grid.append(row_nodes)

    return grid
