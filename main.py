import os
import tkinter as tk
from tkinter import filedialog
import globals
from Obstacle import *
from Robot import *
from myGUI import *
from Polygon import *
import bitmap
import motion_path
import data

def read_all():
    global root
    path1 = './obstacle.dat.txt'
    obstacles = globals.data.process_data_obstacle(path1)
    path2 = './robot.dat.txt'
    robot = globals.data.process_data_robot(path2)
    myGUI.draw(obstacles, robot)
    globals.data.setBitmap()
    # tk.Button(root, text="Draw items", command=lambda: myGUI.draw(obstacles, robot)).place(x=620, y=60)
    tk.Button(root, text="Generate Potential Field", command=lambda: globals.data.setBitmap()).place(x=620, y=60)
    #tk.Button(root, text="Draw bitmap", command=lambda: bitmap.draw_Bitmap_from_Canvas(data.obstacleList, data.robotList[0],data.myGUI.canvas)).place(x=620, y=90)
    #tk.Button(root, text="Start", command=lambda: motion_path.motion(data.bitmap, data.obstacleList, data.robotList[0])).place(x=620, y=90)
    tk.Button(root, text="Test collision",
              command=lambda: motion_path.collision_detection(globals.data.obstacleList, globals.data.robotList[0])).place(x=620, y=90)
    tk.Button(root, text="Plan", command=globals.data.searchPath).place(x=620, y=120)
    #tk.Button(root, text="Draw bitmap(canvas)", command=lambda: bitmap.draw_Bitmap_from_Canvas(data.obstacleList, data.robotList[0], data.myGUI.canvas)).place(x=620, y=90)

def read_file_obstacle():
    globals.data
    #path = './obstacle.dat.txt'
    path = filedialog.askopenfilename()
    globals.data.process_data_obstacle(path)

def read_file_robot():
    globals.data
    path = filedialog.askopenfilename()
    globals.data.process_data_robot(path)



if __name__ == "__main__":
    globals.initialize()
    root = tk.Tk()
        #path = './robot.dat.txt'
    root.title("Motion Planner")
    # 定義視窗大小
    root.geometry("800x600")

    myGUI = myGUI(root)
    globals.data = data.data(myGUI)
    bm = [[254 for i in range(128)] for i in range(128)]
    # 讀檔按鈕
    tk.Button(root, text="Read default", command=read_all).place(x=620, y=30)
    #tk.Button(root, text="Read Obstacle", command=read_file_obstacle).place(x=650, y=60)
    #tk.Button(root, text="Read Robot", command=read_file_robot).place(x=660, y=90)
    # 建立畫布

    #cv = tk.Canvas(root, bg='white', width=600, height=600).place(x=0, y=0)

    root.mainloop()





