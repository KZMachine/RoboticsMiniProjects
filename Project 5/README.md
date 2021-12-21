# CSCE 452 Mini Project 5 "Robot Motion Planning"

![alt text](https://github.tamu.edu/yk7335/CSCE-452/blob/master/Project%205/Project5_Picture.PNG?raw=true)

## Overview:  

We were tasked to create a path finding algorithm with the landscapr known to us. We were told to complete this using cell decomposition. The following statements explain what, and how our project was built. It also inlcudes some important functions and what they do.  

Our path finding algorithm used cell decomposition method. We break up the area into subsections. We do this by drawing lines and the lines never intersect the blockades. We then place midpoints on the lines that would esentially create a path for the robot to go to the destination without running into the blockades.  

We also used the A-star method to search through all the points and pick the most opitimized path. To do this we had to store each node or point on the lines in an array and use them to traverse through.  

Some important funcitons:  

def moveRobot(x, y): This function takes x and y positions and moves the robot to that position. This funciton is used after we find the path.  

def beginProcess(): This function breaks the area down into cells. The cells are our area. Here we make sure the lines that we draw never interesect the area of the square. We also draw midpoints of each line.  

def drawOnFrame(choice, x, y): This function lets your draw or move around the robot, all the boxes, and the destination.  

def EraseAll(): Gets rid of everything on the Enviroment canvas.

We also have all these in a class called cell. This cell class is what our area gets split into. It's basically a rectangle that splits the enviorment into pieces.

## How to Run:
Download Project 5 folder  
Run the command: `python3 main.py`

## Contributors:
Travis Abel, Yash Kalyani, Karim Zaher, Alex Lin, Nate Krall

## Instructors:
Dr. Dezhen Song, Shu-Hao (Eric) Yeh
