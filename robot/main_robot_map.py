from random import randrange, choice
from turtle import *

from freegames import square, vector

food = vector(0, 0)
snake = vector(10, 0)
backward = vector(0, -10)
forward = vector(0, 10)
tern_left = vector(-10, 0)
tern_right = vector(10, 0)

all_commands = [backward, forward, tern_left, tern_right]


def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190


def move_1():
    """Move snake forward one segment."""
    snake.move(forward)
    
    if not inside(snake):
        move_2()


    print("This is snake", snake)

    clear()

    square(snake.x, snake.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    
    update()
    ontimer(move_1, 100)


def move_2():
    """Move snake forward one segment."""
    snake.move(tern_left)
    
    if not inside(snake):
        return

    print("This is snake", snake)

    clear()

    square(snake.x, snake.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    
    update()
    ontimer(move_1, 100)
    
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
move_1()
done()
