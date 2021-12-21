# CSCE 452 Mini Project 4 "Driving Simulator for Porsche 911 Carrera (2019 Model)"

![alt text](https://github.tamu.edu/yk7335/CSCE-452/blob/master/Project%204/GuiPicture.PNG?raw=true)

## Overview:

This application mimics a race track. we have a local and global track. The global track tracks where the car is at on the track. This is indicated by the red dot on our big track. The local track shows the top down view of the car (basically a zoomed in version of the global map). 

The movement of the car is done by moving the background around the vehicle. While we do this we rotate the tire and the base vehicle so that the movement is smooth and looks natural. The vehicle is split into three parts the right, and left wheels, and the base of the vehicle. The followed the Ackerman Steering model to calculate our angles of rotation.

The replay button allows you to see the movements previously made by the car. When the replay button is pressed, the command is run which sets car.replay  to True. When moveVehicle() detects that, it goes through an array (changed it from a csv file because I couldn't figure out how to close and reopen the file) and updates every car variable that was stored in the array. It then runs what moveVehicle() typically runs 

## How to Run:
Download Project 4 folder  
Run the command: `python3 main.py`

## Contributors:
Travis Abel, Yash Kalyani, Karim Zaher, Alex Lin, Nate Krall

## Instructors:
Dr. Dezhen Song, Shu-Hao (Eric) Yeh
