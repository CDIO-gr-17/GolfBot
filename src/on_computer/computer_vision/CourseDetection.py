import cv2 as cv
import numpy as np
import Globals as G
from positions.Positions import sort_balls_by_distance

def get_masks_from_frame(frame):

    #Define color ranges
    red_lower_1 = np.array([0, 126, 133], dtype="uint8")
    red_upper_1 = np.array([6, 255, 255], dtype="uint8")

    red_lower_2 = np.array([169, 168, 187], dtype="uint8")
    red_upper_2 = np.array([179, 255, 255], dtype="uint8")

    orange_lower = np.array([10, 102, 203], dtype="uint8")
    orange_upper = np.array([36, 255, 255], dtype="uint8")

    white_lower = np.array([0, 0, 200], dtype="uint8")
    white_upper = np.array([179, 35, 255], dtype="uint8")

    # green_lower = np.array([26, 33, 0], dtype="uint8")
    # green_upper = np.array([78, 255, 255], dtype="uint8")

    # blue_lower = np.array([98, 121, 64], dtype="uint8")
    # blue_upper = np.array([133, 244, 152], dtype="uint8")

    blur_frame = cv.GaussianBlur(frame, (3, 3), 0) #Add blur
    hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV) #Convert from RGB to HSV

    # Create masks for red, green, blue, orange and white
    mask_red_1 = cv.inRange(hsv_frame, red_lower_1, red_upper_1)
    mask_red_2 = cv.inRange(hsv_frame, red_lower_2, red_upper_2)
    mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
    # mask_green = cv.inRange(hsv_frame, green_lower, green_upper)
    # mask_blue = cv.inRange(hsv_frame, blue_lower, blue_upper)
    # mask_robot = cv.bitwise_or(mask_green, mask_blue) #Combine blue and green to see the robot
    mask_orange = cv.inRange(hsv_frame, orange_lower, orange_upper)
    mask_white = cv.inRange(hsv_frame, white_lower, white_upper)
    # mask_ball = cv.bitwise_or(mask_orange, mask_white) #Combine orange and white to see the ball

    #Apply dilation
    obstacle_kernel = np.ones((15, 15), np.uint8)
    ball_kernel = np.ones((3, 3), np.uint8)
    mask_white = cv.dilate(mask_white, ball_kernel)
    mask_orange = cv.dilate(mask_orange, ball_kernel)
    mask_red = cv.dilate(mask_red,obstacle_kernel)
    mask_ball = cv.bitwise_or(mask_orange, mask_white)

    masks = {
        'red': mask_red,
        'balls': mask_ball,
    }

    # cv.imshow('ImageWindow', mask_white)
    # cv.imwrite('frame.jpg', frame)
    # cv.imwrite('mask_white.jpg', mask_white)
    # cv.imwrite('mask_orange.jpg', mask_orange)
    # cv.imwrite('mask_red.jpg', mask_red)
    # path = 'images'
    return masks


def find_clusters(mask):
    amount, labels, stats, _ = cv.connectedComponentsWithStats(mask, connectivity=4)
    clusters = {
        'amount': amount - 1, # Subtract 1 to exclude the background
        #'labels': labels[1:], # Returns an array of the labels of the clusters, but we don't need it for now
        'stats': stats[1:] # Information about each cluster. Used to find the center of each cluster
    }
    return clusters

#Returns a list of centers for each cluster
def find_clusters_center(stats):
    centers = []
    for stat in stats:
        # Calculate the center of the blob
        x = stat[cv.CC_STAT_LEFT] + stat[cv.CC_STAT_WIDTH] // 2
        y = stat[cv.CC_STAT_TOP] + stat[cv.CC_STAT_HEIGHT] // 2
        centers.append((x, y))
    return centers

def filter_clusters_by_size(clusters):
    max_pixels = 30  # Maximum number of pixels in a cluster
    filtered_clusters = {
        'amount': 0,
        'stats': []
    }
    for stat in clusters['stats']:
        area = stat[cv.CC_STAT_AREA]
        if area <= max_pixels:
            filtered_clusters['amount'] += 1
            filtered_clusters['stats'].append(stat)
    return filtered_clusters

def get_grid(masks):
    clusters = find_clusters(masks['balls'])
    filtered_clusters = filter_clusters_by_size(clusters)
    G.BALLS = find_clusters_center(filtered_clusters['stats'])
    G.BALLS = sort_balls_by_distance()
    coordinates = np.argwhere(masks['red'] != 0)
    grid = np.zeros_like(masks['red'])
    for center in G.BALLS:
        grid[center[1], center[0]] = 2
    grid[coordinates[:, 0], coordinates[:, 1]] = 1


    #Here overwrite all balls outside walls
    # Use connectedComponents to label the connected components in the grid
    num_labels, labeled_grid = cv.connectedComponents(grid)

    # Check if there are any 1's in the grid
    if np.any(grid == 1):
        # Find the label of the largest component of 1's
        court_label = np.argmax(np.bincount(labeled_grid[grid == 1].flat))

        # Set all the balls that are not in the court to 0
        grid[(labeled_grid != court_label) & (grid == 2)] = 0
    else:
        # Handle the case where there are no 1's (e.g., by logging or passing)
        print("No 1's found in the grid.")


    return grid
