from tkinter import *
from PIL import Image, ImageTk
import math
from math import *
import scipy
import numpy as np


class Vehicle:
    def __init__(self, global_frame, local_frame):
        self.X = 500
        self.Y = 500

        self.Velocity = 0
        self.Orientation = 0    # Both the current angle of the steering wheel and its previous angle determine where the car will move next
        self.replay = False
        self.replayStep = 0
        self.FrontWheels = FrontWheels()
        self.BackWheels = BackWheels()

        self.globalMapVehicle = globalMapVehicle(global_frame, local_frame)

class FrontWheels:
    def __init__(self):
        self.Angle = 0

        self.LeftWheel = Wheel()
        self.RightWheel = Wheel()

class BackWheels:
    def __init__(self):
        self.LeftWheel = Wheel()
        self.RightWHeel = Wheel()

class Wheel:
    def __init__(self):
        self.Velocity = 0

class globalMapVehicle:
    def __init__(self, global_frame, local_frame):
        self.X = 505
        self.Y = 135
        self.global_frame = global_frame
        self.redDot = self.global_frame.create_oval(self.X - 5,self.Y - 5, self.X + 5, self.Y + 5, fill="red", tag="Circle")
        self.local_frame = local_frame

        self.LocalMapVehicle = LocalMapVehicle(local_frame, self.X, self.Y)

    def moveCircle(self, xPos, yPos, orientation, spinWHEEE):
        self.global_frame.delete("Circle")
        self.redDot = self.global_frame.create_oval(xPos - 5,yPos - 5, xPos + 5, yPos + 5, fill="red", tag="Circle")
        self.X = xPos
        self.Y = yPos
        self.LocalMapVehicle.updateLocalMap(self.local_frame, self.X, self.Y, orientation, spinWHEEE)

class LocalMapVehicle:
    def __init__(self, local_frame, X, Y):
        self.img2 = PhotoImage(file = "Images/GlobalTrack.png")
        local_frame.create_image(-X + 175, -Y + 175, anchor=NW, image=self.img2)

        self.LocalCar = LocalVehicle(local_frame)

    def updateLocalMap(self, local_frame, X, Y, orientation, spinWHEEE):
        self.img2 = PhotoImage(file = "Images/GlobalTrack.png")
        local_frame.create_image(-X + 175, -Y + 175, anchor=NW, image=self.img2)

        self.LocalCar.updateLocalCar(local_frame, orientation, X, Y, spinWHEEE)

class LocalVehicle:
    def __init__(self, local_frame):
        self.X = 115
        self.Y = 235
        self.bodyOrientation = 270
        self.wheelLeftOrientation = 1 #angle with respect to body coming out of the page
        self.wheelRightOrientation = 1 # angle with respect to body coming out of the page
        self.g = 96.5
        self.two_d = 60
        self.r = (self.g/math.tan(math.radians(self.wheelRightOrientation))) + self.two_d/2
        self.local_frame = local_frame
        resizeFactor = 1
        #Grab these from the properties of the pictures we are using
        bodyWidth = 119
        bodyHeight = 118
        wheelWidth = 38
        wheelHeight = 38

        bodyImage = Image.open("Images/Base3.png")
        bodyImage = bodyImage.resize((math.floor(bodyWidth*resizeFactor), math.floor(bodyHeight*resizeFactor)))
        self.bodyimg = ImageTk.PhotoImage(bodyImage.rotate(self.bodyOrientation))
        local_frame.create_image(self.X,self.Y,anchor=SW,image=self.bodyimg)

        LWImage = Image.open("Images/Wheel.png")
        LWImage = LWImage.resize((math.floor(wheelWidth*resizeFactor), math.floor(wheelHeight*resizeFactor)))

        self.LeftWheel = ImageTk.PhotoImage(LWImage.rotate(self.bodyOrientation+self.wheelLeftOrientation))
        local_frame.create_image(self.X + math.floor(82*resizeFactor),self.Y - math.floor(10*resizeFactor),anchor=SW,image=self.LeftWheel)

        self.RightWheel = ImageTk.PhotoImage(LWImage.rotate(self.bodyOrientation+self.wheelRightOrientation))
        local_frame.create_image(self.X + math.floor(82*resizeFactor),self.Y - math.floor(71*resizeFactor),anchor=SW,image=self.RightWheel)

    def updateLocalCar(self, local_frame, orientation, X, Y, spinWHEEE):
        #self.X = 115
        #self.Y = 235
        self.bodyOrientation = (-orientation + 90) % 360
        #self.wheelLeftOrientation +=1 # angle with respect to body coming out of the page
        #self.wheelRightOrientation = 1 # angle with respect to body coming out of the page

        self.woop = spinWHEEE % 360

        img2 = Image.open("Images/GlobalTrack.png")
        #img2 = scipy.ndimage.imread("Images/GlobalTrack.png", mode='RGB')
        self.bg = ImageTk.PhotoImage(img2.rotate(self.woop, center = (X, Y)))
        local_frame.create_image(-X + 175, -Y + 175, anchor=NW, image=self.bg)

        if(self.wheelRightOrientation == 0):
            self.wheelRightOrientation = 359
        self.r = (self.g/math.tan(math.radians(self.wheelRightOrientation))) + self.two_d/2
        self.wheelLeftOrientation = math.degrees((math.atan(self.g/(self.r + (self.two_d/2)))))
        # print("orientation: " + str(self.bodyOrientation))
        self.local_frame = local_frame
        resizeFactor = 1
        #Grab these from the properties of the pictures we are using
        bodyWidth = 119
        bodyHeight = 118
        wheelWidth = 38
        wheelHeight = 38

        bodyImage = Image.open("Images/Base3.png")
        bodyImage = bodyImage.resize((math.floor(bodyWidth*resizeFactor), math.floor(bodyHeight*resizeFactor)))
        self.bodyimg = ImageTk.PhotoImage(bodyImage.rotate(270))
        local_frame.create_image(self.X,self.Y,anchor=SW,image=self.bodyimg)

        LWImage = Image.open("Images/Wheel.png")
        LWImage = LWImage.resize((math.floor(wheelWidth*resizeFactor), math.floor(wheelHeight*resizeFactor)))

        orii = (self.bodyOrientation + 90) % 360
        yorii = (self.bodyOrientation + 270) % 360

        self.RightWheel = ImageTk.PhotoImage(LWImage.rotate(self.bodyOrientation-self.wheelRightOrientation))
        local_frame.create_image(self.X + math.floor(82*resizeFactor), self.Y - math.floor(10*resizeFactor),anchor=SW,image=self.RightWheel)

        self.LeftWheel = ImageTk.PhotoImage(LWImage.rotate(self.bodyOrientation-self.wheelLeftOrientation))
        local_frame.create_image(self.X + math.floor(82*resizeFactor),self.Y - math.floor(71*resizeFactor),anchor=SW,image=self.LeftWheel)
