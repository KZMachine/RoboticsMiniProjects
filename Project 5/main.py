from tkinter import *
import math


root=Tk()
root.title('Robot Motion Planning')
root.geometry("770x515")
root.config(bg="maroon")

# Environment
Environment_frame = Canvas(root, width=500, height=500)
Environment_frame.grid(row=0, column=0)
Environment_frame.config(bg="white")

# Control frame
Control_frame = Frame(root, width=250, height=500)
Control_frame.grid(row=0, column=1,sticky="nsew")
Control_frame.pack_propagate(False)

# Title
Title = Label(Control_frame, text = "Robot Motion Planning",font='Helvetica 12 bold')
Title.pack(side=TOP)

click = Label(Control_frame, text = "Select & Right Click to draw",font='Helvetica 12').place(x = 30, y = 40)

def getSelected(e):
    e = draw.get()
    print(e)


draw = StringVar() # default value
WhatToDraw = ["Robot", "Block1", "Block2", "Block3", "Destination"]
drawWhat = OptionMenu(root, draw, *WhatToDraw, command=getSelected)
drawWhat_place = drawWhat.place(x = 600, y = 80)

alllabel = []
def EraseAll():
	#Environment_frame.delete('robot', 'Block1', 'Block2', 'Block3', 'Destination')
	Environment_frame.delete('all')
	for label in alllabel:
		label.destroy()
	allCells.clear()

allCells = []

class Cell():
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		#Variables for A*
		self.f = 0
		self.g = 0
		self.h = 0
		self.parent = None

		self.number = len(allCells)
		Environment_frame.create_rectangle(x1, y1, x2, y2)
		if(self.number != 0):
			self.label = Label(Environment_frame, text = self.number, font='Helvetica 12')
			self.label.place(x = self.x1 + 0, y = self.y1 + 0)
			alllabel.append(self.label)
		ymidpoint = (y1+y2)/2 # need to make sure it's not in the square
		xmidpoint = (x1+x2)/2
		self.midpoint = (xmidpoint, ymidpoint)
		Environment_frame.create_oval(x1-5, ymidpoint-5, x1+5, ymidpoint+5,fill="green")
		Environment_frame.create_oval(x2-5, ymidpoint-5, x2+5, ymidpoint+5,fill="green")
		self.nextCells = []
		self.nextNode = []

		if self.x1 != 0:
			for cell in allCells:
				if cell.x2 == self.x1 + 5 and ((cell.y1 >= self.y1 + 5 and cell.y1 <= self.y2 + 5 ) or (cell.y2 >= self.y1 +5  and cell.y2 <= self.y2 +5)):
					cell.nextCells.append(self.number)
					self.nextCells.append(cell.number)
					cell.nextNode.append(self)
					self.nextNode.append(cell)


def moveRobot(x, y):
	if x == robotPosition[0] and y == robotPosition[1]:
		pass
	else:
		xDistance = x - robotPosition[0]
		yDistance = y - robotPosition[1]
		angle = math.atan2(yDistance, xDistance)
		x_move = math.cos(angle)
		y_move = math.sin(angle)
		robotPosition[0] += x_move
		robotPosition[1] += y_move
		Environment_frame.create_oval(robotPosition[0]-5, robotPosition[1]-5, robotPosition[0]+5, robotPosition[1]+5,fill="red")
		if abs(xDistance) > 2 or abs(yDistance) > 2:
			# root.after(100, lambda: moveRobot(x, y))
			moveRobot(x, y)		
def distance(point1, point2):
	return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def beginProcess():
	global xBoundaries
		
	xBoundaries = [blockPosition[0][0] - 100, blockPosition[1][0] - 75,
				blockPosition[2][0] - 50, blockPosition[0][0] + 100, 
				blockPosition[1][0] + 75, blockPosition[2][0] + 50]
	xBoundaries.append(500)
	xBoundaries.append(0)
	xBoundaries_set = sorted(set(xBoundaries))
	print(xBoundaries_set)

	print(robotPosition, destinationPosition)
	for i in range(0, len(xBoundaries_set)):
		if i == 0:
			continue

		#X boundaries of cells are xBoudaries_set[i] and i-1
		#Determine Y boundaries by checking if there are boxes intersecting the x

		yBoundariesOnX_set = []
		if xBoundaries_set[i] > blockPosition[0][0] - 100 and xBoundaries_set[i] <= blockPosition[0][0] + 100:
			yBoundariesOnX_set.append(blockPosition[0][1] + 100)
			yBoundariesOnX_set.append(blockPosition[0][1] - 100)
		if xBoundaries_set[i] > blockPosition[1][0] - 75 and xBoundaries_set[i] <= blockPosition[1][0] + 75:
			yBoundariesOnX_set.append(blockPosition[1][1] + 75)
			yBoundariesOnX_set.append(blockPosition[1][1] - 75)
		if xBoundaries_set[i] > blockPosition[2][0] - 50 and xBoundaries_set[i] <= blockPosition[2][0] + 50:
			yBoundariesOnX_set.append(blockPosition[2][1] + 50)
			yBoundariesOnX_set.append(blockPosition[2][1] - 50)
		
		yBoundariesOnX_set.append(0)
		yBoundariesOnX_set.append(500)

		yBoundariesOnX_set = sorted(set(yBoundariesOnX_set))

		print("X: " + str(xBoundaries_set[i]) + " Y bounds: " + str(yBoundariesOnX_set))

		#totalYBOunds_set = sorted(set(yBoundariesOnX_set + prevYBounds_set))
		totalYBOunds_set = sorted(set(yBoundariesOnX_set))

		print("X: " + str(xBoundaries_set[i]) + " Y bounds total: " + str(totalYBOunds_set))

		for j in range(0, len(totalYBOunds_set), 2):
			newCell = Cell(xBoundaries_set[i - 1], totalYBOunds_set[j], xBoundaries_set[i], totalYBOunds_set[j + 1])
			allCells.append(newCell)

		prevYBounds_set = yBoundariesOnX_set
	for cell in allCells:
		print("Number: " + str(cell.number) + " next: " + str(cell.nextCells))
	# check cell adjacency
	#find start and end cells
	# starting_cell = Cell()
	# ending_cell = -1
	for cell in allCells:
		if (cell.x1 <= robotPosition[0] <=  cell.x2) and (cell.y1 <= robotPosition[1] <=  cell.y2):
			starting_cell = cell
		if (cell.x1 <= destinationPosition[0] <=  cell.x2) and (cell.y1 <= destinationPosition[1] <=  cell.y2):
			ending_cell = cell
	print("Starting Cell: {}\nEnding Cell: {}".format(starting_cell.number, ending_cell.number))

	#dfs
	visitedNodes = []
	toVisitQueue = []
	toVisitQueue.append(starting_cell.number)
	while len(toVisitQueue):
		if toVisitQueue[0] == ending_cell.number:
			print("Goal")
			print(toVisitQueue[0])
			break
		if toVisitQueue[0] not in visitedNodes:
			visitedNodes.append(toVisitQueue[0])
			print(toVisitQueue[0])
			for num in allCells[toVisitQueue[0]].nextCells:
				if num not in visitedNodes:
					toVisitQueue.append(num)
					allCells[num].parent = allCells[toVisitQueue[0]]
			
		toVisitQueue.pop(0)

	print("Done")

	parents = [ending_cell.number]

	par = ending_cell.parent
	while par.number != starting_cell.number:
		parents.append(par.number)
		par = par.parent
	parents.append(par.number)

	parents = parents[::-1]

	if allCells[parents[0]].x1 < allCells[parents[1]].x1:
		moveRobot(allCells[parents[1]].x1, robotPosition[1])

	#maybe if start to right of

	#if allCells[parents[0]].x1 > allCells[parents[1]].x1:
		#moveRobot(allCells[parents[1]].x1, robotPosition[1])

	while len(parents) != 1:
		moveRobot(robotPosition[0], allCells[parents[1]].y1)
		parents.pop(0)
		if len(parents) != 1:
			moveRobot(allCells[parents[1]].x1, robotPosition[1])

	moveRobot(destinationPosition[0], destinationPosition[1])
	#par = allCells[ending_cell.number]
	#while par.number != starting_cell.number:
		#print(par.number)
		#par = allCells[allCells[par.number].parent]




StartButton = Button(Control_frame, text="Start",width=17, command = beginProcess) 
StartButton.pack(side=BOTTOM, pady=10)

EraseButton = Button(Control_frame, text="Erase All",width=17, command = EraseAll) 
EraseButton.pack(side=BOTTOM, pady=10)

global blockPosition
blockPosition = [[], [], []]
global robotPosition
robotPosition = []
global destinationPosition
destinationPosition = []

def drawOnFrame(choice, x, y):
	# Need to get the mouse position from key(), and shape selected from getSelected()
	# pass
	if choice == "Robot":
		r = 5
		Environment_frame.delete("robot")
		Environment_frame.create_oval(x-r, y-r, x+r, y+r,fill="red", tags='robot')
		global robotPosition
		robotPosition = [x, y]

	elif choice == "Destination":
		r = 5
		Environment_frame.delete("Destination")
		Environment_frame.create_oval(x-r, y-r, x+r, y+r,fill="blue", tags='Destination')
		global destinationPosition
		destinationPosition = [x, y]

	elif choice == "Block1":
		r = 100   # size is 200
		Environment_frame.delete("Block1")
		Environment_frame.create_rectangle(x-r, y-r, x+r, y+r, fill="black", tags='Block1')
		blockPosition[0] = [x, y]

	elif choice == "Block2":
		r = 75   # size is 150
		Environment_frame.delete("Block2")
		Environment_frame.create_rectangle(x-r, y-r, x+r, y+r, fill="gray", tags='Block2')
		blockPosition[1] = [x, y]

	elif choice == "Block3":
		r = 50   # size is 100
		Environment_frame.delete("Block3")
		Environment_frame.create_rectangle(x-r, y-r, x+r, y+r, fill="brown", tags='Block3')
		blockPosition[2] = [x, y]
	
	



 
def key(event):
	x, y = event.x, event.y
	print(x," ",y)
	drawOnFrame(draw.get(), x, y)

	#drawOnFrame("Robot", 400, 100)
	#drawOnFrame("Destination", 100, 450)
	drawOnFrame("block5", 110, 300)
	#drawOnFrame("Block2", 300, 100)
	#drawOnFrame("Block3", 400, 300)
	#Environment_frame.create_line(10,20,40,50)
	# how you create a line x1,y1 to x2,y2 

root.bind('<Button-3>', key) # right click 



root.update()
root.mainloop()

