import cv2 as cv
import numpy as np

i = 1

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

def get_masks_from_camera():
    x = 320
    y = 180
    x = 320
    y = 180

    #video_capture = cv.VideoCapture(1, cv.CAP_DSHOW) #Open camera WINDOWS OS
    video_capture = cv.VideoCapture(0) #Open camera MAC OS

    video_capture.set(cv.CAP_PROP_FRAME_WIDTH, x)
    video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, y)

    #Define color ranges
    red_lower_1 = np.array([0, 126, 133], dtype="uint8")
    red_upper_1 = np.array([6, 255, 255], dtype="uint8")

    red_lower_2 = np.array([169, 168, 187], dtype="uint8")
    red_upper_2 = np.array([179, 255, 255], dtype="uint8")

    orange_lower = np.array([10, 102, 203], dtype="uint8")
    orange_upper = np.array([36, 255, 255], dtype="uint8")

    white_lower = np.array([0, 0, 200], dtype="uint8")
    white_upper = np.array([179, 35, 255], dtype="uint8")

    green_lower = np.array([26, 33, 0], dtype="uint8")
    green_upper = np.array([78, 255, 255], dtype="uint8")

    blue_lower = np.array([98, 121, 64], dtype="uint8")
    blue_upper = np.array([133, 244, 152], dtype="uint8")

    ret, frame = video_capture.read()
    if not ret:
        print("Camera not detected")

    elif ret:
        blur_frame = cv.GaussianBlur(frame, (3, 3), 0) #Add blur
        hsv_frame = cv.cvtColor(blur_frame, cv.COLOR_BGR2HSV) #Convert from RGB to HSV

        # Create masks for red, green, blue, orange and white
        mask_red_1 = cv.inRange(hsv_frame, red_lower_1, red_upper_1)
        mask_red_2 = cv.inRange(hsv_frame, red_lower_2, red_upper_2)
        mask_red = cv.bitwise_or(mask_red_1, mask_red_2)
        mask_green = cv.inRange(hsv_frame, green_lower, green_upper)
        mask_blue = cv.inRange(hsv_frame, blue_lower, blue_upper)
        mask_robot = cv.bitwise_or(mask_green, mask_blue) #Combine blue and green to see the robot
        mask_orange = cv.inRange(hsv_frame, orange_lower, orange_upper)
        mask_white = cv.inRange(hsv_frame, white_lower, white_upper)
        mask_ball = cv.bitwise_or(mask_orange, mask_white) #Combine orange and white to see the ball

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

        cv.imshow('ImageWindow', mask_white)
        cv.imwrite('frame.jpg', frame)
        cv.imwrite('mask_white.jpg', mask_white)
        cv.imwrite('mask_orange.jpg', mask_orange)
        cv.imwrite('mask_red.jpg', mask_red)
        cv.imwrite('mask_green.jpg', mask_green)
        cv.imwrite('mask_blue.jpg', mask_blue)	        
        path = 'images'
        global i 
        cv.imwrite(path + '/robot' + str(i) + '.jpg', mask_robot)
        i += 1

    video_capture.release()
    cv.destroyAllWindows()
    return masks

masks = get_masks_from_camera()
mask_white = masks['white']
white_clusters = find_clusters(mask_white)
white_centers = find_clusters_center(white_clusters['stats'])