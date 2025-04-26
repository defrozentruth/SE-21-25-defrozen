import numpy as np
import matplotlib.pyplot as plt

R = 1.2
n2 = 1
def f1(y):
    return 1.2 + 0.3 * (np.cos(0.8 * y))**3

def Zf(y):
    return 42 + 3 * np.sin(17.951958020513104*y)

omega = 3.2 * 10**14
y0 = -0.3
alpha = -22



def getN1(y):
    return f1(y) * (1 - ((0.35 * 10**14)/omega)**2)


def getStartSin():
    n1_0 = getN1(y0)
    sinBeta = np.sin(np.pi/2 - np.arcsin(np.sin(np.radians(abs(alpha))) * n2 / n1_0))
    return sinBeta, np.sign(alpha)


hop = 0.0001

currentY = y0
currentZ = 0
currentN = getN1(currentY)
currentSin, direction = getStartSin()
totalLength = 0

def makeStep():
    global currentY
    global currentZ
    global currentN
    global currentSin
    global totalLength
    global direction
    
    newY = currentY + np.sqrt(1 - currentSin**2) * hop * direction
    newZ = currentZ + np.abs(currentSin) * hop
    newN = getN1(newY) if R >= abs(newY) else n2 
    newSin = (currentSin * currentN) / newN
    
    totalLength += hop
    currentY = newY
    currentZ = newZ
    
    if(abs(newSin) >= 1):
        direction *= -1
        return
    
    currentN = newN
    currentSin = newSin
    

pointsByY = []
pointsByZ = []

def start():
    while(currentZ < Zf(currentY)):
        pointsByY.append(currentY)
        pointsByZ.append(currentZ)
        makeStep()
    
    print(totalLength)
    t1 = np.arange(-R, R, 0.001)
    plt.plot(pointsByZ, pointsByY, Zf(t1), t1, [0,Zf(R)], [R, R], 'g', [0,Zf(-R)], [-R, -R], 'g')
    plt.show()
    

start()