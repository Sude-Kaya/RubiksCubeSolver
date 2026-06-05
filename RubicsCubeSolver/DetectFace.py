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

grid_coords = [
    ((100,200),(100,200)), ((100,200),(200,300)), ((100,200),(300,400)),
    ((200,300),(100,200)), ((200,300),(200,300)), ((200,300),(300,400)),
    ((300,400),(100,200)), ((300,400),(200,300)), ((300,400),(300,400)),
]

def showGrid(frame):
    cv.rectangle(frame, (100,100), (400,400), (255,255,255), thickness=3)
    cv.line(frame, (100,200), (400,200), (255,255,255), thickness=3)
    cv.line(frame, (100,300), (400,300), (255,255,255), thickness=3)
    cv.line(frame, (200,100), (200,400), (255,255,255), thickness=3)
    cv.line(frame, (300,100), (300,400), (255,255,255), thickness=3)

def scanFace(frame, cell_coords, hsv_img):
    current_face = np.full(9, "unknown", dtype='<U10')

    for i, cell in enumerate(cell_coords):
        cell_color = detectCellColor(hsv_img, cell)
        current_face[i] = cell_color

        y1, y2 = cell[0]
        x1, x2 = cell[1]

        cx = (x1 + x2) // 2 - 30
        cy = (y1 + y2) // 2 - 20

        cv.putText(frame, cell_color, (cx, cy),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), thickness=2)

    return current_face

def get_cell_coords(boundaries):
    coords = []
    for x, y, w, h in boundaries:
        coords.append(((y, y + h),(x, x + w)))
    return coords

def sort_boundaries(boundaries):
    
    boundaries.sort(key=lambda cell: cell[1])

    row1 = sorted(boundaries[:3], key=lambda cell: cell[0])
    row2 = sorted(boundaries[3:6], key=lambda cell: cell[0])
    row3 = sorted(boundaries[6:9], key=lambda cell: cell[0])

    return row1 + row2 + row3

def get_cube_boundaries(boundaries):
    min_x = min(cell[0] for cell in boundaries)
    min_y = min(cell[1] for cell in boundaries)

    max_x = max(cell[0] + cell[2] for cell in boundaries)
    max_y = max(cell[1] + cell[3] for cell in boundaries)

    return (min_x, min_y), (max_x, max_y)

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



