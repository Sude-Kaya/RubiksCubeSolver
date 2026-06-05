import cv2 as cv
import numpy as np
import math

def solutionVisualization(frame, move,  cube_size, cube_center):
   
    color = (0, 0, 255)
    thickness = 7
    arrow_size = 25

    cx, cy = cube_center
    cube_size = cube_size
    half = cube_size // 2

   
    left, right = cx - half, cx + half
    top, bottom = cy - half, cy + half

    is_inverse = "'" in move
    is_double = "2" in move

    
    def apply_arrow(start_pt, end_pt, double_side=False):
        cv.line(frame, start_pt, end_pt, color, thickness)
        
       
        angle_end = math.atan2(end_pt[1] - start_pt[1], end_pt[0] - start_pt[0])
        p1 = (int(end_pt[0] - arrow_size * math.cos(angle_end + math.pi / 6)),
              int(end_pt[1] - arrow_size * math.sin(angle_end + math.pi / 6)))
        p2 = (int(end_pt[0] - arrow_size * math.cos(angle_end - math.pi / 6)),
              int(end_pt[1] - arrow_size * math.sin(angle_end - math.pi / 6)))
        cv.fillPoly(frame, [np.array([end_pt, p1, p2], dtype=np.int32)], color)

       
        if double_side:
            angle_start = math.atan2(start_pt[1] - end_pt[1], start_pt[0] - end_pt[0])
            p3 = (int(start_pt[0] - arrow_size * math.cos(angle_start + math.pi / 6)),
                  int(start_pt[1] - arrow_size * math.sin(angle_start + math.pi / 6)))
            p4 = (int(start_pt[0] - arrow_size * math.cos(angle_start - math.pi / 6)),
                  int(start_pt[1] - arrow_size * math.sin(angle_start - math.pi / 6)))
            cv.fillPoly(frame, [np.array([start_pt, p3, p4], dtype=np.int32)], color)

  
    if move.startswith('U'):
        start, end = (right, top), (left, top)
        if is_inverse: start, end = end, start
        apply_arrow(start, end, double_side=is_double)

    elif move.startswith('D'):
        start, end = (left, bottom), (right, bottom)
        if is_inverse: start, end = end, start
        apply_arrow(start, end, double_side=is_double)

  
    elif move.startswith('L'):
        start, end = (left, top), (left, bottom)
        if is_inverse: start, end = end, start
        apply_arrow(start, end, double_side=is_double)

    
    elif move.startswith('R'):
        start, end = (right, bottom), (right, top)
        if is_inverse: start, end = end, start
        apply_arrow(start, end, double_side=is_double)

    
    elif move.startswith('F'):
        radius = 110
        cv.ellipse(frame, (cx, cy), (radius, radius), 0, 40, 320, color, thickness)
        
        p_40 = (int(cx + radius * np.cos(np.deg2rad(40))), int(cy + radius * np.sin(np.deg2rad(40))))
        p_320 = (int(cx + radius * np.cos(np.deg2rad(320))), int(cy + radius * np.sin(np.deg2rad(320))))
        
        t_40 = (int(p_40[0] - 20 * np.sin(np.deg2rad(40))), int(p_40[1] + 20 * np.cos(np.deg2rad(40))))
        t_320 = (int(p_320[0] + 20 * np.sin(np.deg2rad(320))), int(p_320[1] - 20 * np.cos(np.deg2rad(320))))

        if is_double:
            apply_arrow(t_40, p_40, double_side=False)
            apply_arrow(t_320, p_320, double_side=False)
        else:
            if is_inverse:
                apply_arrow(t_40, p_40, double_side=False)
            else:
                apply_arrow(t_320, p_320, double_side=False)

  
    elif move.startswith('B'):
        radius = 140
        cv.ellipse(frame, (cx, cy), (radius, radius), 0, 40, 320, color, thickness)
        
        p_40 = (int(cx + radius * np.cos(np.deg2rad(40))), int(cy + radius * np.sin(np.deg2rad(40))))
        p_320 = (int(cx + radius * np.cos(np.deg2rad(320))), int(cy + radius * np.sin(np.deg2rad(320))))
        
        t_40 = (int(p_40[0] - 20 * np.sin(np.deg2rad(40))), int(p_40[1] + 20 * np.cos(np.deg2rad(40))))
        t_320 = (int(p_320[0] + 20 * np.sin(np.deg2rad(320))), int(p_320[1] - 20 * np.cos(np.deg2rad(320))))

        if is_double:
            apply_arrow(t_40, p_40, double_side=False)
            apply_arrow(t_320, p_320, double_side=False)
        else:
            if is_inverse:
                apply_arrow(t_320, p_320, double_side=False)
            else:
                apply_arrow(t_40, p_40, double_side=False)

