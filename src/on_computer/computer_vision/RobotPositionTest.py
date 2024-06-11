from Displacement import find_displacement_of_robot, find_distance_from_middle, find_middle, find_angle_to_field
import numpy as np


def get_robot_position(blue_square, green_square):
    heading = 'UNKNOWN'
    resolution = (int(300), int(170))
    grid = np.zeros(resolution)
    #blue_square = (0,1)
    #green_square = (0,0)
    middle = find_middle(grid)
    theta = find_angle_to_field(grid, green_square)
    
    pos_without_displacement = (green_square)
    displacement = find_displacement_of_robot(grid, pos_without_displacement)
    #pos = tuple(x + displacement for x in pos_without_displacement[0])
    if (pos_without_displacement):
        temppos = pos_without_displacement[0]+displacement
        pos_without_displacement = (temppos,) + pos_without_displacement[1:]
        pos = pos_without_displacement
  
 #   if (pos_without_displacement is righUpperCorner):

  #  if(pos_without_displacement is leftUpperCorner):

   # if (pos_without_displacement is leftLowerCorner):
   #Kig i moveToNeighbour
    
    return pos
print (get_robot_position((0,1),(0,0)))



def get_robot_direction():
    heading = 'UNKNOWN'
  #write_pixel_grid(mask_red, mask_orange, mask_white, mask_green, mask_grid)
    blue_square = (0,1)
    green_square = (0,0)
    if (blue_square[1] > green_square[1]):  
        heading = 'NORTH'
    if (blue_square[0] < green_square[0]): 
        heading = 'EAST' 
    if (blue_square[1]< green_square[1]):
        heading = 'SOUTH'
    if (blue_square[0] > green_square[0]):
        heading = 'WEST'
    
    pos = (green_square , heading)
    return pos

#print (get_robot_position_and_heading())