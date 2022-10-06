import RPi.GPIO as gpio
import time


class Ultrasonic:
    trigger_pin = 0
    echo_pin = 0
    
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        gpio.setup(self.trigger_pin, gpio.OUT)
        gpio.setup(self.echo_pin, gpio.IN)

    def get_distance(self):
        gpio.output(self.trigger_pin, False)
        time.sleep(1/1000)
        
        gpio.output(self.trigger_pin, True)
        time.sleep(1/1000)
        
        gpio.output(self.trigger_pin, False)
        
        start_time = time.time()
        stop_time = time.time()
        while gpio.input(self.echo_pin) == 0:
            start_time = time.time()
        while gpio.input(self.echo_pin) == 1:
            stop_time = time.time()
     
        pulse_duration = stop_time - start_time
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        return distance
