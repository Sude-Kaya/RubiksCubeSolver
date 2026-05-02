import cv2 as cv
import numpy as np
from DetectFace import *

capture = cv.VideoCapture(0)
face_indices = {"front" : [2, False] , "left" :[4, False] , "right" : [1, False] , "up" : [0, False] , "down" :[3, False], "back" : [5, False]}
faces = ["front", "left", "right", "up", "down", "back"]
current_face_idx = 0
cube_state = np.full((6, 9), "unknown")
scan_complete = False
phase = "SCANNING"

def showGrid(face):
    cv.putText(frame, f"Scan the {face} face", (190,50), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    cv.rectangle(frame, (100,100), (400,400), (0,255,0), thickness=5)
    cv.line(frame, (100,200), (400,200), (0,255,0), thickness=5)
    cv.line(frame, (100,300), (400,300), (0,255,0), thickness=5)
    cv.line(frame, (200,100), (200,400), (0,255,0), thickness=5)
    cv.line(frame, (300,100), (300,400), (0,255,0), thickness=5)
    cv.putText(frame, "Press 'c' to confirm", (190,450), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

def scanFace():
    current_face = np.full(9, "unknown")

    for i, cell in enumerate(cells):
        cell_color = detectCellColor(hsv_img, cell)
        current_face[i] = cell_color

        y1, y2 = cell[0]
        x1, x2 = cell[1]

        cx = (x1 + x2) // 2 - 30
        cy = (y1 + y2) // 2 - 30

        cv.putText(frame, cell_color, (cx, cy),
                   cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

    return current_face

while True:
    isTrue, frame = capture.read()
    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    key = cv.waitKey(1) & 0xFF
    
    if phase == "SCANNING":
        face = faces[current_face_idx]

        showGrid(face)

        current_face = scanFace() 


        if key == ord('c'):
            cube_state[face_indices[face][0]] = current_face
            face_indices[face][1] = True
            current_face_idx += 1
            print(cube_state)
            print(f"{face} saved:", current_face)

            if current_face_idx >= len(faces):
                print("DONE SCANNING")
                phase = "SOLVING"
                
    elif phase == "SOLVING":
        cv.putText(frame, f"Solving...", (200,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), 2)

        #Solver module integration here

    cv.imshow("frame", frame)
    if key == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
