from ultrasonic import Ultrasonic
import RPi.GPIO as gpio

#setup mode
gpio.setmode(gpio.BOARD)

#ignore warnings
gpio.setwarnings(False)

left_ultrasonic = Ultrasonic(31, 29)
right_ultrasonic = Ultrasonic(35, 33)


left_distance = left_ultrasonic.get_distance()
right_distance = right_ultrasonic.get_distance()

for i in range(5):
    print("Left distance: ", left_distance)
    print("Right distance: ", right_distance)

stop()
gpio.cleanup()