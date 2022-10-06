import RPi.GPIO as gpio
import time

#setup mode
gpio.setmode(gpio.BOARD)

#ignore warnings
gpio.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 35
GPIO_ECHO = 33
 
#set GPIO direction (IN / OUT)
gpio.setup(GPIO_TRIGGER, gpio.OUT)
gpio.setup(GPIO_ECHO, gpio.IN)

def ultasonic_2():
    try:
        # set Trigger to HIGH
        gpio.output(GPIO_TRIGGER, False)
        time.sleep(1/1000)
        
        gpio.output(GPIO_TRIGGER, True)
        time.sleep(1/1000)
        gpio.output(GPIO_TRIGGER, False)
        
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while gpio.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while gpio.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        pulse_duration = StopTime - StartTime
        distance = pulse_duration *17150
        distance = round(distance, 2)
        return distance

     

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Cleaning up")
        gpio.cleanup()

while True:
    er = ultasonic_2()
    print(er)