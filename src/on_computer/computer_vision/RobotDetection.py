import cv2 as cv
import numpy as np
from positions.Displacement import move_point
import Globals as G


def get_robot_pos_and_heading(frame):
    # Convert the image to grayscale
    grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the image
    blurred = cv.GaussianBlur(grayscale, (3, 3), 0)

    # Apply Canny edge detection
    edges = cv.Canny(blurred, 25, 150)

    # Find contours in the edged image
    contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    min_area = 500  # Adjust this value based on your requirements
    min_angle = np.pi * 1 / 8  # Minimum angle of a triangle (in radians)
    max_angle = np.pi * 1 / 2  # Maximum angle of a triangle (in radians)

    for contour in contours:
        # Filter out small contours
        if cv.contourArea(contour) < min_area:
            continue

        # Approximate the contour
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)
        # If the approximated contour has three points, then it might be a triangle
        if len(approx) == 3:
            # Compute the angles of the triangle
            a = np.linalg.norm(approx[1] - approx[2])
            b = np.linalg.norm(approx[2] - approx[0])
            c = np.linalg.norm(approx[0] - approx[1])
            angles = np.arccos((np.square(a) + np.square(b) - np.square(c)) / (2 * a * b))

            # Calculate the centroid of the triangle
            centroid = np.mean(approx, axis=0).squeeze()

            # Find the vertex that is farthest from the centroid
            distances = [np.linalg.norm(vertex - centroid) for vertex in approx]
            farthest_vertex = approx[np.argmax(distances)].squeeze()

            # Calculate the heading (in radians) from the centroid to the farthest vertex
            heading = np.arctan2(farthest_vertex[1] - centroid[1], farthest_vertex[0] - centroid[0])

            # Convert the heading to degrees
            heading_degrees = np.degrees(heading)
            # Adjust the heading so that 0 degrees is up and increases in a clockwise direction
            adjusted_heading_degrees = (heading_degrees + 90) % 360

            # Full resolution of the image
            full_width, full_height = frame.shape[1], frame.shape[0]

            # Lower resolution
            low_width, low_height = 320, 180

            # Calculate the ratios
            width_ratio = low_width / full_width
            height_ratio = low_height / full_height

            # Convert the coordinates of the farthest vertex
            farthest_vertex_low_res = farthest_vertex * [width_ratio, height_ratio]
            # Round the coordinates and convert to integers
            farthest_vertex_low_res = np.round(farthest_vertex_low_res).astype(int)
            farthest_vertex_low_res_adjusted = (move_point(farthest_vertex_low_res, G.GRID))
            if farthest_vertex_low_res_adjusted is None:
                return None
            farthest_vertex_low_res_adjusted = (int(farthest_vertex_low_res_adjusted[0]), int(farthest_vertex_low_res_adjusted[1]))

            # Check if the angles are within the range expected for a triangle
            if np.all(np.logical_and(angles > min_angle, angles < max_angle)):
                cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv.imwrite('robot.jpg', frame)
                return adjusted_heading_degrees, farthest_vertex_low_res_adjusted
