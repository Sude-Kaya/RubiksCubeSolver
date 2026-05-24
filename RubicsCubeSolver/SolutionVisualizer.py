import cv2 as cv
import numpy as np
from Solver import moves_translation

def solutionVisualization(frame, move, blank, sol_idx):
    color = (0, 0, 255) 
    thickness = 7
    tip_length = 0.3
    
    is_inverse = "'" in move
    is_double = "3" in move


    offset = 70 if is_double else 0

    if move.startswith('U'):
        y = 150
        start, end = (350, y), (150, y)
        if is_inverse: start, end = end, start
        cv.arrowedLine(frame, start, end, color, thickness, tipLength=tip_length)
        if is_double: 
            cv.arrowedLine(frame, (start[0], y+offset), (end[0], y+offset), color, thickness, tipLength=tip_length)

    elif move.startswith('D'):
        y = 350
        start, end = (150, y), (350, y)
        if is_inverse: start, end = end, start
        cv.arrowedLine(frame, start, end, color, thickness, tipLength=tip_length)
        if is_double:
            cv.arrowedLine(frame, (start[0], y+offset), (end[0], y+offset), color, thickness, tipLength=tip_length)

    elif move.startswith('L'):
        x = 150
        start, end = (x, 150), (x, 350)
        if is_inverse: start, end = end, start
        cv.arrowedLine(frame, start, end, color, thickness, tipLength=tip_length)
        if is_double:
            cv.arrowedLine(frame, (x+offset, start[1]), (x+offset, end[1]), color, thickness, tipLength=tip_length)

    elif move.startswith('R'):
        x = 350
        start, end = (x, 350), (x, 150)
        if not is_inverse: start, end = end, start
        cv.arrowedLine(frame, start, end, color, thickness, tipLength=tip_length)
        if is_double:
            cv.arrowedLine(frame, (x+offset, start[1]), (x+offset, end[1]), color, thickness, tipLength=tip_length)

    elif move.startswith('F'):
        pts = np.array([[150,150], [350,150], [350,350], [150,350]], np.int32)
        if is_inverse: pts = pts[::-1]
        for i in range(len(pts)-1):
            cv.arrowedLine(frame, tuple(pts[i]), tuple(pts[i+1]), color, 5)
            if is_double: 
                cv.arrowedLine(frame, tuple(pts[i] + 15), tuple(pts[i+1] + 15), color, 3)
        cv.arrowedLine(frame, tuple(pts[3]), tuple(pts[0]), color, 5)

    elif move.startswith('B'):
        pass

    this_move = moves_translation.get(move)
    info_text = f"Step {sol_idx+1}: {this_move}"

    cv.putText(blank, info_text, (100, 50), 
               cv.FONT_HERSHEY_COMPLEX, 0.9, (255, 255, 255), 2)