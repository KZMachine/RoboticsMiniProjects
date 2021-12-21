from tkinter import *
import math
import numpy as np
from PIL import Image, ImageTk

class Vehicle:
    def __init__(self, xGiven, yGiven, lightCollection, k, canvas, Orientation):
        self.X = xGiven
        self.Y = yGiven

        self.K_Matrix = k

        self.Orientation = Orientation * -1

        self.LWheel = Wheel(self.X, self.Y + 20, 0)
        self.RWheel = Wheel(self.X, self.Y - 20, 0)

        self.LSensor = Sensor(self.X + 80, self.Y + 10, lightCollection)
        self.RSensor = Sensor(self.X + 80, self.Y - 10, lightCollection)

        image = Image.open('robot.png')
        self.tkimage = ImageTk.PhotoImage(image.rotate(Orientation))
        self.canvas_obj = canvas.create_image(self.X, self.Y, image=self.tkimage, tags="img")

    def deleteVe(self, canvas):
        canvas.delete(self.canvas_obj)

    def DrawVehicle(self, canvas):
        # image = Image.open('robot.png')
        # tkimage = ImageTk.PhotoImage(image.rotate(180))
        # canvas.create_image(250, 250, image=tkimage)
        # global tkimage
        # canvas.create_rectangle(
        #     self.X,
        #     self.Y - 20,
        #     self.X + 80,
        #     self.Y + 20,
        #     fill = "white",
        #     tags="body"
        # )
        # canvas.create_rectangle(
        #     self.LWheel.X,
        #     self.LWheel.Y - 5,
        #     self.LWheel.X + 20,
        #     self.LWheel.Y + 5,
        #     fill = "white",
        #     tags="lwheel"
        # )
        # canvas.create_rectangle(
        #     self.RWheel.X,
        #     self.RWheel.Y - 5,
        #     self.RWheel.X + 20,
        #     self.RWheel.Y + 5,
        #     fill = "white",
        #     tags="rwheel"
        # )
        # canvas.create_oval(
        #     self.LSensor.X - 3,
        #     self.LSensor.Y - 3,
        #     self.LSensor.X + 3,
        #     self.LSensor.Y + 3,
        #     fill="yellow",
        #     tags="lsensor"
        # )
        # canvas.create_oval(
        #     self.RSensor.X - 3,
        #     self.RSensor.Y - 3,
        #     self.RSensor.X + 3,
        #     self.RSensor.Y + 3,
        #     fill="yellow",
        #     tags="rsensor"
        # )

        # K_Input = input("Enter k-input in the following format: k11 k12 k21 k22\n")
        # KInputArray = K_Input.split(sep=' ')
        # for i in KInputArray:
        #     self.K_Matrix.append(float(i))
        return 0

    def UpdatePosition(self, canvas):
        canvas.delete(self.canvas_obj)

        #Take wheel velocities, find new body position and orientation, wheel positons and orientations come as a part of that
        SensorInputs = np.array([[self.RSensor.getLightSense()], [self.LSensor.getLightSense()]]) # then do matrix mult between K and sensorInputs to get wheel vel


        wheelVelocity = np.matmul(self.K_Matrix, SensorInputs)

        self.LWheel.Speed = float(wheelVelocity[0] / 100)
        self.RWheel.Speed = float(wheelVelocity[1] / 100)

        #calc angular velocity with given eqation on slides
        angular_vel = (self.RWheel.Speed - self.LWheel.Speed) / 2 * 20
        angular_vel_degrees = angular_vel * 180 / math.pi

        #add angular velocity to current orientation
        self.Orientation = self.Orientation + angular_vel_degrees

        #calculate robot velocity
        if self.RWheel.Speed != self.LWheel.Speed:
            velocity = angular_vel * 20 * (self.RWheel.Speed + self.LWheel.Speed) / (self.RWheel.Speed - self.LWheel.Speed)
        else:
            velocity = self.RWheel.Speed * 100

        # get new robot position from (current X + xComponent of velocity) and (current Y + yComponent of velocity)
        self.X = self.X + velocity * math.cos(math.radians(self.Orientation))
        self.Y = self.Y + velocity * math.sin(math.radians(self.Orientation))

        self.LWheel.X = self.X #they will always be same x as robot body
        self.LWheel.Y = self.LWheel.Y + velocity * math.sin(math.radians(self.Orientation))

        self.RWheel.X = self.X #they will always be same x as robot body
        self.RWheel.Y = self.RWheel.Y + velocity * math.sin(math.radians(self.Orientation))

        self.LSensor.X = self.X + 80
        self.LSensor.Y = self.LSensor.Y + velocity * math.sin(math.radians(self.Orientation))

        self.RSensor.X = self.X + 80
        self.RSensor.Y = self.RSensor.Y + velocity * math.sin(math.radians(self.Orientation))

        # ImageTk.PhotoImage(image.rotate(0))

        image = Image.open('robot.png')
        self.tkimage = ImageTk.PhotoImage(image.rotate((self.Orientation)*-1))
        self.canvas_obj = canvas.create_image(self.X, self.Y, image=self.tkimage, tags="img")



class Wheel:
    def __init__(self, xGiven, yGiven, speedGiven):
        self.X = xGiven
        self.Y = yGiven

        self.Speed = speedGiven

class Sensor:
    def __init__(self, xGiven, yGiven, lightCollection):
        self.X = xGiven
        self.Y = yGiven
        self.LightCollection = lightCollection

    def getLightSense(self):
        #want to return the strongest intensity from a source we see
        #simply looks at all light sources and finds the highest value and returns that
        maxIntensity = 0
        for light in self.LightCollection.getLights():
            if light.Intensity / math.sqrt((self.X - light.X) ** 2 + (self.Y - light.Y) ** 2) > maxIntensity:
                maxIntensity = light.Intensity / math.sqrt((self.X - light.X) ** 2 + (self.Y - light.Y) ** 2)

        return maxIntensity


class Light:
    def __init__(self, x, y, intensity):
        self.X = x
        self.Y = y
        self.Intensity = intensity

class LightCollection:
    def __init__(self):
        #Create light array
        self.Lights = []

    def addLight(self, light):
        #Append new light into array of lights
        self.Lights.append(light)

    def getLights(self):
        #return the array of lights we have
        return self.Lights

    def clearCollection(self):
        #reset local array of lights
        self.Lights = []
