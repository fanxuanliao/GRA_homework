class Polygon():

    def __init__(self):
        self.vertiList = []

    def add_Verti(self, v):
        self.vertiList.append(v)

    def show_Poly(self):
        for vert in self.vertiList:
            print("(", vert.x, ",", vert.y, ")")


class Configuration():

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def show_Confi(self):
        print("x:", self.x, "y:", self.y, "angle:", self.angle)


class Vertice():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mod_Vertice(self, x, y):
        self.x = x
        self.y = y

    def show_Vertice(self):
        print("(",self.x,",",self.y,")")

    def ConvertVertical(self):
        temp = self.x
        self.x = self.y
        self.y = -temp
        return self

    def __sub__(self, o):
        v = Vertice(0,0)
        v.x = self.x- - o.x
        v.y = self.y - o.y
        return v
'''
    def mod_Vertice(self, V):
        self.x = V.x
        self.y = V.y
'''