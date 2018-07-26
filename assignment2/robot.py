# Robot program for the Course
# Made by Paulo Dores
# Open source, enjoy using and modifying it!
# Python 2.7 in Ubuntu 16.4

import turtle
import os
import random
from math import floor
from time import sleep

# Constants
border = -400
safe_margin = border - 15
robotspeed = 1
reachgoal = False
FREEWALK = 0
FINDFOOD = 1
EAT = 2
intention = ["free walk", "find food", "eat"]
intention_idx = FREEWALK
POSX = 0
POSY = 1
IDLE = 2
MIN_RADIUS = 80
MAX_RADIUS = 200
STAMP_SIZE = 20
REDUCE_HUNGER = 60

# Variables
intention_idx = 0
hunger = 25 #random.randint(0, 25)
hunger_radius = MIN_RADIUS
intention_history = ["free walk", "free walk", "free walk"]

# Register shapes
turtle.register_shape("robot_top.gif")
turtle.register_shape("robot_bot.gif")
turtle.register_shape("robot_lef.gif")
turtle.register_shape("robot_rig.gif")
turtle.register_shape("apple.gif")
turtle.register_shape("hole.gif")
turtle.register_shape("water.gif")
turtle.register_shape("snake.gif")

turtle.register_shape("explosion-gif/frame_00_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_01_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_02_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_03_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_04_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_05_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_06_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_07_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_08_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_09_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_10_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_11_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_12_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_13_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_14_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_15_delay-0.01s.gif")
turtle.register_shape("explosion-gif/frame_16_delay-0.01s.gif")

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.bgpic("grass_background.gif")
wn.tracer(3)
wn.screensize(800, 800)
wn.title("Robot")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(border, border)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
	border_pen.fd(border*-2)
	border_pen.lt(90)
border_pen.hideturtle()

def check_collision(tiles, target):
	for tile in tiles:
		if target.distance(tile) == 0:
			return True
	return False

def check_collision(tiles, target, threshold = 0):
	for tile in tiles:
		if target.distance(tile) <= threshold:
			return True
	return False

def generate_water_position(number_tiles):
	idx = number_tiles
	randomX = random.randint(0,7)
	randomY = random.randint(0,7)
	matrix = [ [0 for i in range(8)] for j in range(8)]
	matrix[randomX][randomY] = 1
	pos_list = []
	pos_list.append([randomX, randomY])
	idx -= 1
	while idx > 0:
		if randomX+1 < 8:
			randomX += 1
		elif randomY+1 < 8:
			randomY += 1
		elif randomX-1 > 0:
			randomX -= 1
		elif randomY-1 > 0:
			randomY -= 1
		matrix[randomX][randomY] = 1
		pos_list.append([randomX, randomY])
		idx -= 1
	return pos_list

# Create waters
NUMBER_WATERS = random.randint(2, 4)
position_list = generate_water_position(NUMBER_WATERS)
print position_list
waters = []
for i in range(NUMBER_WATERS):
	waters.append(turtle.Turtle())
for water in waters:
	water.color("blue")
	water.shape("water.gif")
	water.penup()
	water.speed(0)
	randomX = position_list[0][0] * 100 - 350
	randomY = position_list[0][1] * 100 - 350
	print randomX, randomY
	water.setposition(randomX, randomY)
	position_list = position_list[1:]
	print position_list

# Create holes
NUMBER_HOLES = 3
holes = []
for i in range(NUMBER_HOLES):
	holes.append(turtle.Turtle())

for hole in holes:
	hole.color("brown")
	hole.shape("hole.gif")
	hole.penup()
	hole.speed(0)
	randomY = random.randint(-350, 350)
	randomX = random.randint(-350, 350)
	hole.setposition(randomX, randomY)
	while check_collision(waters, hole, 100):
		randomY = random.randint(-350, 350)
		randomX = random.randint(-350, 350)
		hole.setposition(randomX, randomY)

# Create the snake
snake = turtle.Turtle()
snake.color("yellow")
snake.shape("snake.gif")
snake.penup()
snake.speed(0)
randomY = random.randint(-350, 350)
randomX = random.randint(-350, 350)
snake.setposition(randomX, randomY)
while check_collision(waters, snake, 100) or check_collision(holes, snake, 100):
	randomY = random.randint(-350, 350)
	randomX = random.randint(-350, 350)
	snake.setposition(randomX, randomY)


# Create the robot
robot = turtle.Turtle()
robot.color("blue")
robot.shape("robot_bot.gif")
robot.penup()
robot.speed(0)
robot.setposition(0,-250)

# Create apple
NUMBER_APPLES = 3
apples = []
for i in range(NUMBER_APPLES):
	apples.append(turtle.Turtle())

for apple in apples:
	apple.color("red")
	apple.shape("apple.gif")
	apple.penup()
	apple.speed(0)
	randomY = random.randint(-350, 350)
	randomX = random.randint(-350, 350)
	apple.setposition(randomX, randomY)
	while check_collision(holes, apple, 100) or check_collision(waters, apple, 100):
		randomY = random.randint(-350, 350)
		randomX = random.randint(-350, 350)
		apple.setposition(randomX, randomY)

# Create food sense

# Move robot left
def move_left(target):
	#robot.setheading(-180)
	if target == robot:
		robot.shape("robot_lef.gif")
	x = target.xcor()
	x -= robotspeed
	if x < -380:
		x = -380
	target.setx(x)

# Move robot right
def move_right(target):
	#target.setheading(0)
	if target == robot:
		robot.shape("robot_rig.gif")
	x = target.xcor()
	x += robotspeed
	if x > 380:
		x = 380
	target.setx(x)

# Move robot up
def move_up(target):
	#target.setheading(90)
	if target == robot:
		robot.shape("robot_top.gif")
	y = target.ycor()
	y += robotspeed
	if y > 380:
		y = 380
	target.sety(y)

# Move robot down
def move_down(target):
	#target.setheading(270)
	if target == robot:
		robot.shape("robot_bot.gif")
	y = target.ycor()
	y -= robotspeed
	if y < -380:
		y = -380
	target.sety(y)

def trespass_perimeter(tile, targets, target_height = 100, target_width = 100):
	for target in targets:
		if (tile.xcor() >= target.xcor()) and (tile.ycor() >= target.ycor()):
			if (tile.xcor() <= target.xcor()+target_width) and (tile.ycor() <= target.ycor()+target_height):
				return True
		else:
			return False

# Create print pen
print_pen = turtle.Turtle()
print_pen.speed(0)
print_pen.color("white")
print_pen.penup()
print_pen.setposition(-380, 350)

# Text on screen
def print_text(hunger, intention_idx):
	print_pen.clear()
	intention_string = intention[intention_idx]
	hunger_string = str(int(floor(hunger)))
	printstring = "Intention: "+intention_string+"\nHunger: "+hunger_string
	print_pen.write(printstring, False, align="left", font=("Arial", 14, "normal"))
	print_pen.hideturtle()

print_history_pen = turtle.Turtle()
print_history_pen.speed(0)
print_history_pen.color("white")
print_history_pen.penup()
print_history_pen.setposition(380, 350)

print_history_pen_two = turtle.Turtle()
print_history_pen_two.speed(0)
print_history_pen_two.color("white")
print_history_pen_two.penup()
print_history_pen_two.setposition(380, 334)

print_history_pen_three = turtle.Turtle()
print_history_pen_three.speed(0)
print_history_pen_three.color("white")
print_history_pen_three.penup()
print_history_pen_three.setposition(380, 318)

def print_history(intention_history):
	print_history_pen.clear()
	print_history_pen_two.clear()
	print_history_pen_three.clear()

	printstring = intention_history[2]
	print_history_pen.write(printstring, False, align="right", font=("Arial", 14, "normal"))

	printstring = intention_history[1]
	print_history_pen_two.write(printstring, False, align="right", font=("Arial", 12, "normal"))

	printstring = intention_history[0]
	print_history_pen_three.write(printstring, False, align="right", font=("Arial", 10, "normal"))

	print_history_pen.hideturtle()
	print_history_pen_two.hideturtle()
	print_history_pen_three.hideturtle()
"""
def print_history(intention_history):
	print_history_pen.clear()
	printstring = "["+intention_history[0]+", "+intention_history[1]+", "+intention_history[2]+"]"
	print_history_pen.write(printstring, False, align="right", font=("Arial", 14, "normal"))
	print_history_pen.hideturtle()
"""
# Find Apple
def find_apple(robot, apples, goal, smell_sense):
	for apple in apples:
		if robot.distance(apple) <= smell_sense/2:
			goal = [apple.xcor(), apple.ycor(), 0]
	return goal

# Action for intentions
def free_walk(robotpos):
	distance = random.randint(40, 240)
	direction = random.randint(1,4) # U R D L
	idle = random.randint(250,750)
	x_pos, y_pos = robotpos
	if direction == 1:
		y_pos += distance
		if y_pos > 380:
			y_pos = 380
	elif direction == 3:
		y_pos -= distance
		if y_pos < -380:
			y_pos = -380
	elif direction == 2:
		x_pos += distance
		if x_pos > 380:
			x_pos = 380
	else:
		x_pos -= distance
		if x_pos < -380:
			x_pos = -380
	goal = [x_pos, y_pos, idle]
	return goal

def find_food(robotpos):
	smallest_distance = 1000
	if len(apples) <= 0:
		goal = [0, 0, 0]
		return goal
	for apple in apples:
		if smallest_distance > robot.distance(apple):
			smallest_distance = robot.distance(apple)
			x_pos = apple.xcor()
			y_pos = apple.ycor()
	idle = 0
	goal = [x_pos, y_pos, idle]
	return goal

def eat(hunger, intention_idx):
	for apple in apples:
		if robot.distance(apple) == 0:
			new_y = random.randint(-380, 380)
			new_x = random.randint(-380, 380)
			apple.hideturtle()
			reduce_count = REDUCE_HUNGER
			while (reduce_count > 1) and hunger > 1:
				reduce_count -= 1
				hunger -= 1
				print_text(hunger, intention_idx)
				sleep(2.0/REDUCE_HUNGER)
			apples.remove(apple)
	return hunger

def update_history(idx, history):
	if history[-1] != intention[idx]:
		history.append(intention[idx])
		history = history[1:]
		print_history(history)
	return history

def explosion():
	robot.shape("explosion-gif/frame_08_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_09_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_10_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_11_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_12_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_13_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_14_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_15_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_16_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_00_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_01_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_02_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_03_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_04_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_05_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_06_delay-0.01s.gif")
	sleep(0.05)
	robot.shape("explosion-gif/frame_07_delay-0.01s.gif")
	sleep(0.05)
	robot.hideturtle()

def move_snake_2_goal(snake_goal):
	if snake.xcor() > snake_goal[POSX]:
		move_left(snake)
	elif snake.xcor() < snake_goal[POSX]:
		move_right(snake)
	elif snake.xcor() == snake_goal[POSX]:
		if snake.ycor() > snake_goal[POSY]:
			move_down(snake)
		elif snake.ycor() < snake_goal[POSY]:
			move_up(snake)

# Initializing positions and intention
something = 0
robotpos = [robot.xcor(), robot.ycor()]
goal = free_walk(robotpos)
last_state = [0, 0]

print_text(hunger, intention_idx)
print_history(intention_history)

snakes = []
snakes.append(snake)

min_dist = 1000
# SET SNAKE'S GOAL TO NEAREST APPLE
for apple in apples:
	if min_dist > snake.distance(apple):
		min_dist = snake.distance(apple)
		snake_goal = [apple.xcor(), apple.ycor()]

sleep(1)

# Main loop
while True:
	robotpos = [robot.xcor(), robot.ycor()]

	"""
		TODO: Fix
	"""
	# COLLISION CHECKING
	"""if check_collision(waters, robot, 50):
		explosion()
	elif check_collision(holes, robot):
		explosion()
	elif check_collision(snakes, robot, 10):
		explosion()
"""
	if trespass_perimeter(robot, waters) or \
	trespass_perimeter(robot, holes) or \
	trespass_perimeter(robot, snakes, 80, 90):
		explosion()

	# MOVE SNAKE
	if snake.ycor() > robot.ycor():
		if abs(snake.xcor() -robot.xcor()) <= 10 and abs(snake.distance(robot) < 200):
			move_down(snake)
		else:
			move_snake_2_goal(snake_goal)
	else:
		move_snake_2_goal(snake_goal)

	# CHECK HUNGER
	if hunger >= 100:
		explosion()
	elif hunger > 50 and hunger < 100:
		intention_idx = FINDFOOD
	else:
		intention_idx = FREEWALK

	if reachgoal and goal[IDLE] == 0:
		if intention_idx == FINDFOOD:
			goal = find_food(robotpos)
			reachgoal = False
		elif goal[IDLE] == 0:
			goal = free_walk(robotpos)
			reachgoal = False

	if intention_idx == FINDFOOD and not reachgoal:
		goal = find_apple(robot, apples, goal, smell_sense = MAX_RADIUS)
	elif intention_idx == FREEWALK and not reachgoal:
		goal = find_apple(robot, apples, goal, smell_sense = MIN_RADIUS)

	# MOVE TOWARDS A GOAL or WAIT
	if robotpos[POSX] == goal[POSX] and robotpos[POSY] == goal[POSY]:
		if goal[IDLE] > 0:
			goal[IDLE] -= 1
			sleep(0.001)
		else:
			reachgoal = True
	elif robot.xcor() > goal[POSX]:
		move_left(robot)
	elif robot.xcor() < goal[POSX]:
		move_right(robot)
	elif robot.xcor() == goal[POSX]:
		if robot.ycor() > goal[POSY]:
			move_down(robot)
		elif robot.ycor() < goal[POSY]:
			move_up(robot)

	# UPDATE HUNGER AND INTENTION
	if check_collision(apples, robot):
		intention_idx = EAT
		intention_history = update_history(intention_idx, intention_history)
		hunger = eat(hunger, intention_idx)
	if intention_idx == FREEWALK:
		hunger += 0.003
	elif intention_idx == FINDFOOD:
		hunger += 0.005
	if hunger > 100:
		hunger = 100

	# PRINT INFO
	if (floor(hunger) != floor(last_state[0])) or (intention_idx != last_state[1]) :
		print_text(hunger, intention_idx)
	intention_history = update_history(intention_idx, intention_history)

	last_state = [hunger, intention_idx]

	sleep(0.001)

# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(move_up, "Up")
turtle.onkey(move_down, "Down")

delay = raw_input("Press enter to finish")
