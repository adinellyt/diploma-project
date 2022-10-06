import RPi.GPIO as gpio
import time
from ultrasonic import Ultrasonic
from robot_path import return_robot_path
from grid import Grid

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

left_wheel = 15
right_wheel = 13
left_speed_pin = 3
right_speed_pin = 5

gpio.setup(left_wheel, gpio.OUT)
gpio.setup(right_wheel, gpio.OUT)
gpio.setup(left_speed_pin, gpio.OUT)
gpio.setup(right_speed_pin, gpio.OUT)

left_speed = gpio.PWM(left_speed_pin, 1000)
left_speed.start(100)

right_speed = gpio.PWM(right_speed_pin, 1000)
right_speed.start(100)


def go_forward():
    gpio.output(left_wheel, 1)
    gpio.output(right_wheel, 1)
    time.sleep(1 / 6)
    gpio.output(left_wheel, 0)
    gpio.output(right_wheel, 0)


def turn_left():
    gpio.output(right_wheel, 1)
    time.sleep(1 / 6)
    gpio.output(right_wheel, 0)


def turn_right():
    gpio.output(left_wheel, 1)
    time.sleep(1 / 6)
    gpio.output(left_wheel, 0)


left_ultrasonic = Ultrasonic(31, 29)
right_ultrasonic = Ultrasonic(35, 33)

distance_limit = 60

# 'direction_on_map-where_to_turn': 'direction_on_map'
direction_map = {
    'down-left': 'right',
    'down-right': 'left',
    'left-right': 'up',
    'left-left': 'down',
    'right-left': 'up',
    'right-right': 'down',
    'up-left': 'left',
    'up-right': 'right'
}


def return_left_distance():
    return left_ultrasonic.get_distance()


def return_right_distance():
    return right_ultrasonic.get_distance()


def change_source_position(g, direction):
    if direction == 'left':
        g.source_x -= 1
    elif direction == 'right':
        g.source_x += 1
    elif direction == 'up':
        g.source_y -= 1
    elif direction == 'down':
        g.source_y += 1


def get_forward_position(g, direction):
    if direction == 'left':
        return g.source_x - 1, g.source_y
    elif direction == 'right':
        return g.source_x + 1, g.source_y
    elif direction == 'up':
        return g.source_x, g.source_y - 1
    elif direction == 'down':
        return g.source_x, g.source_y + 1


def road(grid, robot_path, direction):
    for i in robot_path:
        time.sleep(1/2)

        if i == 'forward':
            if return_left_distance() > distance_limit and return_right_distance() > distance_limit:
                print("Going forward ...")
                change_source_position(grid, direction)
                go_forward()
            else:
                blocked_x, blocked_y = get_forward_position(grid, direction)
                grid.set_obstructing_grid(blocked_x, blocked_y)
                grid.update_source()
                return grid, False, direction
        elif i == 'left':
            print("Turning left ...")
            turn_left()
            direction = direction_map.get(f"{direction}-{i}")

        elif i == 'right':
            print("Turning right ...")
            turn_right()
            direction = direction_map.get(f"{direction}-{i}")

    return grid, True, direction,


def go(source_x, source_y, destination_x, destination_y, direction):
    grid = Grid(source_x, source_y, destination_x, destination_y)
    grid.set_grid()

    tries_count = 0
    try:
        passed = False
        while not passed:
            if tries_count >= 5:
                return False, direction, grid.source_x, grid.source_y

            robot_path = return_robot_path(grid.grid, direction)
            print(robot_path)

            grid, passed, direction = road(grid, robot_path, direction)
            tries_count += 1

        return True, direction, grid.source_x, grid.source_y
    except Exception as e:
        print(str(e))
        return False, direction, grid.source_x, grid.source_y
