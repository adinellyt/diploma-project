import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
 #ignore warnings
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 6
GPIO_ECHO = 5
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
try:
    while True:
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(1)
        
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(1/1000)
        GPIO.output(GPIO_TRIGGER, False)
        
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        pulse_duration = StopTime - StartTime
        distance = pulse_duration *17150
        distance = round(distance, 2)
        
        print("Distance: ", str(distance), "cm")
 

    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()