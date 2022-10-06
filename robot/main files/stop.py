import RPi.GPIO as gpio
import random 
import time
import cv2
import numpy as np
'''
videoCapture = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

#red color
lower = np.array([161, 155, 84])
upper = np.array([179, 255, 255])
'''

#setup mode
gpio.setmode(gpio.BOARD)

#ignore warnings
gpio.setwarnings(False)

#wheel ports
left_w = 13
right_w = 15



#wheel setups
gpio.setup(left_w,gpio.OUT)
gpio.setup(right_w,gpio.OUT)



#go  
def go():
    gpio.output(left_w, 1)
    gpio.output(right_w, 1)


#turn wheel left
def leftOn():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    time.sleep(18/10)


#turn wheel right
def rightOn():
    gpio.output(left_w, 0)
    gpio.output(right_w, 1)
    time.sleep(18/10)
    
    
#stop
def stop():
    gpio.output(left_w, 0)
    gpio.output(right_w, 0)
    time.sleep(1)


#circle_red_object detect
'''def red_circle_detect():    
    ret, frame = videoCapture.read()
    if not ret: break
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)
    maskFrame = cv2.inRange(hsvFrame, lower, upper)
    
    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100,
                              param1=100, param2=30, minRadius=75, maxRadius=400)  
    
    mask_contours, hierarchy = cv2.findContours(maskFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    if circles is not None and len(mask_contours) != 0:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0,:]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen = i
                    print('Direction find')'''


#main program    
while True:
    #leftOn()
    #rightOn()
    stop()
    #go()
    #time.sleep(6)
    #stop()
    #time.sleep(4)
        
    
gpio.cleanup()
