import numpy as np
import matplotlib.pyplot as plt

R = 0.8
n2 = 1
omega = 3.6 * 10**14
y0 = -0.1
alpha = -30

def f1(y):
    return 1.4 - 0.18 * y ** 4

def Zf(y):
    return 8 + np.sin(17.951958020513104 * y)

def n1(y):
    return f1(y) * (1 - ((0.35 * 10**14)/omega)**2)


def startSin():
    n1_0 = n1(y0)
    sinBeta = np.sin(np.pi/2 - np.arcsin(np.sin(np.radians(abs(alpha))) * n2 / n1_0))
    return sinBeta, np.sign(alpha)


e = 0.0001

currY = y0
currZ = 0
currN = n1(currY)
currSin, direction = startSin()
S = 0

def step():
    global currY
    global currZ
    global currN
    global currSin
    global S
    global direction
    
    newY = currY + np.sqrt(1 - currSin**2) * e * direction
    newZ = currZ + np.abs(currSin) * e
    newN = n1(newY) if R >= abs(newY) else n2 
    newSin = (currSin * currN) / newN
    
    S += e
    currY = newY
    currZ = newZ
    
    if(abs(newSin) >= 1):
        direction *= -1
        return
    
    currN = newN
    currSin = newSin
    

pointsY = []
pointsZ = []

def start():
    while(currZ < Zf(currY)):
        pointsY.append(currY)
        pointsZ.append(currZ)
        step()
    
    print(S)
    t1 = np.arange(-R, R, 0.001)
    plt.plot(pointsZ, pointsY, Zf(t1), t1, [0,Zf(R)], [R, R], 'r', [0,Zf(-R)], [-R, -R], 'r')
    plt.show()
    

start()
