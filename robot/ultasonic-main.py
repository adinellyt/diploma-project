import RPi.GPIO as GPIO
import time
  
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
trig = 6 #16
echo = 5 #18
 
#set GPIO direction (IN / OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
 
GPIO.output(trig, False)
print("Waiting For Sensor To Settle")
time.sleep(2)

GPIO.output(trig, True)
time.sleep(1/100000)
GPIO.output(trig, False)

while GPIO.input(echo) == 0:
    pulse_start = time.time()
    
while GPIO.input(echo) == 1:
    pulse_end = time.time()
    
pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)

print("Distance:", distance,"cm")

GPIO.cleanup()