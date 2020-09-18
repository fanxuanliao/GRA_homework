from Obstacle import *
from Robot import *
from Polygon import *
import bitmap
import motion_path
import math

class data():
    def __init__(self, GUI):
        self.robotList = []
        self.obstacleList = []
        self.myGUI = GUI
        self.bitmap = []
        self.OPEN = {}
        self.PFields = []

        # initiate BFS array
        for i in range(255):
            self.OPEN[i] = []

    def searchPath(self):
        print("searchPath")
        path = motion_path.plan(self.bitmap, self.obstacleList, self.robotList[0], self.PFields, self.OPEN)
        if path != "Fail":
            self.myGUI.animate(path)


    def setBitmap(self):
        self.bitmap = bitmap.draw_Bitmap(self.obstacleList, self.robotList[0])
        self.PFields = bitmap.spread(self.bitmap, self.robotList[0])
        # print(self.PFields)

    def process_data_obstacle(self, file):
        obstacleList = self.obstacleList
        var_list = []

        # 取出參數
        with open(file) as f:
            for line in f.readlines():
                if '#' not in line:
                    var_list.append(line.strip("\n").split(" "))

        num_of_obs = int(var_list[0][0])  # 第一個參數是障礙物數量
        del var_list[0]

        for i in range(num_of_obs):  # 建立障礙物
            obstacle = Obstacle()
            obstacleList.append(obstacle)  # 障礙物列表
            num_of_polys = int(var_list[0][0])
            del var_list[0]

            for j in range(num_of_polys):  # 建立多邊形
                poly = Polygon()
                num_of_vertices = int(var_list[0][0])
                del var_list[0]

                for k in range(num_of_vertices):
                    verti = Vertice(float(var_list[0][0]), float(var_list[0][1]))
                    poly.add_Verti(verti)  # 座標加在多邊形上
                    del var_list[0]

                obstacleList[i].add_Poly(poly)  # 多邊形加在障礙上

            obstacle.mod_confi(float(var_list[0][0]), float(var_list[0][1]), float(var_list[0][2]))
            del var_list[0]
            #print("complete")
            #obstacleList[i].show_Ob()
        #global cv
        #Draw(cv, obstacleList)
        #self.myGUI.draw_Ob(obstacleList)
        return obstacleList

    def process_data_robot(self, file):
        robotList = self.robotList
        #robotList = []
        var_list = []

        # 取出參數
        with open(file) as f:
            for line in f.readlines():
                if '#' not in line:
                    var_list.append(line.strip("\n").split(" "))
        #print(var_list)

        num_of_rbs = int(var_list[0][0])  # 第一個參數是機器數量
        del var_list[0]

        for i in range(num_of_rbs):  # 建立機器
            robot = Robot()
            robotList.append(robot)  # 機器列表
            num_of_polys = int(var_list[0][0])
            del var_list[0]

            for j in range(num_of_polys):  # 建立多邊形
                poly = Polygon()
                num_of_vertices = int(var_list[0][0])
                del var_list[0]

                for k in range(num_of_vertices):
                    verti = Vertice(float(var_list[0][0]), float(var_list[0][1]))
                    poly.add_Verti(verti)  # 座標加在多邊形上
                    del var_list[0]

                robotList[i].add_Poly(poly)  # 多邊形加在障礙上

            robotList[i].mod_initConfi(float(var_list[0][0]), float(var_list[0][1]), float(var_list[0][2]))
            del var_list[0]
            robotList[i].mod_goalConfi(float(var_list[0][0]), float(var_list[0][1]), float(var_list[0][2]))
            del var_list[0]
            cp_num = int(var_list[0][0])
            #print(cp_num)
            del var_list[0]
            for l in range(cp_num):
                CP = Vertice(float(var_list[0][0]), float(var_list[0][1]))
                robotList[i].add_ControlPoints(CP)
                del var_list[0]

            #print("complete")
            #robotList[i].show_Rb()
        #self.myGUI.draw_Robot(robotList[0])
        robotList[0].update_init_bbox()
        robotList[0].update_goal_bbox()
        return(robotList[0])
        #myGUI.draw_Goal(robotList[0])