import cv2 as cv
import numpy as np
from DetectFace import *
from CubeVisualizer import setup_screen, draw_face 

capture = cv.VideoCapture(0)

# Face mapping and scan status
face_indices = {
    "front" : [2, False], "left" :[4, False], "right" : [1, False], 
    "up" : [0, False], "down" :[3, False], "back" : [5, False]
}
faces = ["front", "left", "right", "up", "down", "back"]
current_face_idx = 0

# Main data structure to store the state of all 6 faces
cube_state = np.full((6, 9), "unknown", dtype='<U10') 
phase = "SCANNING"

# Initialize the Matplotlib visualization window before the loop
fig, ax = setup_screen() 

def showGrid(face):
    """Draws the 3x3 scanning guide and instructions on the camera feed."""
    cv.putText(frame, f"Scan the {face} face", (190,50), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    cv.rectangle(frame, (100,100), (400,400), (0,255,0), thickness=5)
    cv.line(frame, (100,200), (400,200), (0,255,0), thickness=5)
    cv.line(frame, (100,300), (400,300), (0,255,0), thickness=5)
    cv.line(frame, (200,100), (200,400), (0,255,0), thickness=5)
    cv.line(frame, (300,100), (300,400), (0,255,0), thickness=5)
    cv.putText(frame, "Press 'c' to confirm", (190,450), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

def scanFace():
    """Identifies colors for each cell in the grid using HSV analysis."""
    current_face = np.full(9, "unknown", dtype='<U10')
    for i, cell in enumerate(cells):
        cell_color = detectCellColor(hsv_img, cell)
        current_face[i] = cell_color
        
        y1, y2 = cell[0]
        x1, x2 = cell[1]
        cx, cy = (x1 + x2) // 2 - 30, (y1 + y2) // 2 - 30
        cv.putText(frame, cell_color, (cx, cy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    return current_face

while True:
    isTrue, frame = capture.read()
    if not isTrue: break 
    
    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    key = cv.waitKey(1) & 0xFF
    
    if phase == "SCANNING":
        face = faces[current_face_idx]
        showGrid(face)
        current_face_data = scanFace() 

        # Save data and trigger visualization on 'c' key press
        if key == ord('c'):
            target_idx = face_indices[face][0]
            cube_state[target_idx] = current_face_data
            face_indices[face][1] = True
            
            # Update the 2D Matplotlib map with the confirmed colors
            draw_face(ax, current_face_data, target_idx) 

            current_face_idx += 1
            print(f"Saved {face}:", current_face_data)

            if current_face_idx >= len(faces):
                print("Scanning Complete.")
                phase = "SOLVING"
                
    elif phase == "SOLVING":
        cv.putText(frame, "Solving...", (200,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), 2)

    cv.imshow("Cube Scanner", frame)
    
    # Exit program on 'd' key press
    if key == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
