class Heading():
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8

    heading_to_degrees = {
            NORTH: 0,
            NORTHEAST: 45,
            EAST: 90,
            SOUTHEAST: 135,
            SOUTH: 180,
            SOUTHWEST: 225,
            WEST: 270,
            NORTHWEST: 315
        }

        degrees_to_heading = {v: k for k, v in heading_to_degrees.items()}