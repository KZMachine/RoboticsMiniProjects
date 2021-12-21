from tkinter import *
from vehicle import *
import math
from random import randrange
from PIL import Image
import csv
import time
replayHistory = []



root=Tk()
root.title('Driving Simulator')
root.geometry("1395x705")
root.config(bg="maroon")

# Global Frame
global_frame = Canvas(root, width=1010, height=690)
global_frame.grid(row=0, column=1, padx=2.5, pady=5)
global_frame.config(bg="black")
img = PhotoImage(file = "Images/GlobalTrack.png")
global_frame.create_image(0,0, anchor=NW, image=img)

# Control frame
frame = Frame(root, width=350, height=690)
frame.grid(row=0, column=0, padx=5, pady=5,sticky="nsew")
frame.pack_propagate(False)

# Control frame
control_frame = Frame(frame, width=350, height=370)
control_frame.grid(row=0, column=0, padx=5,sticky="nsew")
control_frame.pack_propagate(False)

# Local frame
local_frame = Canvas(frame, width=350, height=320)
local_frame.grid(row=1, column=0, padx=5,sticky="nsew")
local_frame.config(bg="gray")
#img2 = PhotoImage(file = "Images/GlobalTrack.png")
#local_frame.create_image(0,0, anchor=NW, image=img2)
#local_frame.pack_propagate(False)


# Title
Title = Label(control_frame, text = "Driving Simulator - TAMU 2021",font='Helvetica 12 bold')
Title.pack(side=TOP)


####################################### Steering Control #######################################
alphaRight=DoubleVar()

def getAlphaRight(event):
    print(alphaRight.get())
    # return alphaRight.get()

Direction_label = Label(control_frame, text = "Direction Control", font='Helvetica 12 bold').place(x = 105, y = 40)
Direction = Scale(control_frame, from_= -30, to= 30, orient='horizontal',length = 250, variable=alphaRight, command = getAlphaRight).place(x = 50, y = 60)

####################################### Global Map -- Car #######################################
# globalVehicle = globalMapVehicle(global_frame)
car = Vehicle(global_frame, local_frame)
steeringBackLog = 0
####################################### Local Map -- Car ########################################
####################################### Velocity Control #######################################
V_FR = 0.0
V_FL = 0.0
V_BR = 0.0
V_BL = 0.0
V_Overall = 0.0

def changeDisplayLabel(overall, V_FL, V_FR, V_BL, V_BR):
    alpha_right = car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation
    alpha_left = car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation
    G = car.globalMapVehicle.LocalMapVehicle.LocalCar.g
    D = car.globalMapVehicle.LocalMapVehicle.LocalCar.two_d / 2
    R = car.globalMapVehicle.LocalMapVehicle.LocalCar.r
    angular_vel = (car.Velocity * math.sin(math.radians(alpha_right))) / G

    # Need to be modified
    #overall["text"] = str(car.Velocity)
    V_FL["text"] = str((angular_vel*G)/math.sin(math.radians(alpha_left)))[0:4]
    V_FR["text"] = str(car.Velocity)
    V_BL["text"] = str(angular_vel*(R+D))[0:4]
    V_BR["text"] = str(angular_vel*(R-D))[0:4]
    overall["text"] = str(angular_vel*G)[0:4]

def Accelerate(overall, V_FL, V_FR, V_BL, V_BR):
    if car.Velocity < 200:
        car.Velocity += 1
    changeDisplayLabel(overall, V_FL, V_FR, V_BL, V_BR)

def Decelerate(overall, V_FL, V_FR, V_BL, V_BR):
    if car.Velocity > -5:
        car.Velocity -= 1
    changeDisplayLabel(overall, V_FL, V_FR, V_BL, V_BR)

def moveVehicle():
    if car.replay and car.replayStep < len(replayHistory)-1:
        # print(data)
        car.globalMapVehicle.X = float(replayHistory[car.replayStep][0])
        car.globalMapVehicle.Y = float(replayHistory[car.replayStep][1])
        car.Orientation = float(replayHistory[car.replayStep][2])
        car.Velocity = float(replayHistory[car.replayStep][3])
        car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation = float(replayHistory[car.replayStep][4])
        car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation = float(replayHistory[car.replayStep][5])
        # # if car.Velocity > 0:
        # #     car.Orientation += int(alphaRight.get())
        # # elif car.Velocity < 0:
        # #     car.Orientation -= int(alphaRight.get())
        calculatedX = (-car.Velocity / 10) * math.cos(math.radians(car.Orientation))
        calculatedY = (-car.Velocity / 10) * math.sin(math.radians(car.Orientation))

        car.replayStep += 1
        car.globalMapVehicle.moveCircle(car.globalMapVehicle.X - calculatedX, car.globalMapVehicle.Y - calculatedY, int(replayHistory[car.replayStep][6]), car.Orientation)
        root.after(100, moveVehicle)
        if car.replayStep >= len(replayHistory) - 1:
            print("Replay over, shutting down window")
            exit()
        
    else:
        replayHistory.append([car.globalMapVehicle.X,car.globalMapVehicle.Y,car.Orientation, car.Velocity, car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation, car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation, int(alphaRight.get())])
        if car.Velocity > 0:
            car.Orientation += int(alphaRight.get())
        elif car.Velocity < 0:
            car.Orientation -= int(alphaRight.get())
        calculatedX = (-car.Velocity / 10) * math.cos(math.radians(car.Orientation))
        calculatedY = (-car.Velocity / 10) * math.sin(math.radians(car.Orientation))
        if car.replay != True:
            car.globalMapVehicle.moveCircle(car.globalMapVehicle.X - calculatedX, car.globalMapVehicle.Y - calculatedY, int(alphaRight.get()), car.Orientation)
        root.after(100, moveVehicle)
        

Velocity_label = Label(control_frame, text = "Velocity Control", font='Helvetica 12 bold').place(x = 110, y = 120)
Minus_Velocity = Button(control_frame, text = "-", width=10, command = lambda: Decelerate(Overall_Velocity_Label,FL_Velocity,FR_Velocity,BL_Velocity,BR_Velocity)).place(x = 80, y = 160)
Plus_Velocity = Button(control_frame, text = "+", width=10, command = lambda: Accelerate(Overall_Velocity_Label,FL_Velocity,FR_Velocity,BL_Velocity,BR_Velocity)).place(x = 180, y = 160)


####################################### Velocity of each wheels #######################################
Velocity_label = Label(control_frame, text = "Velocity", font='Helvetica 12 bold').place(x = 130, y = 200)
V_FL_Label = Label(control_frame, text = "FL: ", font='Helvetica 10 bold').place(x = 80, y = 240)
V_FR_Label = Label(control_frame, text = "FR: ", font='Helvetica 10 bold').place(x = 180, y = 240)
V_BL_Label = Label(control_frame, text = "BL: ", font='Helvetica 10 bold').place(x = 80, y = 270)
V_BR_Label = Label(control_frame, text = "BR: ", font='Helvetica 10 bold').place(x = 180, y = 270)
V_Overall_Label = Label(control_frame, text = "Overall Velocity: ", font='Helvetica 10 bold').place(x = 110, y = 300)

FL_Velocity = Label(control_frame, text = V_FL, font='Helvetica 10 ')
FL_Velocity_Display = FL_Velocity.place(x = 130, y = 240)

FR_Velocity = Label(control_frame, text = V_FR, font='Helvetica 10 ')
FR_Velocity_Display = FR_Velocity.place(x = 230, y = 240)

BL_Velocity = Label(control_frame, text = V_BR, font='Helvetica 10 ')
BL_Velocity_Display = BL_Velocity.place(x = 130, y = 270)

BR_Velocity = Label(control_frame, text = V_BR, font='Helvetica 10 ')
BR_Velocity_Display = BR_Velocity.place(x = 230, y = 270)

Overall_Velocity_Label = Label(control_frame, text = V_Overall, font='Helvetica 10 ')
Overall_Velocity_Place = Overall_Velocity_Label.place(x = 230, y = 300)

####################################### Replay Buttons #######################################
CarHistory = []
def replay(car):
    car.replay = True

Replay_btn = Button(control_frame, text = "Replay", width=18, command = lambda: replay(car)).place(x = 100, y = 330)


####################################### Hotkeys #######################################
history = []
def HotKeyControl():
    for key in history:
        # print(key)
        if key == 37:
            Decelerate(Overall_Velocity_Label,FL_Velocity,FR_Velocity,BL_Velocity,BR_Velocity)
        if key == 39:
            Accelerate(Overall_Velocity_Label,FL_Velocity,FR_Velocity,BL_Velocity,BR_Velocity)
        if key == 40: # down
            if(car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation < 30 and car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation < 30):
                car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation += 0.3
                car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation += (math.atan(car.globalMapVehicle.LocalMapVehicle.LocalCar.g/(car.globalMapVehicle.LocalMapVehicle.LocalCar.r + (car.globalMapVehicle.LocalMapVehicle.LocalCar.two_d/2))))
                car.globalMapVehicle.LocalMapVehicle.LocalCar.updateLocalCar(local_frame)
        if key == 38: # up
            if(car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation > -30 and car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation > -30):
                car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelRightOrientation -= 0.3
                car.globalMapVehicle.LocalMapVehicle.LocalCar.wheelLeftOrientation -= (math.atan(car.globalMapVehicle.LocalMapVehicle.LocalCar.g/(car.globalMapVehicle.LocalMapVehicle.LocalCar.r + (car.globalMapVehicle.LocalMapVehicle.LocalCar.two_d/2))))
                car.globalMapVehicle.LocalMapVehicle.LocalCar.updateLocalCar(local_frame)
    root.after(5, HotKeyControl)

def keyup(e):
    if e.keycode in history :
        history.pop(history.index(e.keycode))

def keydown(e):
    if not e.keycode in history :
        history.append(e.keycode)

root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)
HotKeyControl()

moveVehicle()

root.update()
root.mainloop()