import Polygon
import Obstacle
import Robot
import tkinter as tk
import math
import time

class myGUI():

    def __init__(self, master=None):
        self.master = master
        self.cv_height = 600
        self.w_height = 128
        self.widget_ID = [] #[3,4]
        self.cv_obstacleList = [] #[[1], [2], [3,4]]
        self.cv_robotList = []
        self.obstacleList = []
        self.robotList=[]
        self.canvas = tk.Canvas(self.master, bg='white', width=600, height=600)
        self.canvas.place(x=0, y=0)
        #self.canvas.bind("<B1-Motion>", self.motion)
        self.curIndex = Polygon.Vertice(0, 0)

    def mod_Vcp(self, x, y):
        # 600*600轉換成128*128 更新節點
        Scp = self.w_height / self.cv_height
        #x = self.canvas.coords(self.widget_ID[Pindex])[index]
        #y = self.canvas.coords(self.widget_ID[Pindex])[index + 1]
        trans_x = x / Scp
        trans_y = y / Scp
        return (trans_x,trans_y)

    def centroid(self, coords):

        xPoints = []
        yPoints = []
        for index in range(0, len(coords),2):
            xPoints.append(coords[index])
            yPoints.append(coords[index+1])
        bbox = (min(xPoints), min(yPoints), max(xPoints), max(yPoints))  # return tuple of bbox
        return ((bbox[0]+bbox[2]) / 2, (bbox[1]+bbox[3]) / 2)

    def startRotate(self,event):
        self.curIndex = Polygon.Vertice(event.x, event.y)
        self.master.config(cursor="exchange")
        event.widget.bind("<Motion>", self.rotate)
        ########抓要移動的障礙物底下的所有多邊形的ID
        ID = event.widget.find_closest(event.x, event.y)[0] #最近的物件

        if ID in self.cv_robotList[0]:  # 動本體
            self.widget_ID = self.cv_robotList[0]
            # event.widget.bind("<Motion>", self.robotList[0].robot_updateVertice(self.cv_robotList, self.widget_ID))
        elif ID in self.cv_robotList[1]:  # 動目標
            self.widget_ID = self.cv_robotList[1]
        else:  # 動障礙物

            index = 0
            for i in self.cv_obstacleList: #檢查每個障礙物的polygon id
                if ID in i:
                    self.widget_ID = i
                    break
                index += 1

            coords = []
            for id in self.widget_ID:
                coords.extend(list(self.canvas.coords(id)))
            print(coords)
            #center = self.centroid(coords)
            #center = self.centroid(self.canvas.coords(self.cv_obstacleList[index]))
            offset = self.mod_Vcp(self.obstacleList[index].confi.x, self.obstacleList[index].confi.y)
            #x1, y1 = (center[0] - 1), self.cv_height-(center[1] - 1)
            #x2, y2 = (center[0] + 1), self.cv_height-(center[1] + 1)
            #x1, y1 = (center[0] - 1)+self.obstacleList[index].confi.x, (center[1] - 1)+self.obstacleList[index].confi.y
            #x2, y2 = (center[0] + 1)+self.obstacleList[index].confi.x, (center[1] + 1)+33self.obstacleList[index].confi.y
            #offset = self.mod_Vcp(self.obstacleList[index].confi.x, self.obstacleList[index].confi.y)
            #x1, y1 = (center[0] - 1) + offset[0], self.cv_height-(center[1] - 1) + offset[1]
            #x2, y2 = (center[0] + 1) + offset[0], self.cv_height-(center[1] + 1) + offset[1]
            #self.canvas.create_oval(x1, y1, x2, y2, fill="green", tags="center")

        for id in self.widget_ID:
            self.canvas.itemconfigure(id, outline="blue")  # 移動時填滿藍色

    def rotate(self,event):
        x, y = event.x, event.y
        #for id in self.widget_ID:
            #self.curIndex = Polygon.Vertice(event.x, event.y)  # 更新前一個位置
        cnv = event.widget  # 畫布
        #########移動時防止移出範圍

        for id in self.widget_ID:
            if event.x < 0:
                x = 0
            elif event.y < 0:
                y = 0
            elif event.y > self.cv_height:
                y = self.cv_height
            elif event.x > self.cv_height:
                x = self.cv_height
        ##########################

            center = self.centroid(cnv.coords(id))
            if len(self.widget_ID) > 1:
                all_coords = []
                for all_id in self.widget_ID:
                    all_coords.extend(cnv.coords(all_id))
                center = self.centroid(all_coords)

            newAngle = math.atan2(y, x) - math.atan2(self.curIndex.y, self.curIndex.x) #旋轉角度公式
            sin = math.sin(newAngle)
            cos = math.cos(newAngle)
            new_coords = []
            for index in range(0, len(cnv.coords(id)), 2):
                #旋轉公式
                #NewX = CenterX + (OldX-CenterX)*Cos(Fi) - (OldY-CenterY)*Sin(Fi)
                #NewY = CenterY + (OldX-CenterX)*Sin(Fi) + (OldY-CenterY)*Cos(Fi)
                new_coords.append(center[0] + (cnv.coords(id)[index]-center[0]) * cos - sin * (cnv.coords(id)[index+1] - center[1]))
                new_coords.append(center[1] + (cnv.coords(id)[index]-center[0]) * sin + cos * (cnv.coords(id)[index+1] - center[1]))
    #print("after x:", xPoints)
    #print("after y:", yPoints)
            cnv.coords(id, new_coords)  # 移動至新位置
        # self.updateVertice() #更新planner的多邊形點
        self.curIndex = Polygon.Vertice(event.x, event.y)  # 更新前一個位置
        time.sleep(.05)  # 阻止破圖

    def stopRotate(self,event):
        self.canvas.delete("center")
        ID = event.widget.find_closest(event.x, event.y)[0]

        if ID in self.cv_robotList[0]:  # 動本體
            self.widget_ID = self.cv_robotList[0]
            self.robotList[0].robot_updateVertice(self.canvas, self.cv_robotList, self.widget_ID)

            for CPindex in range(len(self.robotList[0].controlPoints)):
                tmpx, tmpy = self.robotList[0].controlPoints[CPindex].x, self.robotList[0].controlPoints[CPindex].y
                #confi_V = self.mod_Vcp(event.x, event.y)
                #self.robotList[0].move_ControlPoints(CPindex, confi_V.x - tmpx, confi_V.y - tmpy)  # 位移只改x, y
        elif ID in self.cv_robotList[1]:  # 動目標
            self.widget_ID = self.cv_robotList[1]
            #confi_V = self.mod_Vcp(event.x, event.y)
            #self.robotList[0].mod_goalConfi(confi_V.x, confi_V.y, self.robotList[0].goalConfi.angle)  # 位移只改x, y
        else:  # 動障礙物
            for i in range(len(self.cv_obstacleList)):
                if ID in self.cv_obstacleList[i]:
                    self.widget_ID = self.cv_obstacleList[i]
                    #self.obstacleList[i].obstacle_updateVertice(self.canvas, self.cv_obstacleList, self.widget_ID)
        for id in self.widget_ID:
            self.canvas.itemconfigure(id, outline="black")  # 回復黑色
        self.curIndex = None  # Reset curIndex
        self.master.config(cursor="arrow")  # Reset cursor
        event.widget.unbind("<Motion>")


    #########################畫布物件位移函式########################
    def setCurrent(self, event):
        self.curIndex = Polygon.Vertice(event.x, event.y)
        self.master.config(cursor="hand2")
        event.widget.bind("<Motion>", self.motion)
        ########抓要移動的障礙物底下的所有多邊形的ID
        ID = event.widget.find_closest(event.x, event.y)[0]

        if ID in self.cv_robotList[0]: #動本體
                self.widget_ID = self.cv_robotList[0]
                #event.widget.bind("<Motion>", self.robotList[0].robot_updateVertice(self.cv_robotList, self.widget_ID))
        elif ID in self.cv_robotList[1]: #動目標
                self.widget_ID = self.cv_robotList[1]
        else: #動障礙物
            for i in self.cv_obstacleList:
                if ID in i:
                    self.widget_ID = i
        for id in self.widget_ID:
            self.canvas.itemconfigure(id, outline="blue")  # 移動時填滿藍色

    def motion(self, event):
        x,y = event.x,event.y
        cnv = event.widget #畫布
        for id in self.widget_ID:
            if event.x < 0:
                x = 0
            elif event.y < 0:
                y = 0
            elif event.y > self.cv_height:
                y = self.cv_height
            elif event.x > self.cv_height:
                x = self.cv_height
            cnv.move(id, x - self.curIndex.x, y - self.curIndex.y)  # 移動至目前位置-前一位置
        #self.updateVertice() #更新planner的多邊形點
        self.curIndex = Polygon.Vertice(event.x, event.y)  # 更新前一個位置

        time.sleep(.05)  # 阻止破圖

    #########################重設參數########################
    def stopMotion(self, event):
        ID = event.widget.find_closest(event.x, event.y)[0]

        if ID in self.cv_robotList[0]:  # 動本體
            self.widget_ID = self.cv_robotList[0]
            self.robotList[0].robot_updateVertice(self.canvas, self.cv_robotList, self.widget_ID)

            for CPindex in range(len(self.robotList[0].controlPoints)):
                tmpx, tmpy = self.robotList[0].controlPoints[CPindex].x, self.robotList[0].controlPoints[CPindex].y
                confi_V = self.mod_Vcp(event.x, event.y)
                self.robotList[0].move_ControlPoints(CPindex, confi_V[0]-tmpx, confi_V[1]-tmpy) # 位移只改x, y
                self.robotList[0].mod_initConfi(confi_V[0], confi_V[1], self.robotList[0].initConfi.angle)
        elif ID in self.cv_robotList[1]:  # 動目標
            self.widget_ID = self.cv_robotList[1]
            confi_V = self.mod_Vcp(event.x, event.y)
            self.robotList[0].mod_goalConfi(confi_V[0], confi_V[1], self.robotList[0].goalConfi.angle) # 位移只改x, y
        else:  # 動障礙物
            for i in range(len(self.cv_obstacleList)):
                if ID in self.cv_obstacleList[i]:
                    self.widget_ID = self.cv_obstacleList[i]
                    confi_V = self.mod_Vcp(event.x, event.y)
                    self.obstacleList[i].mod_confi(confi_V[0], confi_V[0], self.obstacleList[i].confi.angle)
                    #self.obstacleList[i].obstacle_updateVertice(self.canvas, self.cv_obstacleList, self.widget_ID)
                #redraw(self.obstacleList[i])
        for id in self.widget_ID:
            self.canvas.itemconfigure(id, outline="black")  # 回復黑色
        self.curIndex = None  # Reset curIndex
        self.master.config(cursor="arrow")  # Reset cursor
        event.widget.unbind("<Motion>")

    def draw_Ob(self, obstacleList):
        self.obstacleList = obstacleList

        for O in obstacleList:
            #O.show_Ob()
            obPoly = []
            for P in O.polyList:

                tupleList = []
                for V in P.vertiList:
                    # Do transformation
                    sin = math.sin(math.radians(O.confi.angle))
                    cos = math.cos(math.radians(O.confi.angle))
                    Spc = self.cv_height / 128

                    trans_x = int((V.x * cos - sin * V.y + O.confi.x) * Spc)
                    trans_y = int(self.cv_height - (V.x * sin + cos * V.y + O.confi.y) * Spc)

                    # 把轉換後Vertice存成tuple list才可以放進create polygon
                    L = [trans_x, trans_y]
                    t = tuple(L)
                    #print(t)
                    tupleList.append(t)
                #print(P.vertiList)
                #print(tupleList)
                obPoly.append(self.canvas.create_polygon(tupleList, outline="black", fill="black", tags="Obstacle"))
                self.canvas.tag_bind("Obstacle", '<ButtonRelease-1>', self.stopMotion) # 綁定滑鼠左鍵移動事件
                self.canvas.tag_bind("Obstacle", '<Button-1>', self.setCurrent)
                self.canvas.tag_bind("Obstacle", '<ButtonRelease-3>', self.stopRotate) # 綁定右鍵旋轉事件
                self.canvas.tag_bind("Obstacle", '<Button-3>', self.startRotate)

            self.cv_obstacleList.append(obPoly) # 每個障礙物裡面的Polygon id變成一個list (可以把同一個障礙物裡面的多邊形綁在一起)

        #print(self.cv_obstacleList)

    def draw_Robot(self, Robot):
        self.robotList.append(Robot)

        ######################### DRAW ROBOT #############################
        RbPoly=[]
        for P in Robot.polyList:
            tupleList = []
            for V in P.vertiList:
                # Do transformation
                sin = math.sin(math.radians(Robot.initConfi.angle))
                cos = math.cos(math.radians(Robot.initConfi.angle))
                c_height = 600
                Spc = c_height / 128

                trans_x = int((V.x * cos - sin * V.y + Robot.initConfi.x) * Spc)
                trans_y = int(c_height - (V.x * sin + cos * V.y + Robot.initConfi.y) * Spc)

                L = [trans_x, trans_y]
                t = tuple(L)
                tupleList.append(t)

            #print(P.vertiList)
            RbPoly.append(self.canvas.create_polygon(tupleList, outline="black", fill="yellow", tags="R_Init"))

        self.cv_robotList.append(RbPoly)
        self.canvas.tag_bind("R_Init", '<ButtonRelease-1>', self.stopMotion)  # 綁定滑鼠左鍵移動事件
        self.canvas.tag_bind("R_Init", '<Button-1>', self.setCurrent)
        self.canvas.tag_bind("R_Init", '<ButtonRelease-3>', self.stopRotate)  # 綁定右鍵旋轉事件
        self.canvas.tag_bind("R_Init", '<Button-3>', self.startRotate)


         ######################### DRAW GOAL #############################
        RbPoly = []
        for P in Robot.polyList:
            tupleList = []
            for V in P.vertiList:
                # Do transformation
                sin = math.sin(math.radians(Robot.goalConfi.angle))
                cos = math.cos(math.radians(Robot.goalConfi.angle))
                c_height = 600
                Spc = c_height / 128

                trans_x = int((V.x * cos - sin * V.y + Robot.goalConfi.x) * Spc)
                trans_y = int(c_height - (V.x * sin + cos * V.y + Robot.goalConfi.y) * Spc)

                L = [trans_x, trans_y]
                t = tuple(L)
                # print(t)
                tupleList.append(t)
            # print(P.vertiList)
            RbPoly.append(self.canvas.create_polygon(tupleList, outline="black", fill="white", tags="R_Goal"))

        self.cv_robotList.append(RbPoly)
        self.canvas.tag_bind("R_Goal", '<ButtonRelease-1>', self.stopMotion)  # 綁定滑鼠左鍵移動事件
        self.canvas.tag_bind("R_Goal", '<Button-1>', self.setCurrent)
        self.canvas.tag_bind("R_Goal", '<ButtonRelease-3>', self.stopRotate)  # 綁定右鍵旋轉事件
        self.canvas.tag_bind("R_Goal", '<Button-3>', self.startRotate)
'''
    def redraw_Ob(self, item):
        for P in item.polyList:

            tupleList = []
            for V in P.vertiList:
                # Do transformation
                sin = math.sin(math.radians(O.confi.angle))
                cos = math.cos(math.radians(O.confi.angle))
                Spc = self.cv_height / 128

                trans_x = int((V.x * cos - sin * V.y + O.confi.x) * Spc)
                trans_y = int(self.cv_height - (V.x * sin + cos * V.y + O.confi.y) * Spc)

                # 把轉換後Vertice存成tuple list才可以放進create polygon
                L = [trans_x, trans_y]
                t = tuple(L)
                # print(t)
                tupleList.append(t)

            self.canvas.tag_bind("Obstacle", '<ButtonRelease-1>', self.stopMotion)  # 綁定滑鼠左鍵移動事件
            self.canvas.tag_bind("Obstacle", '<Button-1>', self.setCurrent)
            self.canvas.tag_bind("Obstacle", '<ButtonRelease-3>', self.stopRotate)  # 綁定右鍵旋轉事件
            self.canvas.tag_bind("Obstacle", '<Button-3>', self.startRotate)
'''