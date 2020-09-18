import Polygon
import tkinter as tk
import math
import time
import motion_path


class myGUI():

    def __init__(self, master=None):
        self.master = master
        self.cv_height = 600
        self.w_height = 128
        self.obstacleList = []
        self.robot = None
        self.Ob_polyID = []
        self.Ri_polyID = []
        self.Rg_polyID = []
        self.moving_id = None
        self.moving_object = ['default']
        self.canvas = tk.Canvas(self.master, bg='white', width=600, height=600)
        self.canvas.place(x=0, y=0)
        #self.canvas.bind("<B1-Motion>", self.motion)
        self.click_id = None
        self.prePos = Polygon.Vertice(0, 0)

        self.canvas.tag_bind("DnD", '<B1-Motion>', self.startMove)
        self.canvas.tag_bind("DnD", '<ButtonRelease-1>', self.stopMove)  # 綁定滑鼠左鍵移動事件
        # self.canvas.tag_bind("DnD", '<B1-Motion>', self.motion)
        self.canvas.tag_bind("DnD", '<ButtonRelease-3>', self.stopRotate)  # 綁定右鍵旋轉事件
        self.canvas.tag_bind("DnD", '<B3-Motion>', self.startRotate)
        # self.canvas.tag_bind("DnD", '<B3-Motion>', self.rotate)




    #######################畫圖函式#######################
    def draw(self, obstacles, robot):
        # 讓GUI能取得障礙物和機器
        self.canvas.delete("all")
        self.obstacleList = obstacles
        self.robot = robot

        self.draw_obstacles()
        self.draw_robot("init")
        self.draw_robot("goal")

    def draw_obstacles(self):
        for O in self.obstacleList:
            # self.Ob_polyID.append(self.draw_polygon(O.polyList, O.confi))
            O.canvas_id = self.draw_polygon(O.polyList, O.confi)
            # self.draw_bbox(O.bbox, "Ob")
            #O.canvas_id.append(self.draw_bbox(O.bbox, "ob"))
        #print(self.Ob_polyID)

    def draw_robot(self, command="init"):
        if command == 'init':
            # self.Ri_polyID = self.draw_polygon(self.robot.polyList, self.robot.initConfi, "Ri")
            self.robot.init_canvas_id = self.draw_polygon(self.robot.polyList, self.robot.initConfi, "Ri")
            #print(self.Ri_polyID)
            #self.robot.init_canvas_id.append(self.draw_bbox(self.robot.bbox, "Ri"))
        elif command == 'goal':
            # self.Rg_polyID = self.draw_polygon(self.robot.polyList, self.robot.goalConfi, "Rg")
            self.robot.goal_canvas_id = self.draw_polygon(self.robot.polyList, self.robot.goalConfi, "Rg")
            #print(self.Rg_polyID)
            #self.robot.goal_canvas_id.append(self.draw_bbox(self.robot.bbox, "Rg"))

    def draw_polygon(self, polyList, confi, command='Ob'):
        indexList = []
        tupleList = []

        sin = math.sin(math.radians(confi.angle))
        cos = math.cos(math.radians(confi.angle))
        Spc = self.cv_height / self.w_height
        for P in polyList:
            for V in P.vertiList:
                # Do transformation
                trans_x = (V.x * cos - sin * V.y + confi.x) * Spc
                trans_y = self.cv_height - (V.x * sin + cos * V.y + confi.y) * Spc
                tupleList.append((trans_x, trans_y)) #把點蒐集起來變成list of tuples
            if command == 'Ri':
                indexList.append(self.canvas.create_polygon(tupleList, outline="black", fill="yellow", tags="DnD")) # 畫多邊形
                # print(indexList)
                # self.canvas.create_polygon(tupleList, outline="black", fill="yellow", tags="DnD")
            elif command == 'Rg':
                indexList.append(self.canvas.create_polygon(tupleList, outline="black", fill="", tags="DnD")) # 畫多邊形
                # self.canvas.create_polygon(tupleList, outline="black", fill="", tags="DnD")
            else:
                indexList.append(self.canvas.create_polygon(tupleList, outline="black", fill="black", tags="DnD")) # 畫多邊形
                # self.canvas.create_polygon(tupleList, outline="black", fill="black", tags="DnD")
            tupleList.clear()
        return indexList

    def draw_bbox(self, object_bbox, command="Ri"):
        if command == "Ri":
            bbox = [object_bbox["xMin"][0], object_bbox["yMin"][0], object_bbox["xMax"][0], object_bbox["yMax"][0]]
            # print(bbox)
            trans_bbox = []
            count = 0
            for v in bbox:
                if count % 2 == 0:
                    trans_bbox.append(v * 600 / 128)
                else:
                    trans_bbox.append(600 - (v * 600 / 128))
                count += 1
            # print(trans_bbox)
            return self.canvas.create_rectangle(trans_bbox, outline="red", fill="")
        elif command == "Rg":
            bbox = [object_bbox["xMin"][1], object_bbox["yMin"][1], object_bbox["xMax"][1], object_bbox["yMax"][1]]
            # print(bbox)
            trans_bbox = []
            count = 0
            for v in bbox:
                if count % 2 == 0:
                    trans_bbox.append(v * 600 / 128)
                else:
                    trans_bbox.append(600 - (v * 600 / 128))
                count += 1
            # print(trans_bbox)
            return self.canvas.create_rectangle(trans_bbox, outline="red", fill="")
        elif command == "ob":
            bbox = [object_bbox["xMin"][0], object_bbox["yMin"][0], object_bbox["xMax"][0], object_bbox["yMax"][0]]
            # print(bbox)
            trans_bbox = []
            count = 0
            for v in bbox:
                if count % 2 == 0:
                    trans_bbox.append(v * 600 / 128)
                else:
                    trans_bbox.append(600 - (v * 600 / 128))
                count += 1
            # print(trans_bbox)
            return self.canvas.create_rectangle(trans_bbox, outline="red", fill="")

    ##########################移動函式#########################
    # def findOb(self, ID):
    #     #print(ID, self.Ob_polyID)
    #     for i in range(len(self.Ob_polyID)):
    #         if ID in self.Ob_polyID[i]:
    #             return i

    def mod_Vcp(self, x, y):
        #轉到canvas時
        #trans_x = (V.x * cos - sin * V.y + confi.x) * Spc
        #trans_y = self.cv_height - (V.x * sin + cos * V.y + confi.y) * Spc
        #sin = math.sin(math.radians(angle))
        #cos = math.cos(math.radians(angle))
        # 600*600轉換成128*128 更新節點
        Scp = self.w_height / self.cv_height
        #x = self.canvas.coords(self.widget_ID[Pindex])[index]
        #y = self.canvas.coords(self.widget_ID[Pindex])[index + 1]
        trans_x = x * Scp
        trans_y = (y * Scp)
        return Polygon.Vertice(trans_x, 128-trans_y)

    def find_moving_object(self, x, y):
        # print(self.robot.bbox, x, y)
        if self.robot.bbox["xMax"][0] > x > self.robot.bbox["xMin"][0] and self.robot.bbox["yMax"][0] > y > \
                self.robot.bbox["yMin"][0]:
            return ["init", self.robot]
        elif self.robot.bbox["xMax"][1] > x > self.robot.bbox["xMin"][1] and self.robot.bbox["yMax"][1] > y > \
                self.robot.bbox["yMin"][1]:
            return ["goal", self.robot]
        else:
            for O in self.obstacleList:
                if O.bbox["xMax"][0] > x > O.bbox["xMin"][0] and O.bbox["yMax"][0] > y > O.bbox["yMin"][0]:
                    return ["obstacle", O]
        return["No", None]

    def startMove(self, event):
        print("start move")
        # self.prePos = Polygon.Vertice(event.x, event.y)
        mouse_pos = self.mod_Vcp(event.x, event.y)
        self.moving_object = self.find_moving_object(mouse_pos.x, mouse_pos.y)
        # print(self.moving_object[0])
        self.master.config(cursor="hand2")
        event.widget.bind("<B1-Motion>", self.motion)
        event.widget.bind("<ButtonRelease-1>", self.stopMove)

    def motion(self, event):
        print("moving")
        # mouse_pos = self.mod_Vcp(event.x, event.y)
        # self.moving_object = self.find_moving_object(mouse_pos.x, mouse_pos.y)
        # self.master.config(cursor="hand2")
        #print(event.x,event.y)
        newV = self.mod_Vcp(event.x, event.y)

        if self.moving_object[0] == "init":
            # print(self.robot.initConfi.x, self.robot.initConfi.y)
            # print(newV.x, newV.y)
            self.robot.mod_initConfi(newV.x, newV.y, self.robot.initConfi.angle)
        elif self.moving_object[0] == "goal":
            self.robot.mod_goalConfi(newV.x, newV.y, self.robot.goalConfi.angle)
        elif self.moving_object[0] == "obstacle":
            self.moving_object[1].mod_confi(newV.x, newV.y, self.moving_object[1].confi.angle)  # 危險啊 有空要改

        # 不斷重畫canvas
        self.draw(self.obstacleList, self.robot)
        # self.canvas.tag_bind("DnD", '<B1-Motion>', self.motion)
        # self.canvas.tag_bind("DnD", '<ButtonRelease-1>', self.stopMove)  # 綁定滑鼠左鍵移動事件

        # self.prePos = Polygon.Vertice(event.x, event.y)  # 更新前一個位置
        time.sleep(.05)  # 阻止破圖
        self.canvas.update()
    #
    def stopMove(self, event):
        print("stop move")
        newV = self.mod_Vcp(event.x, event.y)
        try:
            if self.moving_object[0] == "init":
                # print(self.robot.initConfi.x, self.robot.initConfi.y)
                # print(newV.x, newV.y)
                self.robot.mod_initConfi(newV.x, newV.y, self.robot.initConfi.angle)
            elif self.moving_object[0] == "goal":
                self.robot.mod_goalConfi(newV.x, newV.y, self.robot.goalConfi.angle)
            elif self.moving_object[0] == "obstacle":
                self.moving_object[1].mod_confi(newV.x, newV.y, self.moving_object[1].confi.angle)  # 危險啊 有空要改
        except:
            self.moving_object.append('default')

        # 不斷重畫canvas
        self.draw(self.obstacleList, self.robot)

        self.prePos = None  # Reset curIndex
        self.moving_object = []
        self.click_id = None
        self.master.config(cursor="arrow")  # Reset cursor
        event.widget.unbind("<B1-Motion>")  # Release event
        self.moving_object.append('default')
    #
    # ##########################旋轉函式#########################
    def centroid(self, coords):

        xPoints = []
        yPoints = []
        for index in range(0, len(coords),2):
            xPoints.append(coords[index])
            yPoints.append(coords[index+1])
        bbox = (min(xPoints), min(yPoints), max(xPoints), max(yPoints))  # return tuple of bbox
        return ((bbox[0]+bbox[2]) / 2, (bbox[1]+bbox[3]) / 2)

    def startRotate(self, event):
        self.prePos = Polygon.Vertice(event.x, event.y)
        mouse_pos = self.mod_Vcp(event.x, event.y)
        self.moving_object = self.find_moving_object(mouse_pos.x, mouse_pos.y)
        self.master.config(cursor="exchange")
        event.widget.bind("<B3-Motion>", self.rotate)
        event.widget.bind("<ButtonRelease-3>", self.stopRotate)

    def rotate(self,event):
        print("rotating")
        newAngle = math.degrees(math.atan2(event.y, event.x) - math.atan2(self.prePos.y, self.prePos.x)) * 2  # 旋轉角度公式
        # print( self.robot.initConfi.angle + newAngle)
        if self.moving_object[0] == "init":
            self.robot.mod_initConfi(self.robot.initConfi.x, self.robot.initConfi.y, self.robot.initConfi.angle + newAngle)
        elif self.moving_object[0] == "goal":
            self.robot.mod_goalConfi(self.robot.goalConfi.x, self.robot.goalConfi.y, self.robot.goalConfi.angle + newAngle)
        elif self.moving_object[0] == "obstacle":
            self.moving_object[1].mod_confi(self.moving_object[1].confi.x, self.moving_object[1].confi.y, self.moving_object[1].confi.angle + newAngle)  # 危險啊 有空要改

        self.draw(self.obstacleList, self.robot)
        self.prePos = Polygon.Vertice(event.x, event.y)  # 更新前一個位置
        time.sleep(.05)  # 阻止破圖

    def stopRotate(self, event):
        print("stop rotate")
        event.widget.unbind("<B3-Motion>")  # Release event
        self.prePos = None  # Reset curIndex
        self.moving_object = []
        self.master.config(cursor="arrow")  # Reset cursor

    def animate(self, path):
        node: motion_path.ListNode
        for index, node in enumerate(path):
            for id in self.robot.init_canvas_id:
                self.canvas.delete(id)
            self.robot.initConfi = node.confi
            self.robot.update_init_bbox()
            self.draw_robot("init")
            time.sleep(.05)
            self.canvas.update()
