import cv2 as cv
import numpy as np
from DetectFace import *

from CubeVisualizer import setup_screen, draw_face, plt 


capture = cv.VideoCapture(0)


face_indices = {
    "front": [0, False], "up": [1, False], "left": [2, False], 
    "right": [3, False], "down": [4, False], "back": [5, False]
}
faces = ["front", "up", "left", "right", "down", "back"]
current_face_idx = 0
cube_state = np.full((6, 9), "unknown", dtype='<U10')
phase = "SCANNING"


fig, ax = setup_screen()

def showGrid(face):
    cv.putText(frame, f"Scan the {face.upper()} face", (190,50), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    cv.rectangle(frame, (100,100), (400,400), (0,255,0), thickness=5)
    # Izgara çizgileri
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
        cx, cy = (x1 + x2) // 2 - 30, (y1 + y2) // 2 - 30
        cv.putText(frame, cell_color, (cx, cy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)
    return current_face


while True:
    isTrue, frame = capture.read()
    if not isTrue:
        print("Kamera algılanamadı!")
        break

    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    key = cv.waitKey(1) & 0xFF
    
    if phase == "SCANNING":
        face_name = faces[current_face_idx]
        showGrid(face_name)
        current_face_data = scanFace() 

        # 'c' tuşuna basıldığında onaylar ve çizdirir
        if key == ord('c'):
            target_idx = face_indices[face_name][0]
            cube_state[target_idx] = current_face_data
            face_indices[face_name][1] = True
            
            
            formatted_face = [color[0].upper() if color != "unknown" else "unknown" for color in current_face_data]
            
           
            draw_face(ax, formatted_face, target_idx)
            
            print(f"{face_name} kaydedildi: {formatted_face}")
            current_face_idx += 1

            if current_face_idx >= len(faces):
                print("TÜM YÜZLER OKUNDU!")
                phase = "SOLVING"
                
    elif phase == "SOLVING":
        cv.putText(frame, "Solving Phase...", (200,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,0,255), 2)

    cv.imshow("Kup Tarayici", frame)
    
    
    if key == ord('d'):
        break

capture.release()
cv.destroyAllWindows()

plt.ioff()
plt.show()
