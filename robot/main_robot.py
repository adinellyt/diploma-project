import RPi.GPIO as gpio                                

#setup mode
gpio.setmode(gpio.BOARD)

#ignore warnings
gpio.setwarnings(True)


#wheel setups
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(3, gpio.OUT)
gpio.setup(5, gpio.OUT)
pwmL = gpio.PWM(3, 1)
pwmR = gpio.PWM(5, 1)


#go  
def go_forward():
    gpio.output(13, 1)
    gpio.output(15, 1)

#turn wheel left
def turn_left():
    gpio.output(13, 0)
    gpio.output(15, 1)


#turn wheel right
def turn_right():
    gpio.output(13, 1)
    gpio.output(15, 0)
    
    
#stop
def stop():
    gpio.output(13, 0)
    gpio.output(15, 0)



#main program    
while True:
    print('Hi')
    stop()
    pwmL.start(50)
    pwmR.start(100)
    print('Hi5')

stop()
gpio.cleanup()