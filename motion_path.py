import math
import numpy as np
from Polygon import Vertice
import copy
from Polygon import Configuration
import main
import  tkinter as tk

# class path():
#     def __init__(self):
#         self.isMotion = True
#         self.BFS = []

def transformation(V, confi):
    sin = math.sin(math.radians(confi.angle))
    cos = math.cos(math.radians(confi.angle))
    return Vertice(V.x * cos - sin * V.y + confi.x, V.x * sin + cos * V.y + confi.y)

def check_edge_intersection(robotEdges, obEdges):
    for r in robotEdges:
        for o in obEdges:
            v1 = r[1] - r[0]
            v2 = o[0] - r[0]
            v3 = o[1] - r[0]
            vv1 = o[1] - o[0]
            vv2 = r[0] - o[0]
            vv3 = r[1] - o[0]
            v1.ConvertVertical()
            vv1.ConvertVertical()
            if (dot(v1, v2) * dot(v1, v3) < 0 and dot(vv1, vv2) * dot(vv1, vv3) < 0):
                return True
    return False


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

def collision_detection(obstacle, robot):
    print("checking collision...")

    R_bbox = [robot.bbox["xMin"][0], robot.bbox["yMin"][0], robot.bbox["xMax"][0], robot.bbox["yMax"][0]] # find robot's bounding box
    # print("R_BBOX", R_bbox)
    robotEdges = []
    for P in robot.polyList:
        for i in range(len(P.vertiList)):
            #P.vertiList[i].show_Vertice()
            if i != len(P.vertiList) - 1:
                robotEdges.append((transformation(P.vertiList[i], robot.initConfi),
                                   transformation(P.vertiList[i+1], robot.initConfi)))
            else:
                robotEdges.append((transformation(P.vertiList[i], robot.initConfi),
                                   transformation(P.vertiList[0], robot.initConfi)))

    for O in obstacle:
        O_bbox = [O.bbox["xMin"][0], O.bbox["yMin"][0], O.bbox["xMax"][0], O.bbox["yMax"][0]] # find obstacle's bounding box
        # print("O_bbox", O_bbox)
        # 1. Check bbox intersection
        # if R_bbox[0] <= O_bbox[2] and R_bbox[2] >= O_bbox[0] and R_bbox[3] >= O_bbox[1] and R_bbox[1] >= O_bbox[3]:
        # if R_bbox[0] <= O_bbox[2] and R_bbox[1] <= O_bbox[3] and R_bbox[2] >= O_bbox[0] and R_bbox[3] >= O_bbox[1]:
        #     print("bbox collision")
            # 2. Check edges intersection
        obsEdges = []
        for P in O.polyList:
            for i in range(len(P.vertiList)):
                if i != len(P.vertiList)-1:
                    obsEdges.append((transformation(P.vertiList[i], O.confi), transformation(P.vertiList[i+1], O.confi)))
                else:
                    obsEdges.append((transformation(P.vertiList[i], O.confi), transformation(P.vertiList[0], O.confi)))

        if check_edge_intersection(robotEdges, obsEdges):
            print("edge cross")
            return True

    print("no collides")
    return False

#def motion_stop():


def arbitration(PFs, robot):
    # print("goal:", robot.goalConfi.x, robot.goalConfi.y, robot.goalConfi.angle)
    trans_CPs = []
    sin = math.sin(math.radians(robot.initConfi.angle))
    cos = math.cos(math.radians(robot.initConfi.angle))
    for CP in robot.controlPoints:
        x = int(CP.x * cos - sin * CP.y + robot.initConfi.x)
        y = int(CP.x * sin + cos * CP.y + robot.initConfi.y)
        trans_CPs.append(Vertice(x, y))

    arbitrary = 0
    base = 0
    for i in range(1, len(PFs)+1):
        base += i
    # print("base:",base)
    if len(PFs) == len(trans_CPs):
        for j in range (len(PFs)):
            try:
            # print("{}: {} + {}".format(i, arbitrary, PFs[i][trans_CPs[i].y][trans_CPs[i].x]))
                arbitrary += int(PFs[j][trans_CPs[j].y][trans_CPs[j].x]) / base * (len(PFs)-j)
            except:
                print(j, "out of range.")
            # print("arb",arbitrary)

    return int(arbitrary)

# 字典中的list是否全為空
def isEmptyDict(OPEN):
    for key in OPEN.keys():
        if not OPEN[key]: # list 是空的
           return False
    return True


def first(OPEN):
    minU = -1
    for key in OPEN.keys():
       if OPEN[key]:
           print("key:", key)
           minU = key
           break
    return OPEN[minU][0]

def delfirst(OPEN):
    minU = -1
    for key in OPEN.keys():
        if OPEN[key]:
            minU = key
            break
    del OPEN[minU][0]


def isGoal(PFs, robot):
    GOAL = True
    for index, CP in enumerate(robot.controlPoints):
        trans_CP = transformation(CP,robot.goalConfi)
        # x = int(CP.x + robot.goalConfi.x)
        # y = int(CP.y + robot.goalConfi.y)
        if PFs[index][int(trans_CP.y)][int(trans_CP.x)] != 0:
            GOAL = False
    if not GOAL:
        return False
    return True


def show_path(lastNode):
    node = copy.deepcopy(lastNode)
    counter = 0
    while True:
        # print(counter)
        counter += 1
        # print("U:", node.U)
        node.confi.show_Confi()
        if node.previous == None:
            break
        node = node.previous


def plan(bitmap, obstacleList, robot, PFs, OPEN):
    print("start planning...")
    SUCCESS = False
    goalNode = None
    visited = [[[False for k in range(360)] for j in range(128)] for i in range(128)]
    # print("shape:", len(visited), len(visited[0]), len(visited[0][0]))
    # 方向
    dx = [1, -1, 0, 0, 0, 0] # x
    dy = [0, 0, 1, -1, 0, 0] # y
    da = [0, 0, 0, 0, 10, -10] # angle

    print("insert first node")
    # insert init position
    initU = arbitration(PFs, robot)
    # print("initU",initU)
    OPEN[initU].append(ListNode(robot.initConfi, initU)) # 搜尋List，用來記錄可以走的地方
    visited[int(robot.initConfi.x)][int(robot.initConfi.y)][int(robot.initConfi.angle)] = True  # 記錄某個configuration是否有走過
    # print("mark")
    temp_robot = copy.deepcopy(robot)  # 用來判斷collision
    while not isEmptyDict(OPEN) and not SUCCESS:
        pre_node = first(OPEN)
        print("finding... from", pre_node.U)
        delfirst(OPEN)

        for i in range(len(dx)):
            next_x, next_y, next_a = int(pre_node.confi.x + dx[i]), int(pre_node.confi.y + dy[i]),  int(pre_node.confi.angle + da[i])
            if next_a >= 360:
                next_a -= 360
            if next_a < 0:
                next_a += 360
            # 超出範圍不考慮
            if next_x >= 128 or next_x < 0 or next_y >= 128 or next_y < 0:
                continue

            if not visited[next_x][next_y][next_a]: # configuration還沒走過
                next_confi = Configuration(next_x, next_y, next_a)
                temp_robot.initConfi.x, temp_robot.initConfi.y, temp_robot.initConfi.angle = next_confi.x, next_confi.y, next_confi.angle
                temp_robot.update_init_bbox()
                u = arbitration(PFs, temp_robot)

                #有碰撞不考慮
                if collision_detection(obstacleList, temp_robot) or u == 255:
                    print("collides")
                    continue
                #無碰撞放進OPEN list
                else:
                    # else: #還沒找完
                    next_node = ListNode(next_confi, u)
                    next_node.previous = pre_node
                    OPEN[u].insert(0, next_node)
                        # if OPEN[u]: #u值的list為空
                        #     OPEN[u].append(next_node)
                        # else: # u值的list已經有東西
                        #     OPEN[u].insert(0, next_node)
                    visited[next_x][next_y][next_a] = True  # 標記走過
                    # show_path(next_node)

                    if isGoal(PFs, temp_robot) : # 找完路徑
                        # next_node = ListNode(next_confi, u)
                        # next_node.previous = pre_node
                        goalNode = next_node
                        SUCCESS = True

    if SUCCESS:
        print("Success")
        path = [goalNode]
        show_path(goalNode)
        node = copy.deepcopy(goalNode)
        while node.previous != None:
            path.insert(0, node.previous)
            node = node.previous
        path.insert(0, node)

        return path

    return "Fail"


class ListNode():
    def __init__(self, confi, u):
        self.confi = confi
        self.U = u
        self.previous = None

