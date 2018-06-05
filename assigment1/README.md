# Theme for the first report

* Make a video in which one or more objects move as if they have intention
* The lenght: longer than 1 minute
* Method: no restriction, i.e: using physical simulator, writing a program to generate it, using software to generate animation
* Submit the video and presentation slides
	* The deadline is 23:59 14th June, 2018


### Presentation

* 15th June (and 22nd June)
* Prepare 5 min presentation in English
	* Show the video
	* Explain a cover story for the video.
	* Explain what intentional behaviors we can observe.
	* Shows the point of how you want me to evaluate the video.
	* Show the video again.

-----

# The Project

The following assignment was made using Python 2.7 for the course of DESIGN OF PHYSICALLY GROUNDED COMMUNICATION SYSTEM of the Graduate School of Open and Environmental Systems of Keio University.

### The Hungry Robot

**robot.py** contains the files for the assignment and has the following dependencies: Python 2.7 and Turtle.

The robot has the ability to eat apples and look for apples in the surroundings. The longer the time passes, the hungrier the robot gets. Most importantly, it has three intentions: free walk, find food and eat food. The initial state and intention of the robot is **free walk**, which means the robot will walk freely (randomly) across the border, with IDLE_TIME between each run. As soon as its hungry level achieves over 50%, it will become hungrier, it will not rest until it finds the apple.
