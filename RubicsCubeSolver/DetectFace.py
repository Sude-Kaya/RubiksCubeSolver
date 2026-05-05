import numpy as np
import cv2 as cv

colors = {
"yellow" : [0,255,255], #yellow in BGR
"red" : [0,0,255],
"blue" : [255,100,0],
"white" : [255,255,255], 
"green" : [0,255,0],
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
    lower_limit=max(hue - 10,0),60,60
    upper_limit=min(hue + 10,179),255,255

    if color == [255,255,255]:
        lower_limit = 0, 0, 100
        upper_limit= 179, 50, 255
    elif color == [0,255,0]:
        lower_limit=max(hue - 10,0),30,60
        upper_limit=min(hue + 10,179),255,255

    lower_limit = np.array(lower_limit, dtype = np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def detectCellColor(hsv_frame, cell_coords):
    y1, y2 = cell_coords[0]
    x1, x2 = cell_coords[1]

    roi = hsv_frame[y1+25:y2-25, x1+25:x2-25]
    roi = roi[::4, ::4]
    votes = {}

    for pixel in roi.reshape(-1, 3):
        h, s, v = pixel
        for name, bgr in colors.items():
            l, u = get_limits(bgr)

            if (l[0] <= h <= u[0] and
                l[1] <= s <= u[1] and
                l[2] <= v <= u[2]):

                votes[name] = votes.get(name, 0) + 1
                break

    if not votes:
        return "unknown"

    return max(votes, key=votes.get)  
