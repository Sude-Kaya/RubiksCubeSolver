import cv2 as cv
import numpy as np
from PIL import Image
from DetectFace import *

capture = cv.VideoCapture(0)

face_1_scanned = False


while True:
    isTrue, frame = capture.read()
    
    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    """
    mask = cv.inRange(hsv_img, lower, upper)
    masked = cv.bitwise_and(frame,frame, mask=mask)
    mask_ = Image.fromarray(mask)
    cv.imshow("masked", masked)
       """

   

    if not face_1_scanned :
        cv.putText(frame, "Scan the front face", (160,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), 2)
        cv.rectangle(frame, (100,100), (400,400), (0,255,0), thickness=5)
        cv.line(frame, (100,200), (400,200), (0,255,0), thickness=5)
        cv.line(frame, (100,300), (400,300), (0,255,0), thickness=5)
        cv.line(frame, (200,100), (200,400), (0,255,0), thickness=5)
        cv.line(frame, (300,100), (300,400), (0,255,0), thickness=5)

        for cell in cells:
                c_color = detectCellColor(hsv_img, cell)

                y1, y2 = cell[0]
                x1, x2 = cell[1]

                cx = (x1 + x2) // 2 -30
                cy = (y1 + y2) // 2 -30

                cv.putText(frame, c_color, (cx, cy),
                        cv.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

      

        
        
    
    cv.imshow("frame", frame)

    if cv.waitKey(1) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()