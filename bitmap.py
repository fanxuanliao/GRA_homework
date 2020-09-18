import math
import sys
import copy
from Polygon import Vertice


def mark_ob(bitmap, itemList, mark_num):    #Draw obstacle on bitmap

    for O in itemList:
        sin = math.sin(math.radians(O.confi.angle))
        cos = math.cos(math.radians(O.confi.angle))

        for P in O.polyList:
            maxX, minX, maxY, minY = 0, 128, 0, 128 # 傳進fill的參數，界定fill的範圍


            for vIndex in range(len(P.vertiList)):
                V = P.vertiList

                #轉換公式
                #X = V.x * cos - sin * V.y + O.confi.x
                #Y = cv_height - (V.x * sin + cos * V.y + O.confi.y)
                if vIndex == len(P.vertiList)-1:
                    x1, y1, x2, y2 = V[vIndex].x*cos - sin*V[vIndex].y + O.confi.x, V[vIndex].x*sin + cos*V[vIndex].y + O.confi.y, \
                                     V[0].x*cos - sin*V[0].y + O.confi.x, V[0].x*sin + cos*V[0].y + O.confi.y
                else:
                    x1, y1, x2, y2 = V[vIndex].x*cos - sin*V[vIndex].y + O.confi.x, V[vIndex].x*sin + cos*V[vIndex].y + O.confi.y, \
                                     V[vIndex+1].x*cos - sin*V[vIndex+1].y + O.confi.x, V[vIndex+1].x*sin + cos*V[vIndex+1].y + O.confi.y

                d = (max(abs(x2 - x1), abs(y2 - y1)))*2  # 看y還x差比較多
                dx = (x2 - x1) / d  # 走一步
                dy = (y2 - y1) / d

                for i in range(0, int(d)): #找到要mark的座標
                    xi = int(x1 + i * dx)
                    yi = int(y1 + i * dy)

                    if xi < minX:
                        minX = xi
                    elif xi > maxX:
                        maxX = xi

                    if yi < minY:
                        minY = yi
                    elif yi > maxY:
                        maxY = yi

                    try:
                        bitmap[yi][xi] = mark_num  # mark polygon
                    except Exception as e:
                        print(e)

            fill(bitmap, minX, maxX+1, minY, maxY+1, mark_num)

def mark_r(bitmap, robot, mark_num):    #Draw robot on bitmap

    sin = math.sin(math.radians(robot.goalConfi.angle))
    cos = math.cos(math.radians(robot.goalConfi.angle))

    for P in robot.polyList:
        maxX, minX, maxY, minY = 0, 128, 0, 128 # 傳進fill的參數，界定fill的範圍


        for vIndex in range(len(P.vertiList)):
            V = P.vertiList

            #轉換公式
            if vIndex == len(P.vertiList)-1:
                x1, y1, x2, y2 = V[vIndex].x*cos - sin*V[vIndex].y + robot.goalConfi.x, V[vIndex].x*sin + cos*V[vIndex].y + robot.goalConfi.y, \
                                 V[0].x*cos - sin*V[0].y + robot.goalConfi.x, V[0].x*sin + cos*V[0].y + robot.goalConfi.y
            else:
                x1, y1, x2, y2 = V[vIndex].x*cos - sin*V[vIndex].y + robot.goalConfi.x, V[vIndex].x*sin + cos*V[vIndex].y + robot.goalConfi.y, \
                                 V[vIndex+1].x*cos - sin*V[vIndex+1].y + robot.goalConfi.x, V[vIndex+1].x*sin + cos*V[vIndex+1].y + robot.goalConfi.y

            d = (max(abs(x2 - x1), abs(y2 - y1)))*2  # 看y還x差比較多
            dx = (x2 - x1) / d  # 走一步
            dy = (y2 - y1) / d

            for i in range(0, int(d)): #找到要mark的座標
                xi = int(x1 + i * dx)
                yi = int(y1 + i * dy)

                if xi < minX:
                    minX = xi
                elif xi > maxX:
                    maxX = xi

                if yi < minY:
                    minY = yi
                elif yi > maxY:
                    maxY = yi

                try:
                    bitmap[yi][xi] = mark_num  # mark polygon
                except Exception as e:
                    print(e)

        fill(bitmap, minX, maxX+1, minY, maxY+1, mark_num)
    spread(bitmap, robot)


def fill(bitmap, x, X, y, Y, mark_num): #找出邊之後把裡面填充
    for i in range(X-x): #縱向掃過bitmap
        FINDUPPER = False
        upper, lower = -1, -1
        for j in range(Y-y):
            if bitmap[y+j][x+i] == mark_num and FINDUPPER == False and bitmap[y+j+1][x+i] != mark_num: #上界
                FINDUPPER = True
                upper = y + j
                spreadP = (y+j, x+i)
            elif bitmap[y+j][x+i] == mark_num and FINDUPPER == True: #下界
                lower = y + j
                for k in range(lower-upper):
                    bitmap[upper + k][x + i] = mark_num
                FINDUPPER = False
                upper, lower = -1, -1

#回傳PField要填的值
def minValue(bitmap, Point):
    values = []
    if int(bitmap[Point[0] - 1][Point[1] - 1]) < int(bitmap[Point[0]][Point[1]]):  # 左上
        values.append(int(bitmap[Point[0] - 1][Point[1] - 1]))
    if int(bitmap[Point[0] - 1][Point[1]]) < int(bitmap[Point[0]][Point[1]]):  # 上
        values.append(int(bitmap[Point[0] - 1][Point[1]]))
    if int(bitmap[Point[0] - 1][Point[1]+1]) < int(bitmap[Point[0]][Point[1]]):  # 右上
        values.append(int(bitmap[Point[0] - 1][Point[1]+1]))
    if int(bitmap[Point[0]][Point[1] - 1]) < int(bitmap[Point[0]][Point[1]]):  # 左
        values.append(int(bitmap[Point[0]][Point[1] - 1]))
    if int(bitmap[Point[0]][Point[1] + 1]) < int(bitmap[Point[0]][Point[1]]):  # 右
        values.append(int(bitmap[Point[0]][Point[1] + 1]))
    if int(bitmap[Point[0]+1][Point[1] - 1]) < int(bitmap[Point[0]][Point[1]]):  # 左下
        values.append(int(bitmap[Point[0]+1][Point[1] - 1]))
    if int(bitmap[Point[0]+1][Point[1] - 1]) < int(bitmap[Point[0]][Point[1]]):  # 下
        values.append(int(bitmap[Point[0]+1][Point[1] - 1]))
    if int(bitmap[Point[0]+1][Point[1]+1]) < int(bitmap[Point[0]][Point[1]]):  # 左下
        values.append(int(bitmap[Point[0]+1][Point[1]+1]))

    if values == []:
        return 0
    else:
        return min(values)+1

#檢查目前點是否在bitmap中
def isInRange(x,y):
    if x >= 128 or x >= 128 or y >= 128 or y >= 128 or x < 0 or x < 0 or y < 0 or y < 0: #超出範圍
        return False
    else: #範圍內
        return True

def isEmpty(val):
    if val == 254:
        return True
    else:
        return False

# output potential fields
def spread(bitmap, robot):
    current = []
    next = []
    CPs = robot.controlPoints
    trans_CP = []
    sin = math.sin(math.radians(robot.goalConfi.angle))
    cos = math.cos(math.radians(robot.goalConfi.angle))

    for CP in CPs:
        #V[vIndex].x*cos - sin*V[vIndex].y + O.goalConfi.x, V[vIndex].x*sin + cos*V[vIndex].y
        x = int(CP.x*cos - sin*CP.y + robot.goalConfi.x)
        y = int(CP.x*sin + cos*CP.y + robot.goalConfi.y)
        trans_CP.append(Vertice(x, y))

    #print("CPs:",trans_CP)

    count = 0
    PFs = []
    for CP in trans_CP: #一個control point 一張potential field

        #intialize
        #print(count)
        del current[:]
        del next[:]
        PF = copy.deepcopy(bitmap)
        # print("PF in spread",PF)
        PFs.append(PF)
        PF[CP.y][CP.x] = '  0'
        #print("CP:",CP[0],CP[1])

        current.append(CP)  #current要是control point，從control point擴散

        while(1):
            #print(PF[80][92], PF[80][78])
            for C in current:
                if isInRange(C.y - 1, C.x) and isEmpty(PF[C.y - 1][C.x]):  # 上
                    PF[C.y - 1][C.x] = "{:>3d}".format(int(PF[C.y][C.x])+1)
                    next.append(Vertice(C.x, C.y-1))

                if isInRange(C.y, C.x - 1) and isEmpty(PF[C.y][C.x - 1]):  # 左
                    PF[C.y][C.x - 1] = "{:>3d}".format(int(PF[C.y][C.x])+1)
                    next.append(Vertice(C.x-1, C.y))

                if isInRange(C.y, C.x + 1) and isEmpty(PF[C.y][C.x + 1]):  # 右
                    PF[C.y][C.x + 1] = "{:>3d}".format(int(PF[C.y][C.x])+1)
                    next.append(Vertice(C.x + 1, C.y))

                if isInRange(C.y + 1, C.x) and isEmpty(PF[C.y + 1][C.x]):  # 下
                    PF[C.y + 1][C.x] = "{:>3d}".format(int(PF[C.y][C.x])+1)
                    next.append(Vertice(C.x, C.y + 1))


            current = next.copy()
            if (next == []):
                break
            next.clear()

        #寫進檔案
        with open("./Potential_Field"+str(count)+".txt", mode="w") as file:
            for i in PF:
                # print(str(i))
                for j in i:
                    file.write(str(j))
                    file.write(" ")
                file.write('\n')

        file.close()

        count += 1

    # print(PF)
    return PFs


def draw_Bitmap(obstacleList, robot):
    bitmap = [[254 for i in range(128)] for i in range(128)]  # 2D array bitmap initialize
    mark_ob(bitmap, obstacleList, '255') #bitmap
    #mark_r(bitmap, robot, '  0')
    #spread(bitmap, robot) #potential field

    with open("./bitmap.txt", mode="w") as file:

        for i in bitmap:
            #print(str(i))
            for j in i:
                file.write(str(j))
                file.write(" ")
            file.write('\n')

    file.close()
    return bitmap
