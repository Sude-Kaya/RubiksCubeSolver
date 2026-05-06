import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
from DetectFace import *
from CubeVisualizer import *
from Solver import *

capture = cv.VideoCapture(0)


face_indices = {
    "front": [2, 0], 
    "up":    [0, 1], 
    "left":  [4, 2], 
    "right": [1, 3], 
    "down":  [3, 4], 
    "back":  [5, 5]
}
faces = ["front", "up", "left", "right", "down", "back"]
current_face_idx = 0
cube_state = np.full((6, 9), "unknown", dtype='<U10')
phase = "SCANNING"

fig, ax = setup_screen()
plt.ion() 

def showGrid(face):
    cv.putText(frame, f"Scan the {face} face", (190,50), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    cv.rectangle(frame, (100,100), (400,400), (0,255,0), thickness=5)
    cv.line(frame, (100,200), (400,200), (0,255,0), thickness=5)
    cv.line(frame, (100,300), (400,300), (0,255,0), thickness=5)
    cv.line(frame, (200,100), (200,400), (0,255,0), thickness=5)
    cv.line(frame, (300,100), (300,400), (0,255,0), thickness=5)
    cv.putText(frame, "Press 'c' to confirm", (190,450), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

def scanFace():
    current_face = np.full(9, "unknown", dtype='<U10')
  
    for i, cell in enumerate(cells):
        cell_color = detectCellColor(hsv_img, cell)
        current_face[i] = cell_color

        y1, y2 = cell[0]
        x1, x2 = cell[1]
        cx = (x1 + x2) // 2 - 30
        cy = (y1 + y2) // 2 - 30

        cv.putText(frame, cell_color, (cx, cy),
                   cv.FONT_HERSHEY_COMPLEX, 0.6, (0,255,0), 1)
    return current_face

while True:
    isTrue, frame = capture.read()
    if not isTrue: break
    
    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    key = cv.waitKey(1) & 0xFF
    
    if phase == "SCANNING":
        face_name = faces[current_face_idx]
        showGrid(face_name)
        current_detected_colors = scanFace() 

        if key == ord('c'):
          
            target_idx = face_indices[face_name][0]
            cube_state[target_idx] = current_detected_colors
            
            formatted_face = [color[0].upper() if color != "unknown" else "U" for color in current_detected_colors]
            
            
            draw_face(ax, formatted_face, face_indices[face_name][1])
            fig.canvas.draw_idle()
            plt.pause(0.1)
            
            print(f"{face_name} saved: {formatted_face}")
            current_face_idx += 1

            if current_face_idx >= len(faces):
                print("completed scaning")
                phase = "SOLVING"
                
    elif phase == "SOLVING":
        cv.putText(frame, "Solving...", (200,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,255), 2)
        
       
        solution = solve_from_colors(
            cube_state[0], cube_state[1], cube_state[2],
            cube_state[3], cube_state[4], cube_state[5]
        )
        print("Solution:", solution)
        phase = "DONE" 

    cv.imshow("Rubik's Cube Solver", frame)
    
    if key == ord('d') 
        break

capture.release()
cv.destroyAllWindows()
plt.ioff()
plt.show()
