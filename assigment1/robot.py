# Robot program for the Course
# Made by Paulo Dores
# Open source, enjoy using and modifying it!
# Python 2.7 in Ubuntu 16.4

import turtle
import os
import random
from math import floor

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


# Variables
intention_idx = 0
hunger = 25 #random.randint(0, 25) 
hunger_radius = MIN_RADIUS

# Set up the screen

wn = turtle.Screen()
wn.bgcolor("black")
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


# Create food sense
foodsense = turtle.Turtle()
foodsense.color("gray14")
foodsense.shape("circle")
foodsense.penup()
foodsense.resizemode("user")
foodsense.speed(0)
foodsense.shapesize(MIN_RADIUS / STAMP_SIZE)
foodsense.setposition(0,-250)

# Create the robot
robot = turtle.Turtle()
robot.color("blue")
robot.shape("triangle")
robot.penup()
robot.speed(0)
robot.setposition(0,-250)

# Create apple

colors = ['white', 'orange', 'red']

NUMBER_APPLES = 3
apples = []
for i in range(NUMBER_APPLES):
	apples.append(turtle.Turtle())
	
for apple in apples:	
	apple.color(colors[i])
	apple.shape("circle")
	apple.penup()
	apple.speed(0)
	randomY = random.randint(-350, 350)
	randomX = random.randint(-350, 350)
	apple.setposition(randomX, randomY)


# Move robot left
def move_left():
	robot.setheading(-180)
	x = robot.xcor()
	x -= robotspeed
	if x < -380:
		x = -380
	robot.setx(x)
	
# Move robot right
def move_right():
	robot.setheading(0)
	x = robot.xcor()
	x += robotspeed
	if x > 380:
		x = 380
	robot.setx(x)

# Move robot up
def move_up():
	robot.setheading(90)
	y = robot.ycor()
	y += robotspeed
	if y > 380:
		y = 380
	robot.sety(y)

# Move robot down	
def move_down():
	robot.setheading(270)
	y = robot.ycor()
	y -= robotspeed
	if y < -380:
		y = -380
	robot.sety(y)


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


"""
# Print text
def print_text(hunger, intention_idx, goal, robotpos):
	os.system('cls' if os.name =='nt' else 'clear')
	print "Intention: " + intention[intention_idx]
	print "Hunger: " + str(hunger)
	print "Goal: "
	print goal
	print robotpos
	print reachgoal
	print "----------------------------------"
"""

# Find Apple
def find_apple(robot, apples, goal, smell_sense):
	for apple in apples:
		if robot.distance(apple) <= smell_sense/2:
			goal = [apple.xcor(), apple.ycor(), 0]
			robot.color("purple")
	return goal

# Action for intentions
def free_walk(robotpos, foodsense):
	distance = random.randint(40, 240)
	direction = random.randint(1,4) # U R D L
	idle = random.randint(500,1500)
	x_pos, y_pos = robotpos
	foodsense.shapesize(MIN_RADIUS / STAMP_SIZE)
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

def find_food(robotpos, foodsense):
	distance = random.randint(50, 170)
	direction = random.randint(1,4) # U R D L
	idle = 0
	x_pos, y_pos = robotpos
	foodsense.shapesize(MAX_RADIUS / STAMP_SIZE)
	if direction == 1:   # UP
		y_pos += distance
		if y_pos > 380:
			y_pos = 380
	elif direction == 3: # DOWN
		y_pos -= distance
		if y_pos < -380:
			y_pos = -380
	elif direction == 2: # RIGHT
		x_pos += distance
		if x_pos > 380:
			x_pos = 380
	else: 				 # LEFT
		x_pos -= distance
		if x_pos < -380:
			x_pos = -380
	goal = [x_pos, y_pos, idle]
	return goal

def eat(hunger):
	for apple in apples:
		if robot.distance(apple) == 0:
			new_y = random.randint(-380, 380)
			new_x = random.randint(-380, 380)
			apple.setposition(new_x, new_y)
	hunger -= 90
	if hunger < 0:
		hunger = 0
	robot.color("blue")
	return hunger

def check_collision(apples, robot):
	for apple in apples:
		if robot.distance(apple) == 0:
			return True
	return False 		

# Initializing positions and intention
something = 0
robotpos = [robot.xcor(), robot.ycor()]
goal = free_walk(robotpos, foodsense)	
last_state = [0, 0]

print_text(hunger, intention_idx)
	
# Main loop
while True:
	robotpos = [robot.xcor(), robot.ycor()]
	foodsense.setposition(robot.position())
	
	# CHECK HUNGER
	if hunger > 50:
		intention_idx = FINDFOOD
	else:
		intention_idx = FREEWALK
	
	if reachgoal and goal[IDLE] == 0:
		if intention_idx == FINDFOOD:
			goal = find_food(robotpos, foodsense)
			reachgoal = False
		elif goal[IDLE] == 0:
			goal = free_walk(robotpos, foodsense)
			reachgoal = False
	
	if intention_idx == FINDFOOD and not reachgoal:
		goal = find_apple(robot, apples, goal, smell_sense = MAX_RADIUS)
	elif intention_idx == FREEWALK and not reachgoal:
		goal = find_apple(robot, apples, goal, smell_sense = MIN_RADIUS)		
			
	# MOVE TOWARDS A GOAL or WAIT
	if robotpos[POSX] == goal[POSX] and robotpos[POSY] == goal[POSY]:
		if goal[IDLE] > 0:
			goal[IDLE] -= 1
			wn.delay(300)
		else:
			reachgoal = True
	elif robot.xcor() > goal[POSX]:
		move_left()
	elif robot.xcor() < goal[POSX]:
		move_right()
	elif robot.xcor() == goal[POSX]:
		if robot.ycor() > goal[POSY]:
			move_down()
		elif robot.ycor() < goal[POSY]:
			move_up()
	
	# UPDATE HUNGER AND INTENTION
	if check_collision(apples, robot):
		hunger = eat(hunger)  
		intention_idx = EAT
	if intention_idx == FREEWALK:
		hunger += 0.003
	elif intention_idx == FINDFOOD:
		hunger += 0.005
	if hunger > 100:
		hunger = 100
		
	# PRINT INFO
	if (floor(hunger) != floor(last_state[0])) or (intention_idx != last_state[1]) :
		print_text(hunger, intention_idx)
				
	last_state = [hunger, intention_idx]	
	
	wn.delay(100)

# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(move_up, "Up")
turtle.onkey(move_down, "Down")

