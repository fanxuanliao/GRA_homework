from Polygon import *
import myGUI
import time
import math

class Robot():
    def __init__(self):
        self.initConfi = Configuration(0, 0, 0)
        self.goalConfi = Configuration(0, 0, 0)
        self.controlPoints = []
        self.polyList = []
        self.bbox = {"xMin":[0,0], "xMax":[0,0], "yMin":[0,0], "yMax":[0,0]} # 0:init 1:goal
        self.init_canvas_id = []
        self.goal_canvas_id = []
        self.selected = False

    def add_Poly(self, poly):
        self.polyList.append(poly)

    def add_ControlPoints(self, V):
        self.controlPoints.append(V)

    def move_ControlPoints(self, index, x, y):
        self.controlPoints[index].x += x
        self.controlPoints[index].y += y

    def mod_initConfi(self, x, y, angle):
        self.initConfi.x = x
        self.initConfi.y = y
        self.initConfi.angle = angle
        self.update_init_bbox()
        #print(x, y, angle)

    def mod_goalConfi(self, x, y, angle):
        #print("mod to:",x,y,angle)
        self.goalConfi.x = x
        self.goalConfi.y = y
        self.goalConfi.angle = angle
        self.update_goal_bbox()

    def update_init_bbox(self):
        sin = math.sin(math.radians(self.initConfi.angle))
        cos = math.cos(math.radians(self.initConfi.angle))
        xOffset = self.initConfi.x
        yOffset = self.initConfi.y

        xPoints = []
        yPoints = []

        for P in self.polyList:
            for V in P.vertiList:
                # 要再加上configuration
                xPoints.append(V.x * cos - sin * V.y + xOffset)
                yPoints.append(V.x * sin + cos * V.y + yOffset)
        self.bbox["xMin"][0] = min(xPoints)
        self.bbox["yMin"][0] = min(yPoints)
        self.bbox["xMax"][0] = max(xPoints)
        self.bbox["yMax"][0] = max(yPoints)

    def update_goal_bbox(self):
        sin = math.sin(math.radians(self.goalConfi.angle))
        cos = math.cos(math.radians(self.goalConfi.angle))
        xOffset = self.goalConfi.x
        yOffset = self.goalConfi.y

        xPoints = []
        yPoints = []

        for P in self.polyList:
            for V in P.vertiList:
                # 要再加上configuration
                xPoints.append(V.x * cos - sin * V.y + xOffset)
                yPoints.append(V.x * sin + cos * V.y + yOffset)
        self.bbox["xMin"][1] = min(xPoints)
        self.bbox["yMin"][1] = min(yPoints)
        self.bbox["xMax"][1] = max(xPoints)
        self.bbox["yMax"][1] = max(yPoints)

    def show_Rb(self):

        pnum=0
        for poly in self.polyList:
            print("Poly:",pnum)
            poly.show_Poly()
            pnum+=1

        cpnum=0
        for cp in self.controlPoints:
            print("Control Point:", cpnum)
            cp.show_Vertice()
            cpnum += 1

        print("init confi:(", self.initConfi.x, ",", self.initConfi.y, ",", self.initConfi.angle, ")")
        print("goal confi:(", self.goalConfi.x, ",", self.goalConfi.y, ",", self.goalConfi.angle, ")")

    ##從canvas更新回Planner
    def robot_updateVertice(self, cv, ID_list, targetID):
        print("Update robot vertices in planner.")
        cv_height = 600
        w_height = 128

        # 更新planner裡面的Vertice
        index = 0
        for Pindex in range(len(targetID)):  # polygon都要改到
            P = self.polyList[Pindex]
            for V in P.vertiList:
                print(cv.coords(targetID[Pindex]))
                # 600*600轉換成128*128 更新節點
                Spc = cv_height / w_height
                x = cv.coords(targetID[Pindex])[index]
                y = cv.coords(targetID[Pindex])[index+1]
                trans_x = x / Spc
                trans_y = y / Spc
                V.mod_Vertice(trans_x, trans_y)
                index += 2
            index = 0
        #self.show_Rb()


class ControlPoint():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show_CP(self):
        print("(", self.x, ",", self.y, ")")
