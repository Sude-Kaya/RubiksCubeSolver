import cv2 as cv
import numpy as np
from DetectFace import *
from CubeVisualizer import *
from Solver import *
from SolutionVisualizer import *
import time
from math import floor
from MainHelper import *

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
cell_coords = []
detect_mode = "TRACK"

def on_mouse_click(event, x, y, flags, param):
    """Kullanıcı ekrandaki butonlara veya 2D haritaya tıkladığında tetiklenir."""
    global cube_state, ax, fig, phase, solution, start_time, current_face_idx, sol_idx, current_move
    
    if event == cv.EVENT_LBUTTONDOWN:
         #Track or grid mode
        if 20 <= x <= 150 and 10 <= y <= 60: 
            global detect_mode 
            if detect_mode == "GRID":
                detect_mode = "TRACK"
            else:
                detect_mode = "GRID"
            return
        
        # 1. TARAMA ve EDİTLEME AŞAMASINDAKİ BUTONLAR
        if phase == "SCANNING":
            # --- "SCAN FACE" Butonu ---
            if 700 <= x <= 880 and 540 <= y <= 590:
                if current_face_idx < len(faces):
                    face = faces[current_face_idx]
                    target_idx = face_indices[face][0]
                    cube_state[target_idx] = current_face
                    formatted_face = [color[0].upper() if color != "unknown" else "unknown" for color in current_face]
                    draw_face(ax, formatted_face, face_indices[face][1])
                    current_face_idx += 1
                return

            # --- "EDIT DONE" Butonu ---
            if 900 <= x <= 1080 and 540 <= y <= 590:
                phase = "SOLVING"
                start_time = time.time()
                solution = solve_from_colors(
                    cube_state[0], cube_state[1], cube_state[2],
                    cube_state[3], cube_state[4], cube_state[5]
                )
                sol_idx = 0
                if len(solution) > 0:
                    current_move = solution[sol_idx]
                else:
                    current_move = "NONE"
                return


            # --- 2D HARİTA ÜZERİNDEKİ KARELERİN TIKLANMA KONTROLÜ ---
            if 680 <= x <= 1180 and 120 <= y <= 520:
                local_x = x - 680
                local_y = y - 120
                
                mat_x = (local_x / 500.0) * 12.0
                mat_y = ((400 - local_y) / 400.0) * 9.0
                
                face_order = ["front", "right", "back", "left", "top", "bottom"]
                
                for face_list_idx, face_name in enumerate(face_order):
                    target_idx, vis_idx = face_indices[face_name]
                    base_x, base_y = FACE_POSITIONS[vis_idx]
                    
                    if (base_x - 0.05) <= mat_x <= (base_x + 3.05) and (base_y - 0.05) <= mat_y <= (base_y + 3.05):
                        col = int(floor(mat_x - base_x))
                        row = 2 - int(floor(mat_y - base_y))
                        
                        col = max(0, min(2, col))
                        row = max(0, min(2, row))
                        
                        cell_idx = row * 3 + col
                        
                        if 0 <= cell_idx < 9:
                            current_color = cube_state[target_idx][cell_idx]
                            if current_color in COLOR_CYCLE:
                                next_idx = (COLOR_CYCLE.index(current_color) + 1) % len(COLOR_CYCLE)
                                new_color = COLOR_CYCLE[next_idx]
                            else:
                                new_color = "yellow"
                                
                            cube_state[target_idx][cell_idx] = new_color
                            
                            patch_idx = (face_list_idx * 9) + cell_idx
                            if patch_idx < len(ax.patches):
                                color_letter = new_color[0].upper()
                                actual_hex_color = COLORS.get(color_letter, '#A0A0A0')
                                ax.patches[patch_idx].set_facecolor(actual_hex_color)
                            break

        # 2. ÇÖZÜM (SOLVING) AŞAMASINDAKİ BUTONLAR
        elif phase == "SOLVING":
            # --- "PREV MOVE" Butonu ---
            if 700 <= x <= 880 and 300 <= y <= 350:
                if sol_idx > 0:
                    sol_idx -= 1
                    current_move = solution[sol_idx]
                return

            # --- "NEXT MOVE" Butonu ---
            if 900 <= x <= 1080 and 300 <= y <= 350:
                if sol_idx < len(solution) - 1:
                    sol_idx += 1
                    current_move = solution[sol_idx]
                else:
                    phase = "COMPLETE"
                return

        # 3. TEBRİKLER (COMPLETE) AŞAMASINDAKİ BUTON
        elif phase == "COMPLETE":
            # --- "EXIT" Butonu ---
            if 500 <= x <= 700 and 420 <= y <= 470:
                capture.release()
                cv.destroyAllWindows()
                exit()

cv.namedWindow("Rubik's Cube Solver")
cv.setMouseCallback("Rubik's Cube Solver", on_mouse_click)


while True:
    blank = np.full((630,1200,3), 0, dtype='uint8')
    key = cv.waitKey(1) & 0xFF

    if phase != "COMPLETE" and detect_mode == "TRACK":
            isTrue, frame = capture.read()
            hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            cv.rectangle(blank, (20,10), (150, 60), color= (0, 0, 140) , thickness=cv.FILLED)
            cv.rectangle(blank, (20,10), (150, 60), (255, 255, 255), thickness=2)
            cv.putText(blank, f"{detect_mode}", (50, 40), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

            valid_contours = []
            boundaries = []
            h,s,v = cv.split(hsv_img)

            _, thresh = cv.threshold(v,70,255,cv.THRESH_BINARY)
            
            thresh = cv.adaptiveThreshold(
                thresh,
                255,
                cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv.THRESH_BINARY_INV,
                11,
                2
            )
            kernel = np.ones((5,5), np.uint8)
            thresh = cv.dilate(thresh, kernel, iterations=2)

            # cv.imshow("thresh adaptive", thresh)

            contours, hierarchy = cv.findContours(
                thresh,
                cv.RETR_LIST,
                cv.CHAIN_APPROX_SIMPLE
            )

            for cnt in contours:
                area = cv.contourArea(cnt)
            
                if area < 800:
                    continue
                peri = cv.arcLength(cnt, True)
                approx = cv.approxPolyDP(
                    cnt,
                    0.04 * peri,
                    True
                )
                if len(approx) == 4:
                    x,y,w,h = cv.boundingRect(approx)
                    if w > 150 or h > 150:
                        continue
                    rect_area = w * h

                    extent = area / float(rect_area)
                    if extent < 0.8:
                        continue

                    aspect = w / float(h)
                
                    if 0.8 < aspect < 1.2:
                        valid_contours.append(approx)
                        boundaries.append([x,y,w,h])

            boundaries = sort_boundaries(boundaries)

            
            if len(boundaries) == 9:
                contoured_frame = cv.drawContours(image = frame, contours = valid_contours, contourIdx= -1,
                                            color=(255,255,255), thickness=2)
                p1, p2 = get_cube_boundaries(boundaries=boundaries)
                cv.rectangle(contoured_frame, p1, p2, thickness=2, color=(255,255,255))
                cell_coords = get_cell_coords(boundaries=boundaries)
            
            else:
                cell_coords = []

    elif phase != "COMPLETE" and detect_mode == "GRID":
        isTrue, frame = capture.read()
        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        showGrid(frame)
        cv.rectangle(blank, (20,10), (150, 60), color= (0, 0, 140) , thickness=cv.FILLED)
        cv.rectangle(blank, (20,10), (150, 60), (255, 255, 255), thickness=2)
        cv.putText(blank, f"{detect_mode}", (50, 40), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)


    if phase == "SCANNING":
            render_Cube_Net(fig,blank)
            if current_face_idx < len(faces):
                face = faces[current_face_idx]
                cv.putText(blank, f"Current step: scan the {face} face", (400,40), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                if detect_mode == "TRACK":
                    current_face = scanFace(frame, cell_coords, hsv_img)
                elif detect_mode == "GRID":
                    current_face = scanFace(frame, grid_coords, hsv_img)
            else:
                cv.putText(blank, "All faces scanned! Check map or click DONE", (300, 40), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
            cv.putText(blank, "Tip: You can click the cube net anytime to fix colors.", (340, 70), cv.FONT_HERSHEY_COMPLEX, 0.6, (180,180,180), 2)

            # "SCAN FACE" Butonu
            cv.rectangle(blank, (700, 540), (880, 590), NAVY_COLOR, thickness=cv.FILLED)
            cv.rectangle(blank, (700, 540), (880, 590), (255, 255, 255), thickness=2)
            cv.putText(blank, "SCAN FACE", (725, 572), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

            # "EDIT DONE" Butonu
            cv.rectangle(blank, (900, 540), (1080, 590), (0, 180, 0), thickness=cv.FILLED)
            cv.rectangle(blank, (900, 540), (1080, 590), (255, 255, 255), thickness=2)
            cv.putText(blank, "DONE", (950, 572), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
            
            blank[80:560, 20:660] = frame
        
           
                
    elif phase == "SOLVING":
        blank[80:560, 20:660] = frame
        cv.putText(blank, f"Solving...", (530,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,255,255), 2)
        if time.time() - start_time >= 3:
            cv.putText(blank, f"Solving...", (530,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,0,0), 2)
            current_move = solution[sol_idx]

            if detect_mode == "GRID":
               showGrid(frame)
               
               solutionVisualization(
                    frame,
                    current_move,
                    cube_size = 200,
                    cube_center=(250,250),
                )

            elif detect_mode == "TRACK":
               if len(boundaries) == 9:
                    try:
                        (x1, y1), (x2, y2) = get_cube_boundaries(boundaries)

                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)

                        width = x2 - x1
                        height = y2 - y1

                        size = max(width, height)

                        solutionVisualization(
                            frame,
                            current_move,
                            cube_size = size,
                            cube_center=(center_x, center_y)
                        )
                    except Exception:
                        pass

            this_move = moves_translation.get(current_move)
            info_text = f"Step {sol_idx + 1}: {this_move}"
            cv.putText(blank, info_text, (170, 50), cv.FONT_HERSHEY_COMPLEX, 0.9, (255, 255, 255), 2)
            cv.putText(blank, f"Move {sol_idx + 1} / {len(solution)}: {current_move}", (750, 200), cv.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

    # "PREV MOVE" Butonu
            cv.rectangle(blank, (700, 300), (880, 350), NAVY_COLOR, thickness=cv.FILLED)
            cv.rectangle(blank, (700, 300), (880, 350), (255, 255, 255), thickness=2)
            cv.putText(blank, "PREV MOVE", (725, 332), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

            # "NEXT MOVE" Butonu
            cv.rectangle(blank, (900, 300), (1080, 350), (0, 180, 0), thickness=cv.FILLED)
            cv.rectangle(blank, (900, 300), (1080, 350), (255, 255, 255), thickness=2)
            cv.putText(blank, "NEXT MOVE", (930, 332), cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
            
            blank[80:560, 20:660] = frame

            
            if sol_idx == len(solution):
                phase = "COMPLETE"
                    
            
    elif phase == "COMPLETE":
        update_and_draw_confetti(blank)
        cv.putText(blank, "Your Rubik's cube is solved!", (400, 310), cv.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
        
        # "EXIT" Butonu
        cv.rectangle(blank, (500, 420), (700, 470), (0, 0, 200), thickness=cv.FILLED)
        cv.rectangle(blank, (500, 420), (700, 470), (255, 255, 255), thickness=2)
        cv.putText(blank, "EXIT", (570, 452), cv.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

    
    cv.imshow("Rubik's Cube Solver", blank)
    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()