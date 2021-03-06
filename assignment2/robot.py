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
ROBOT_HEIGHT = 28
ROBOT_WIDTH = 23
SNAKE_HEIGHT = 85
SNAKE_WIDTH = 75

# Variables
intention_idx = 0
hunger = 40 #random.randint(0, 25)
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

def trespass_perimeter(targets, tile, target_height = None, target_width = None, tile_height = None, tile_width = None):
	X = 0
	Y = 1

	if (target_height is None):
		target_height = 100
	if (target_width is None):
		target_width = 100
	if (tile_height is None):
		tile_height = 100
	if (tile_width is None):
		tile_width = 100

	for target in targets:
		# ADJUST COORDINATES FROM CENTER TO BOTTOM LEFT
		tile_x = tile.xcor() - int(tile_width / 2)
		tile_y = tile.ycor() - int(tile_height / 2)
		target_x = target.xcor() - int(target_width / 2)
		target_y = target.ycor() - int(target_height / 2)

		target_tl = (target_x, target_y + target_height)
		target_br = (target_x + target_width, target_y)

		tile_tl = (tile_x, tile_y + tile_height)
		tile_br = (tile_x + tile_width, tile_y)

		if (tile_tl[X] > target_br[X]) or (target_tl[X] > tile_br[X]):
			return False

		if (tile_tl[Y] < target_br[Y]) or (target_tl[Y] < tile_br[Y]):
			return False

		DEBUGGER = False
		if DEBUGGER:
			ST = 1
			ddb = turtle.Turtle()
			ddb.ht()
			ddb.circle(20)
			ddb.color("brown")
			ddb.st()
			ddb.setposition(tile_x, tile_y)
			ddb.pendown()
			wn.update()
			sleep(ST)

			ddb.setposition(tile_x + tile_width, tile_y)
			wn.update()
			sleep(ST)

			ddb.setposition(tile_x + tile_width, tile_y + tile_height)
			wn.update()
			sleep(ST)

			ddb.setposition(tile_x, tile_y + tile_height)
			wn.update()
			sleep(ST)

			ddb.penup()
			ddb.color("purple")
			ddb.st()
			ddb.setposition(target_x, target_y)
			ddb.pendown()
			wn.update()
			sleep(ST)

			ddb.setposition(target_x + target_width, target_y)
			wn.update()
			sleep(ST)

			ddb.setposition(target_x + target_width, target_y + target_height)
			wn.update()
			sleep(ST)

			ddb.setposition(target_x, target_y + target_height)
			wn.update()
			sleep(ST)
			ddb.ht()
			ddb.penup()

		return True

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
NUMBER_WATERS = random.randint(1, 2)
position_list = generate_water_position(NUMBER_WATERS)
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
	water.setposition(randomX, randomY)
	position_list = position_list[1:]

# Create holes
NUMBER_HOLES = 1
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
	while trespass_perimeter(waters, hole):
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
while trespass_perimeter(waters, snake) or trespass_perimeter(holes, snake):
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
	while trespass_perimeter(holes, apple, 100, 100, 24, 27) or \
	trespass_perimeter(waters, apple, 100, 100, 24, 27):
		randomY = random.randint(-350, 350)
		randomX = random.randint(-350, 350)
		apple.setposition(randomX, randomY)

# Move robot left
def move_left(target):
	if target == robot:
		robot.shape("robot_lef.gif")
	x = target.xcor()
	x -= robotspeed
	if x < -380:
		x = -380
	target.setx(x)

# Move robot right
def move_right(target):
	if target == robot:
		robot.shape("robot_rig.gif")
	x = target.xcor()
	x += robotspeed
	if x > 380:
		x = 380
	target.setx(x)

# Move robot up
def move_up(target):
	if target == robot:
		robot.shape("robot_top.gif")
	y = target.ycor()
	y += robotspeed
	if y > 380:
		y = 380
	target.sety(y)

# Move robot down
def move_down(target):
	if target == robot:
		robot.shape("robot_bot.gif")
	y = target.ycor()
	y -= robotspeed
	if y < -380:
		y = -380
	target.sety(y)

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
	search_animation()
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
	pos = (robot.xcor() + 60, robot.ycor() + 20)
	robot.setposition(pos)
	robot.shape("explosion-gif/frame_08_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_09_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_10_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_11_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_12_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_13_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_14_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_15_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_16_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_00_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_01_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_02_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_03_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_04_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_05_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_06_delay-0.01s.gif")
	wn.update()
	sleep(0.05)
	robot.shape("explosion-gif/frame_07_delay-0.01s.gif")
	wn.update()
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

def search_animation():
	robot.shape("robot_lef.gif")
	wn.update()
	sleep(1)
	robot.shape("robot_rig.gif")
	wn.update()
	sleep(1)
	robot.shape("robot_bot.gif")
	wn.update()
	sleep(1)
	robot.shape("robot_top.gif")
	wn.update()
	sleep(1)

def draw_debugger(targets, color, target_width = 100, target_height = 100):
	ST = 0.33
	for target in targets:
		target_x = target.xcor() - int(target_width / 2)
		target_y = target.ycor() - int(target_height / 2)

		ddb = turtle.Turtle()
		ddb.ht()
		ddb.circle(20)
		ddb.color(color)
		ddb.st()
		ddb.setposition(target_x, target_y)
		ddb.pendown()
		wn.update()
		sleep(ST)

		ddb.setposition(target_x + target_width, target_y)
		wn.update()
		sleep(ST)

		ddb.setposition(target_x + target_width, target_y + target_height)
		wn.update()
		sleep(ST)

		ddb.setposition(target_x, target_y + target_height)
		wn.update()
		sleep(ST)

		ddb.setposition(target_x, target_y)
		wn.update()
		sleep(ST)
		ddb.ht()
		ddb.penup()
		#ddb.clear()



# Initializing positions and intention
something = 0
robotpos = [robot.xcor(), robot.ycor()]
goal = free_walk(robotpos)
last_state = [0, 0]

print_text(hunger, intention_idx)
print_history(intention_history)

snakes = []
snakes.append(snake)

robots = []
robots.append(robot)

min_dist = 1000
# SET SNAKE'S GOAL TO NEAREST APPLE
for apple in apples:
	if min_dist > snake.distance(apple):
		min_dist = snake.distance(apple)
		snake_goal = [apple.xcor(), apple.ycor() + SNAKE_HEIGHT]
		snakes_apple = (apple.xcor(), apple.ycor())
sleep(0.7)

# Main loop
while True:
	robotpos = [robot.xcor(), robot.ycor()]

	# COLLISION CHECKING
	if trespass_perimeter(waters, robot, 100, 100, ROBOT_HEIGHT, ROBOT_WIDTH) or \
	trespass_perimeter(holes, robot, 100, 100, ROBOT_HEIGHT, ROBOT_WIDTH) or \
	trespass_perimeter(snakes, robot, SNAKE_HEIGHT, SNAKE_WIDTH, ROBOT_HEIGHT, ROBOT_WIDTH):
		DEBUGGER = False
		if DEBUGGER:
			draw_debugger(robots, "red", ROBOT_HEIGHT, ROBOT_WIDTH)
			draw_debugger(waters, "yellow", 100, 100)
			draw_debugger(holes, "pink", 100, 100)
			draw_debugger(snakes, "white", SNAKE_HEIGHT, SNAKE_WIDTH)

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

	# CHECK IF THE APPLE IS CLOSE TO THE SNAKE
	if intention_idx == FINDFOOD:
		for apple in apples:
			if apple.position() == snakes_apple:
				if goal[POSX] == snakes_apple[POSX] and goal[POSY] == snakes_apple[POSY]:
					if robot.distance(apple) <= 100:
						sleep(3)
						apples.remove(apple)
						goal = find_food(robotpos)

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
