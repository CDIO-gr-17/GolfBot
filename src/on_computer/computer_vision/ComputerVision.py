import cv2 as cv
import numpy as np

def get_robot_pos_with_mask(mask):
    robot_mask_cluster = find_clusters(mask)
    robot_pos_middle = find_clusters_center(robot_mask_cluster['stats'])
    if(robot_mask_cluster['amount'] == 0):
        return None
    return robot_pos_middle[0]

#Returns a dictionary of clusters with the amount of clusters and the stats of each cluster
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

def get_grid(mask_red, mask_orange, mask_white):
    combined_grid = np.zeros_like(mask_red)

    obstacle_coordinates = np.argwhere(mask_red != 0)
    ball_mask = cv.bitwise_or(mask_orange, mask_white)
    ball_clusters = find_clusters(ball_mask)
    ball_centers = find_clusters_center(ball_clusters['stats'])

    if ball_clusters['amount'] > 0:
        for center in ball_centers:
            combined_grid[center[1], center[0]] = 2
    combined_grid[obstacle_coordinates[:, 0], obstacle_coordinates[:, 1]] = 1

    np.savetxt('combined_grid.txt', combined_grid, fmt='%d')
    return combined_grid

def get_masks_from_camera(mtx=None, dist=None):
    x = 250
    y = 140
    resolution = (x, y)

    video_capture = cv.VideoCapture(1, cv.CAP_DSHOW) #Open camera WINDOWS OS
    #video_capture = cv.VideoCapture(0) #Open camera MAC OS

    #Define color ranges
    red_lower_1 = np.array([0, 100, 20], dtype="uint8")
    red_upper_1 = np.array([5, 255, 255], dtype="uint8")

    red_lower_2 = np.array([170, 100, 20], dtype="uint8")
    red_upper_2 = np.array([180, 255, 255], dtype="uint8")

    orange_lower = np.array([15, 100, 20], dtype="uint8")
    orange_upper = np.array([25, 255, 255], dtype="uint8")

    white_lower = np.array([0, 0, 220], dtype="uint8")
    white_upper = np.array([180, 100, 255], dtype="uint8")

    green_lower = np.array([50, 100, 20], dtype="uint8")
    green_upper = np.array([70, 255, 255], dtype="uint8")

    green_lower = np.array([65, 50, 20], dtype="uint8")
    green_upper = np.array([85, 255, 255], dtype="uint8")

    blue_lower = np.array([100, 150, 20], dtype="uint8")
    blue_upper = np.array([110, 255, 255], dtype="uint8")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Camera not detected")

        elif ret:
            if mtx is not None and dist is not None:
                frame = cv.undistort(frame, mtx, dist, None, mtx)
            blur_frame = cv.GaussianBlur(frame, (17, 17), 0) #Add blur
            hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV) #Convert from RGB to HSV
            resized_frame = cv.resize(hsv_frame, resolution, interpolation=cv.INTER_NEAREST) #Apply the resolution specified

            # Create masks for red, green, blue, orange and white
            mask_red_1 = cv.inRange(resized_frame, red_lower_1, red_upper_1)
            mask_red_2 = cv.inRange(resized_frame, red_lower_2, red_upper_2)
            mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
            mask_green = cv.inRange(resized_frame, green_lower, green_upper)
            mask_blue = cv.inRange(resized_frame, blue_lower, blue_upper)
            mask_orange = cv.inRange(resized_frame, orange_lower, orange_upper)
            mask_white = cv.inRange(resized_frame, white_lower, white_upper)

            #Apply dilation
            obstacle_kernel = np.ones((15, 15), np.uint8)
            ball_kernel = np.ones((3, 3), np.uint8)
            mask_white = cv.dilate(mask_white, ball_kernel)
            mask_orange = cv.dilate(mask_orange, ball_kernel)
            mask_red = cv.dilate(mask_red,obstacle_kernel)

            masks = {
                'red': mask_red,
                'orange': mask_orange,
                'white': mask_white,
                'green': mask_green,
                'blue': mask_blue
            }

            get_grid(mask_red, mask_orange, mask_white) #Used for debugging, saves the grid to a file. Comment out if not needed

            cv.imshow('ImageWindow', mask_white)
            if cv.waitKey(1) & 0xFF == ord('q'): break
    video_capture.release()
    cv.destroyAllWindows()
    return masks

masks = get_masks_from_camera()
mask_white = masks['white']
white_clusters = find_clusters(mask_white)
white_centers = find_clusters_center(white_clusters['stats'])
print("Amount of white clusters: ", white_clusters['amount'])
print("Middle of white clusters position: ", white_centers)