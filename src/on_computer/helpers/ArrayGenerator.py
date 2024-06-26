import numpy as np

def create_border_array(x, y, thickness):
    # Initialize the array with zeros
    array = np.zeros((y, x), dtype=int)
    
    # Set the border with 1's
    array[:thickness, :] = 1  # Top border
    array[-thickness:, :] = 1  # Bottom border
    array[:, :thickness] = 1  # Left border
    array[:, -thickness:] = 1  # Right border
    
    return array

# Define the dimensions and thickness
x = 260
y = 140
thickness = 12

# Create the array
border_array = create_border_array(x, y, thickness)

np.savetxt("border_array.txt", border_array, fmt='%d')