import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import random

outerV = 0
firstV = -6
secondV = 5

VtoFind = 4

equationError = 0.01

def outerElEquation(x, y):
    result = pow(x,2) + pow(y,2)
    
    return result - 25
    

def firstElEquation(x, y):
    result = pow(np.abs(1.8 + x),2) + pow(np.abs(1.8 + y), 2)
    
    return result - 0.7
    
def secondElEquation(x, y):
    result = pow(np.abs(-1.8 + x),2) + 0.8 * pow(np.abs(-1.8 + y), 2)
    
    return result - 0.7

class Vpoint:
    def __init__(self,x,y,V):
        self.x = x
        self.y = y
        self.V = V
        self.needed = True


pointsPerSide = 200
squareRadius = 6


points = [[Vpoint(-squareRadius + 2*squareRadius * x/pointsPerSide,
                  -squareRadius + 2*squareRadius * y/pointsPerSide,
                  firstV + random.random() * (secondV - firstV)) for y in range(pointsPerSide)] for x in range(pointsPerSide)]

visibleX = []
visibleY = []

#marking edges
for x in range(pointsPerSide):
    for y in range(pointsPerSide):
        
        result = outerElEquation(points[x][y].x, points[x][y].y)
        if(result > 0 - 0.5 and result < 0 + 0.5):
            visibleX.append(points[x][y].x)
            visibleY.append(points[x][y].y)
        
        if result >= 0:
            points[x][y].V = outerV
            points[x][y].needed = False
            continue
        
        result = firstElEquation(points[x][y].x, points[x][y].y)
        if(result > 0 - 0.1 and result < 0 + 0.1):
            visibleX.append(points[x][y].x)
            visibleY.append(points[x][y].y)
        
        if result <= 0:
            points[x][y].V = firstV
            points[x][y].needed = False
            continue
        
        result = secondElEquation(points[x][y].x, points[x][y].y)
        if(result > 0 - 0.1 and result < 0 + 0.1):
            visibleX.append(points[x][y].x)
            visibleY.append(points[x][y].y)
        
        if result <= 0:
            points[x][y].V = secondV
            points[x][y].needed = False
            continue

plt.scatter(visibleX, visibleY, c="blue", s=2)


Vprecision = 0.001
def iterateV():
    newV = [[0 for y in range(pointsPerSide)]for x in range(pointsPerSide)]
    
    for x in range(pointsPerSide):
        for y in range(pointsPerSide):
            if(points[x][y].needed):
                newV[x][y] = (points[x + 1][y].V +
                              points[x][y + 1].V +
                              points[x - 1][y].V +
                              points[x][y - 1].V) / 4
    
    isLastIteration = True
    for x in range(pointsPerSide):
        for y in range(pointsPerSide):
            if points[x][y].needed:
                if np.abs(points[x][y].V - newV[x][y]) > Vprecision:
                    isLastIteration = False
                points[x][y].V = newV[x][y]
                
    if not isLastIteration:
        return True
    else:
        return False
                
a = True
while(a):
    a = iterateV()



def getColor(v):
    x = (v - firstV) / (secondV - firstV)
    return [x,x,x]

Xx = []
Yy = []
colors = []

for x in range(pointsPerSide):
    for y in range(pointsPerSide):
        if(points[x][y].needed):
            Xx.append(points[x][y].x)
            Yy.append(points[x][y].y)
            colors.append(getColor(points[x][y].V))
                
plt.scatter(Xx, Yy, c=colors, s=1)


eq_list = []

def f(variables) :
    (a,k1,k2) = variables
    res = []
    for eq in eq_list:
        res.append(eval(eq))
    return res


    

def getLengthOnSquare(LTPoint, RTPoint, LBPoint, RBPoint):
    global eq_list
    
    points = []
    
    eq_list = [
        "a + k1 *" + str(LTPoint.x) + "+ k2 * " + str(LTPoint.y) + " - " + str(LTPoint.V),
        "a + k1 *" + str(RTPoint.x) + "+ k2 * " + str(RTPoint.y) + " - " + str(RTPoint.V),
        "a + k1 *" + str(LBPoint.x) + "+ k2 * " + str(LBPoint.y) + " - " + str(LBPoint.V)
    ]
    (a, k1, k2) = fsolve(f,[1,1,1])
    
    xT = (VtoFind - a - k2 * LTPoint.y)/k1
    if(xT > LTPoint.x and xT < RTPoint.x):
        plt.scatter(xT, LTPoint.y, c='red', s=1)
        points.append((xT, LTPoint.y))
        
    yL = (VtoFind - a - k1 * LTPoint.x)/k2
    if(yL > LBPoint.y and yL < LTPoint.y):
        plt.scatter(LTPoint.x, yL, c='red', s=1)
        points.append((LTPoint.x, yL))
        
    eq_list = [
        "a + k1 *" + str(RBPoint.x) + "+ k2 * " + str(RBPoint.y) + " - " + str(RBPoint.V),
        "a + k1 *" + str(RTPoint.x) + "+ k2 * " + str(RTPoint.y) + " - " + str(RTPoint.V),
        "a + k1 *" + str(LBPoint.x) + "+ k2 * " + str(LBPoint.y) + " - " + str(LBPoint.V)
    ]
    (a, k1, k2) = fsolve(f,[1,1,1])
    
    xB = (VtoFind - a - k2 * RBPoint.y)/k1
    if(xB > LBPoint.x and xB < RBPoint.x):
        plt.scatter(xB, RBPoint.y, c='red', s=1)
        points.append((xB, RBPoint.y))
        
    yR = (VtoFind - a - k1 * RBPoint.x)/k2
    if(yR > RBPoint.y and yR < RTPoint.y):
        plt.scatter(RBPoint.x, yR, c='red', s=1)
        points.append((RBPoint.x, yR))
        
    print(len(points))
    if(len(points) == 2):
        return np.sqrt(pow(np.abs(points[0][0] - points[1][0]),2) + pow(np.abs(points[0][1] - points[1][1]),2))
    
    return 0
    
totalLength = 0

for x in range(pointsPerSide):
    for y in range(pointsPerSide):
        if(points[x][y].needed):
            if(points[x][y].V < VtoFind + 0.3 and
               points[x][y].V > VtoFind - 0.3):
                totalLength += getLengthOnSquare(points[x][y],
                                                 points[x + 1][y],
                                                 points[x][y - 1],
                                                 points[x + 1][y - 1])


print(totalLength)

plt.show()

