from tkinter import *
from vehicle import*
import math
from random import randrange
from PIL import Image, ImageTk

root=Tk()
root.title('Braitenberg Vehicles')
root.geometry("1425x815")
root.config(bg="maroon")

# Space Frame
space_frame = Canvas(root, width=1050, height=800)
space_frame.grid(row=0, column=1, padx=2.5, pady=5)
space_frame.config(bg="black")

# Control frame
control_frame = Frame(root, width=350, height=800)
control_frame.grid(row=0, column=0, padx=5, pady=5,sticky="nsew")
control_frame.pack_propagate(False)

# Title
Title = Label(control_frame, text = "Braitenberg Vehicles - TAMU 2021",font='Helvetica 12 bold')
Title.pack(side=TOP)

####################################### Light #######################################

lights_label = Label(control_frame, text = "Lights",font='Helvetica 16 bold').place(x = 110, y = 60)

def DrawLight():
    x=Light_X_position.get()
    y=Light_Y_position.get()
    Intensity=Intensity_.get()

    if(Intensity > 100):
        Intensity = 100

    space_frame.create_oval(x-Intensity, y-Intensity, x+Intensity, y+Intensity,fill="gray", tags='lights')
    space_frame.create_oval(x-5, y-5, x+5, y+5,fill="yellow", tags='lights')

    Light_X_position.set("0")
    Light_Y_position.set("0")

    #Add new light to lightcollection
    AllLights.addLight(Light(x, y, Intensity))

def EraseAllLight(event=None):
    space_frame.delete("lights")

    #Clear all lights from collection
    AllLights.clearCollection()

def RandomLight():
    x = randrange(1051)
    y = randrange(800)
    Intensity= randrange(10,100)
    space_frame.create_oval(x-Intensity, y-Intensity, x+Intensity, y+Intensity,fill="gray", tags='lights')
    space_frame.create_oval(x-5, y-5, x+5, y+5,fill="yellow", tags='lights')

    #Add new light to collection
    AllLights.addLight(Light(x, y, Intensity))


# declaring int variable for storing X and Y from entry
Light_X_position=IntVar()
Light_Y_position=IntVar()
Intensity_=IntVar()

X_label = Label(control_frame, text = "X").place(x = 50, y = 100)
Y_label = Label(control_frame, text = "Y").place(x = 50, y = 130)
Intensity_label = Label(control_frame, text = "Intensity").place(x = 50, y = 160)
sbmitbtn = Button(control_frame, text = "Draw", activebackground = "green", width=19, activeforeground = "blue", command = DrawLight).place(x = 110, y = 190)
Light_X_entry = Entry(control_frame, textvariable = Light_X_position).place(x = 110, y = 100)
Light_Y_entry = Entry(control_frame, textvariable = Light_Y_position).place(x = 110, y = 130)
Intensity_entry = Entry(control_frame, textvariable = Intensity_).place(x = 110, y = 160)

# Random Light
Randombtn = Button(control_frame, text = "Random Light", activebackground = "green", width=19, activeforeground = "blue", command = RandomLight).place(x = 110, y = 230)

# Erase
Erasebtn = Button(control_frame, text = "Erase All Lights", activebackground = "green", width=19, activeforeground = "blue", command = EraseAllLight).place(x = 110, y = 270)




####################################### Vehicle  #######################################

Vehicle_label = Label(control_frame, text = "Vehicles",font='Helvetica 16 bold').place(x = 110, y = 350)
orientation_num=float()
orientation_label = Label(control_frame, text = "Robot Orientation").place(x = 70, y = 320)
orientation_entry = Entry(control_frame, textvariable = orientation_num, width=5)
orientation_entry_place = orientation_entry.place(x = 200, y = 320)
vehicles = []

def DrawVehicle(x, y, k11, k12, k21, k22):
    k = np.array([[k11,k12], [k21,k22]])
    TestRobot = Vehicle(int(x), int(y), AllLights, k, space_frame, float(orientation_entry.get()))
    TestRobot.DrawVehicle(space_frame)
    vehicles.append(TestRobot)

def EraseAllVehicle(event=None):
    space_frame.delete("body", "lwheel", "rwheel", "lsensor", "rsensor")
    for vehicle in vehicles:
        vehicle.deleteVe(space_frame)

def RandomVehicle(k11, k12, k21, k22):
    k = np.array([[1,0], [0,1]])
    TestRobot = Vehicle(randrange(1040), randrange(840), AllLights,k, space_frame,randrange(359))
    TestRobot.DrawVehicle(space_frame)
    vehicles.append(TestRobot)

# declaring int variable for storing X and Y from entry
Vehicle_X_position=IntVar()
Vehicle_Y_position=IntVar()

k11=IntVar()
k12=IntVar()
k21=IntVar()
k22=IntVar()

Vehicle_X_label = Label(control_frame, text = "X").place(x = 50, y = 390)
Vehicle_Y_label = Label(control_frame, text = "Y").place(x = 50, y = 420)

Vehicle_X_entry = Entry(control_frame, textvariable = Vehicle_X_position)
Vehicle_Y_entry = Entry(control_frame, textvariable = Vehicle_Y_position)
Vehicle_X_entry_place = Vehicle_X_entry.place(x = 110, y = 390)
Vehicle_Y_entry_place = Vehicle_Y_entry.place(x = 110, y = 420)

k11_label = Label(control_frame, text = "k11").place(x = 70, y = 460)
k12_label = Label(control_frame, text = "k12").place(x = 170, y = 460)
k21_label = Label(control_frame, text = "k21").place(x = 70, y = 490)
k22_label = Label(control_frame, text = "k22").place(x = 170, y = 490)

k11_entry = Entry(control_frame, textvariable = k11, width=5)
k12_entry = Entry(control_frame, textvariable = k12, width=5)
k21_entry = Entry(control_frame, textvariable = k21, width=5)
k22_entry = Entry(control_frame, textvariable = k22, width=5)

k11_entry_place = k11_entry.place(x = 110, y = 460)
k12_entry_place = k12_entry.place(x = 210, y = 460)
k21_entry_place = k21_entry.place(x = 110, y = 490)
k22_entry_place = k22_entry.place(x = 210, y = 490)

Vehicle_sbmitbtn = Button(control_frame, text = "Draw", activebackground = "green", width=19, activeforeground = "blue", command = lambda:DrawVehicle(Vehicle_X_entry.get(), Vehicle_Y_entry.get(), k11.get(), k12.get(), k21.get(), k22.get())).place(x = 110, y = 530)

# Random Light
Vehicle_Randombtn = Button(control_frame, text = "Random Vehicle", activebackground = "green", width=19, activeforeground = "blue", command = lambda:RandomVehicle(k11.get(), k12.get(), k21.get(), k22.get())).place(x = 110, y = 560)

# Erase
Vehicle_Erasebtn = Button(control_frame, text = "Erase All Vehicle", activebackground = "green", width=19, activeforeground = "blue", command = EraseAllVehicle).place(x = 110, y = 590)


'''def MoveCar():
    try:
        print("worked")
        TestRobot
    except:
        print("error")
'''

#Create storage for all the lights we have
AllLights = LightCollection()

#Init a robot, just for testing
TestRobot = Vehicle(400, 400, AllLights, np.array([[1,0], [0,1]]), space_frame, 0)
TestRobot.DrawVehicle(space_frame)

vehicles.append(TestRobot)


def robotMoveLoop():
    TestRobot.UpdatePosition(space_frame)
    #if(((TestRobot.X >= 145 and TestRobot.X <= 150) or (TestRobot.Y <= 150 and TestRobot.Y >= 145)) == False):
    for vehicle in vehicles:
        vehicle.UpdatePosition(space_frame)
    root.after(100, robotMoveLoop)

# move
Vehicle_Movebtn = Button(control_frame, text = "Move Vehicle", activebackground = "green", width=19, activeforeground = "blue", command = robotMoveLoop).place(x = 110, y = 620)


#Vehicle_Movebtn = Label(control_frame, text = "Move Vehicle", activebackground = "green", width=19, activeforeground = "blue", command = robotMoveLoop).place(x = 110, y = 650)


root.update()
root.mainloop()
