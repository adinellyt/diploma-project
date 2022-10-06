import cv2
import numpy as np

videoCapture = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

#red color
lower = np.array([161, 155, 84])
upper = np.array([179, 255, 255])

def red_circle():
    try:
        while True:
            ret, frame = videoCapture.read()
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)
            if not ret: break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img, lower, upper)
            mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100,
                                      param1=100, param2=30, minRadius=75, maxRadius=400)  
            #contours = sorted(mask_contours, key=lambda x:cv2.contourArea(x), reverse=True)
            if circles is not None and len(mask_contours) != 0:
                circles = np.uint16(np.around(circles))
                chosen = None
                for i in circles[0,:]:
                    if chosen is None: chosen = i
                    if prevCircle is not None:
                        if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                            chosen = i
                            print("Find")
                #for cnt in contours:
                    #(x, y, w, h) = cv2.boundingRect(cnt)
                
                    #x_medium = int((x + x + w) / 2)
                    #break
            
            #cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)

                            
                
                cv2.circle(frame, (chosen[0],chosen[1]), 1, (0,100,100), 3)
                cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)
                prevCircle = chosen
            
            cv2.imshow("circles",frame)
        
        
        
    except KeyboardInterrupt:
        print("Cleaning up")
        gpio.cleanup()

    