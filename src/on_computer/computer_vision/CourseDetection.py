import cv2 as cv
import numpy as np
import Globals as G


def get_masks_from_frame(frame):

    # Define color ranges
    red_lower_1 = np.array([0, 126, 133], dtype="uint8")
    red_upper_1 = np.array([6, 255, 255], dtype="uint8")

    red_lower_2 = np.array([169, 168, 187], dtype="uint8")
    red_upper_2 = np.array([179, 255, 255], dtype="uint8")

    orange_lower = np.array([10, 102, 203], dtype="uint8")
    orange_upper = np.array([36, 255, 255], dtype="uint8")

    white_lower = np.array([0, 0, 200], dtype="uint8")
    white_upper = np.array([179, 35, 255], dtype="uint8")

    blur_frame = cv.GaussianBlur(frame, (3, 3), 0)  # Add blur
    hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV)  # Convert from RGB to HSV

    # Create masks for red, orange and white
    mask_red_1 = cv.inRange(hsv_frame, red_lower_1, red_upper_1)
    mask_red_2 = cv.inRange(hsv_frame, red_lower_2, red_upper_2)
    mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
    mask_orange = cv.inRange(hsv_frame, orange_lower, orange_upper)
    mask_white = cv.inRange(hsv_frame, white_lower, white_upper)

    # Apply dilation
    obstacle_kernel = np.ones((45, 45), np.uint8)
    ball_kernel = np.ones((3, 3), np.uint8)
    mask_white = cv.dilate(mask_white, ball_kernel)
    mask_orange = cv.dilate(mask_orange, ball_kernel)
    mask_red = cv.dilate(mask_red, obstacle_kernel)
    mask_ball = cv.bitwise_or(mask_orange, mask_white)
    cv.imwrite('border.jpg', mask_red)

    masks = {
        'red': mask_red,
        'balls': mask_ball,
    }

    return masks


def find_clusters(mask):
    amount, labels, stats, _ = cv.connectedComponentsWithStats(mask, connectivity=4)
    clusters = {
        'amount': amount - 1,  # Subtract 1 to exclude the background
        #  'labels': labels[1:], # Returns an array of the labels of the clusters, but we don't need it for now
        'stats': stats[1:]  # Information about each cluster. Used to find the center of each cluster
    }
    return clusters


# Returns a list of centers for each cluster
def find_clusters_center(stats):
    centers = []
    for stat in stats:
        # Calculate the center of the blob
        x = stat[cv.CC_STAT_LEFT] + stat[cv.CC_STAT_WIDTH] // 2
        y = stat[cv.CC_STAT_TOP] + stat[cv.CC_STAT_HEIGHT] // 2
        centers.append((x, y))
    return centers


def get_grid(masks):
    G.BALLS = find_clusters_center(find_clusters(masks['balls'])['stats'])
    coordinates = np.argwhere(masks['red'] != 0)
    grid = np.zeros_like(masks['red'])
    for center in G.BALLS:
        grid[center[1], center[0]] = 2
    grid[coordinates[:, 0], coordinates[:, 1]] = 1
    return grid
