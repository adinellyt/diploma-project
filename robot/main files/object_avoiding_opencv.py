import time
import cv2
import numpy as np
import math
import os
import RPi.GPIO as gpio
import random 

a = 1
b = 0.9
c = 0.8
d = 0.7
e = 0.6
f = 0.5
g = 0.4

testmode = 1 #to enable added features such as view and save on file

key = ''

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


#go backward
def backward():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    print("going backward")
    time.sleep(36/10)
    
#go forward 
def forward():
    gpio.output(left_w, 1)
    gpio.output(right_w, 1)
    print("going forward")
    time.sleep(6/10)


#turn left
def left():
    gpio.output(left_w, 1)
    gpio.output(right_w, 0)
    print("going left")
    time.sleep(18/10)
    forward()


#turn right
def right():
    gpio.output(left_w, 0)
    gpio.output(right_w, 1)
    print("going right")
    time.sleep(18/10)
    forward()
    
    
#stop
def stop():
    gpio.output(left_w, 0)
    gpio.output(right_w, 0)
    print("going off")
    time.sleep(6/10)
   
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

    #if testmode == 1:
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


    for x in range(len(EdgeArray)-1):

        cv2.line(img, EdgeArray[x], EdgeArray[x+1], (0,255,0), 1)



    for x in range(len(EdgeArray)):

        cv2.line(img, (x*StepSize, img_h), EdgeArray[x],(0,255,0),1)


    chunks = getChunks(EdgeArray,int(len(EdgeArray)/3)) # 5

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
          #pwm.start(0)
          #pwm1.start(40)
          direction = "left "
          print(direction)

       else: 
          right()
          direction = "right "
          print(direction)

    else:
       forward()
#       sleep(0.005)
       direction = "forward "
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
         