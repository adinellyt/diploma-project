import RPi.GPIO as gpio
import random 
import time
import cv2
import numpy as np
import os
from ultra1 import ultasonic_1
from ultra2 import ultasonic_2

#status red ball
status_r_b = ""

testmode = 1

#setup mode
gpio.setmode(gpio.BOARD)

#ignore warnings
gpio.setwarnings(False)

#wheel ports
right_w = 13
left_w = 15
enA=16
enB=18

#circle
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

#red color
lower = np.array([161, 155, 84])
upper = np.array([179, 255, 255])


#wheel setups
gpio.setup(left_w,gpio.OUT)
gpio.setup(right_w,gpio.OUT)
gpio.setup(enA,gpio.OUT)
gpio.setup(enB,gpio.OUT)

pA=gpio.PWM(enA,1000)
pA.start(50)

pB=gpio.PWM(enB,1000)
pB.start(50)

#red_ball_right
def red_ball_right():
    gpio.output(left_w, 0)
    gpio.output(right_w, 1)
    print("going red ball right")
    stop()
   
   
#red_ball_right
def red_ball_left():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    print("going red ball left")
    time.sleep(9/10)
    stop()

    
#go backward
def backward():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    print("going backward")
    time.sleep(36/10)
    forward()
    
#go forward 
def forward():
    gpio.output(left_w, 1)
    gpio.output(right_w, 1)
    print("going forward")
    if ultasonic_1() >= 2 and ultasonic_1() <= 60:
        direction = "left ultasonic_1"
        print(direction)
        left()
        
    elif ultasonic_2() >= 2 and ultasonic_2() <= 60:
        direction = "right ultasonic_2"
        print(direction)
        right()
    
    elif ultasonic_1() == 1 and ultasonic_2() == 1:
        print("I need a help")
        stop()
    time.sleep(4/10)


#turn left
def left():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    print("going left")
    time.sleep(18/10)
    stop()
    forward()


#turn right
def right():
    gpio.output(left_w, 0)
    gpio.output(right_w, 1)
    time.sleep(18/10)
    stop()
    forward()
    
#stop
def stop():
    gpio.output(left_w, 0)
    gpio.output(right_w, 0)
    print("going off")
    time.sleep(5/10)


#main program
def calc_dist(p1,p2):
    x1 = p1[0]

    y1 = p1[1]

    x2 = p2[0]

    y2 = p2[1]

    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

    return dist


def getChunks(l, n):

    """Yield successive n-sized chunks from l."""

    a = []

    for i in range(0, len(l), n):   

        a.append(l[i:i + n])

    return a


cap = cv2.VideoCapture(0)
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols / 2)
center = int(cols / 2)
position = 90
        
try:
   if not os.path.exists('data'):
      os.makedirs('data')
except OSError:
   print ('Error: Creating directory of data')

StepSize = 5
currentFrame = 0

if testmode == 1:
   F = open("./data/imagedetails.txt",'a')
   F.write("\n\nNew Test \n")


while(1):

    _,frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
        
    name = './data/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    
    img = frame.copy()
    blur = cv2.bilateralFilter(img,9,40,40)
    edges = cv2.Canny(blur,50,100)
    img_h = img.shape[0] - 1
    img_w = img.shape[1] - 1
    EdgeArray = []

    for j in range(0,img_w,StepSize):
        pixel = (j,0)
        for i in range(img_h-5,0,-1):
            if edges.item(i,j) == 255:
                pixel = (j,i)
                break
    
        EdgeArray.append(pixel)
        
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w)/2)
        print("Find red circle")
        break
    if x_medium < center:
        red_ball_right()
    elif x_medium > center:
        red_ball_left()
    elif x_medium == center:
        stop()
#         time.sleep(20)


    for x in range(len(EdgeArray)-1):

        cv2.line(img, EdgeArray[x], EdgeArray[x+1], (0,255,0), 1)



    for x in range(len(EdgeArray)):

        cv2.line(img, (x*StepSize, img_h), EdgeArray[x],(0,255,0),1)


    chunks = getChunks(EdgeArray,int(len(EdgeArray)/3)) 

    max_dist = 0

    c = []

    for i in range(len(chunks)-1):        

        x_vals = []

        y_vals = []

        for (x,y) in chunks[i]:

            x_vals.append(x)

            y_vals.append(y)


        avg_x = int(np.average(x_vals))

        avg_y = int(np.average(y_vals))

        c.append([avg_y,avg_x])

        cv2.line(frame,(320,480),(avg_x,avg_y),(255,0,0),2)  

    print(c)

    forwardEdge = c[1]
    print(forwardEdge)

    cv2.line(frame,(320,480),(forwardEdge[1],forwardEdge[0]),(0,255,0),3)   
    cv2.imwrite(name, frame)
     
    y = (min(c))
    print(y)
    
        
    if forwardEdge[0] > 250: #200 # >230 works better 

       if y[1] < 310:
          left()
          direction = "left camera"
          print(direction)
       elif y[1] < 310:
          right()
          direction = "right camera"
          print(direction)
       else: 
          right()
          direction = "right camera"
          print(direction)
          
    else:
       forward()
       direction = "forward camera"
       print(direction)
       
    if testmode == 1:
       F.write ("frame"+str(currentFrame)+".jpg" +" | " + str(c[0]) + " | " + str(c[1]) + " | " +str(c[2])  + " | " + direction + "\n") 
       currentFrame +=1

    if testmode == 2:

       cv2.imshow("frame",frame)

       cv2.imshow("Canny",edges)

       cv2.imshow("result",img)


    k = cv2.waitKey(5) & 0xFF  ##change to 5

    if k == 27:

        break


cv2.destroyAllWindows
cap.release()      
gpio.cleanup()