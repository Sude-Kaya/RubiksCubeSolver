import cv2 as cv
import numpy as np
from DetectFace import *
from CubeVisualizer import *
from Solver import *
from SolutionVisualizer import *
import time

capture = cv.VideoCapture(0)

face_indices = {"front" : [2, 0] , "right" :[1, 1] , "back" : [5,2] , "left" : [4, 3] , "top" :[0, 4], "bottom" : [3,5]}
faces = ["front", "right", "back", "left", "top", "bottom"]
current_face_idx = 0
cube_state = np.full((6, 9), "unknown", dtype='<U10')
scan_complete = False
phase = "SCANNING"
solution = [""]
sol_idx = 0
current_move = solution[sol_idx]
fig, ax = setup_screen()


def showGrid(face):
    cv.rectangle(frame, (100,100), (400,400), (255,255,255), thickness=3)
    cv.line(frame, (100,200), (400,200), (255,255,255), thickness=3)
    cv.line(frame, (100,300), (400,300), (255,255,255), thickness=3)
    cv.line(frame, (200,100), (200,400), (255,255,255), thickness=3)
    cv.line(frame, (300,100), (300,400), (255,255,255), thickness=3)

def scanFace():
    current_face = np.full(9, "unknown", dtype='<U10')

    for i, cell in enumerate(cells):
        cell_color = detectCellColor(hsv_img, cell)
        current_face[i] = cell_color

        y1, y2 = cell[0]
        x1, x2 = cell[1]

        cx = (x1 + x2) // 2 - 35
        cy = (y1 + y2) // 2 - 30

        cv.putText(frame, cell_color, (cx, cy),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), thickness=2)

    return current_face

def render_Cube_Net(blank):
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    img = cv.resize(img, (500, 400))

    overlay = img[:, :, :3]
    overlay = cv.cvtColor(overlay, cv.COLOR_RGB2BGR)
    alpha = img[:, :, 3] / 255.0

    y1, y2 = 120, 520
    x1, x2 = 680, 1180

    region = blank[y1:y2, x1:x2]

    for c in range(3):
        region[:, :, c] = (
            alpha * overlay[:, :, c] +
            (1 - alpha) * region[:, :, c]
        )
    blank[y1:y2, x1:x2] = region

while True:
    blank = np.zeros((630,1200,3), dtype='uint8')
    isTrue, frame = capture.read()
    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    key = cv.waitKey(1) & 0xFF
    if phase == "SCANNING":
        face = faces[current_face_idx]
        cv.putText(blank, f"Current step: scan the {face} face", (400,50), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
        showGrid(face)
        cv.putText(blank, "Press 'c' to confirm", (500,600), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
        current_face = scanFace() 

        if key == ord('c'):
            target_idx = face_indices[face][0]
            cube_state[target_idx] = current_face
            
            formatted_face = [color[0].upper() if color != "unknown" else "unknown" for color in current_face]
            
            draw_face(ax, formatted_face,face_indices[face][1])
           
            current_face_idx += 1

            if current_face_idx >= len(faces):
                phase = "SOLVING"
                start_time = time.time()
            solution = solve_from_colors(
          cube_state[0],
          cube_state[1],
          cube_state[2],
          cube_state[3],
          cube_state[4],
          cube_state[5]
    )
                
    elif phase == "SOLVING":
        cv.putText(blank, f"Solving...", (530,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,255,255), 2)
        if time.time() - start_time >= 3:
            cv.putText(blank, f"Solving...", (530,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,0,0), 2)
            print("Solution:", solution)
            showGrid("front")
            current_move = solution[sol_idx]
            solutionVisualization(frame, current_move, blank, sol_idx)
            cv.putText(blank, "Press 'p' to proceed", (500,600), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
            
            if key == ord('p'):
                sol_idx += 1
                
                if sol_idx == len(solution):
                    cv.putText(blank, "Press 'p' to proceed", (500,600), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0), 2)
                    phase = "COMPLETE"
                
        
                   

    elif phase == "COMPLETE":
         cv.putText(blank, f"Your Rubik's cube is solved!", (350,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), 2)
         cv.putText(blank, "Press 'q' to quit", (500,600), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)

    blank[80:560, 20:660] = frame
    render_Cube_Net(blank)
    cv.imshow("Rubik's Cube Solver", blank)
    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()