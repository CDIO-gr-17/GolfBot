from Displacement import find_displacement_of_robot, find_angle_from_centre_to_robot, find_middle, find_angle_to_field
import numpy as np
import math


def get_robot_position(initial_position:tuple):
    resolution = (int(300), int(170))
    grid = np.zeros(resolution) #Def should take a grid as argument
    #blue_square = (0,1)
    #green_square = (0,0)
    #theta = find_angle_to_field(grid, green_square)
    angle = find_angle_from_centre_to_robot(grid, initial_position)
    displacement = find_displacement_of_robot(grid, initial_position)
    x_displacement = displacement * math.cos(angle)
    y_displacement = displacement * math.sin(angle) 
    final_position = (initial_position[0]+x_displacement,initial_position[1]+ y_displacement)

    
    #pos = tuple(x + displacement for x in initial_position[0])
    #temppos = initial_position[0]+displacement
    #initial_position = (temppos,) + initial_position[1:]
    #pos = initial_position
  
 #   if (initial_position is righUpperCorner):

  #  if(initial_position is leftUpperCorner):

   # if (initial_position is leftLowerCorner):
   #Kig i moveToNeighbour
    
    return final_position
print (get_robot_position((170,150)))



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