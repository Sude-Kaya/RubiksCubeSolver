import numpy as np
import cv2 as cv

colors = {
    'yellow': np.array([30, 255, 255]),
    'red':    np.array([0, 255, 255]),
    'blue':   np.array([108, 255, 255]),
    'white':  np.array([0, 0, 255]),
    'green':  np.array([60, 255, 255]),
    'orange': np.array([12, 255, 255])
}

def get_cell_coords(boundaries):
    coords = []
    for x, y, w, h in boundaries:
        coords.append(((y, y + h),(x, x + w)))
    return coords


def detectCellColor(hsv_frame, cell_coords):
    y1, y2 = cell_coords[0]
    x1, x2 = cell_coords[1]

    roi = hsv_frame[y1:y2, x1:x2]
    roi = roi[::10, ::10]
    
    votes = {}

    for pixel in roi.reshape(-1, 3):
        best_color = None
        best_dist = float("inf")

        for name, hsv_ref in colors.items():
            distance = np.linalg.norm(pixel - hsv_ref)
            if distance < best_dist:
                best_dist = distance
                best_color = name

        votes[best_color] = votes.get(best_color, 0) + 1

    if not votes:
        return "unknown"

    return max(votes, key=votes.get)

        
