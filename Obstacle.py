import Polygon
import math

class Obstacle():

    def __init__(self):
        self.confi = Polygon.Configuration(0, 0, 0)
        self.polyList = []
        self.bbox = {"xMin": [0], "xMax": [0], "yMin": [0], "yMax": [0]}
        self.canvas_id = []
        self.selected = False

    def add_Poly(self, poly):
        self.polyList.append(poly)

    def mod_confi(self, x, y, angle):
        self.confi.x = x
        self.confi.y = y
        self.confi.angle = angle
        self.update_bbox()
        #print(x, y, angle)

    def update_bbox(self):
        sin = math.sin(math.radians(self.confi.angle))
        cos = math.cos(math.radians(self.confi.angle))
        xOffset = self.confi.x
        yOffset = self.confi.y

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

    def centroid(self):
        vertexes = []
        for P in self.polyList:
            for V in P.vertiList:
                vertexes.append((V.x,V.y))
        print(vertexes)
        _x_list = [vertex[0] for vertex in vertexes]
        _y_list = [vertex[1] for vertex in vertexes]
        #for index in range(0, len(vertexes) - 1, 2):
         #   _x_list.append(vertexes[index])
          #  _y_list.append(vertexes[index + 1])

        print("depart:", _x_list, _y_list)
        _len = len(vertexes)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        print((_x, _y))
        return (_x, _y)

##從canvas更新回Planner
    def obstacle_updateVertice(self, cv, ID_list, targetID):
        cv_height = 600
        w_height = 128
        # 更新planner裡面的Vertice
        index = 0
        for Pindex in range(len(targetID)):  # 兩個polygon都要改到
            P = self.polyList[Pindex]
            for V in P.vertiList:
                # 600*600轉換成128*128 更新節點
                Spc = w_height / cv_height
                x = cv.coords(targetID[Pindex])[index]
                y = cv.coords(targetID[Pindex])[index+1]
                V.mod_Vertice(x * Spc, y * Spc) #從canvas map 回 planner
                index += 2
            index = 0
        #self.show_Ob()

    def show_Ob(self):
        pnum=0
        for poly in self.polyList:
            print("Poly:",pnum)
            poly.show_Poly()
            pnum+=1
        print("confi:(", self.confi.x, ",", self.confi.y, ",", self.confi.angle, ")")
