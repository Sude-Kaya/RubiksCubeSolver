import numpy as np
from PIL import Image
import cv2 as cv

colors = {
"yellow" : [0,255,255], #yellow in BGR
"red" : [0,0,255],
"blue" : [255,100,0],
"white" : [255,255,255], 
"green" : [10,255,0],
"orange" : [0,100,255],
}

cells = [
    ((100,200),(100,200)), ((100,200),(200,300)), ((100,200),(300,400)),
    ((200,300),(100,200)), ((200,300),(200,300)), ((200,300),(300,400)),
    ((300,400),(100,200)), ((300,400),(200,300)), ((300,400),(300,400)),
]

def get_limits(color):
    c = np.uint8([[color]]) #insert the BGR values to convert to HSV
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV)
   
    hue = int(hsvC[0][0][0])
    lower_limit=max(hue - 10,0),30,50
    upper_limit=min(hue + 10,179),255,255

    if color == [255,255,255]:
        lower_limit = 0, 0, 100
        upper_limit= 179, 50, 255

    lower_limit = np.array(lower_limit, dtype = np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit



def detectCellColor(hsv_frame, cell_coords):
    y1, y2 = cell_coords[0]
    x1, x2 = cell_coords[1]

    roi = hsv_frame[y1+25:y2-25, x1+25:x2-25]

    avg_color = np.mean(roi, axis=(0,1)) 

    avg_hue = avg_color[0]
    avg_saturation = avg_color[1]
    avg_value = avg_color[2]

    for name, bgr in colors.items():
        l, u = get_limits(bgr)

        if (l[0] <= avg_hue <= u[0] and
            l[1] <= avg_saturation <= u[1] and
            l[2] <= avg_value <= u[2]):
            return name

    return "unknown"


    

        
