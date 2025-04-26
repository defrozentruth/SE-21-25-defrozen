import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
from matplotlib.tri import Triangulation
from skimage.measure import find_contours


N = 400
R = 5
h = 2*R/N
mesh = []
for i in range(N):
    mesh.append([None]*N)
x_arr = []
y_arr = []
a1 = (0.7/0.8)**(1/2)
b1 = 0.7**(1/2)
a2 = (0.5/0.3)**(1/2.5)
b2 = 0.5**(1/2.5)
v0 = 1
v1 = 5
v2 = -5


def f(x, y):
    x = x*h - 5
    y = y*h - 5
    if 0.8*abs(1.5 + x)**2 + abs(-1.5 + y)**2 > 0.7 and 0.3*abs(-1.5 + x)**2.5 + abs(1.5 + y)**2.5 > 0.5 and x**2 + y**2 < 25:
        return True
    return False

def cathode(i, j):
    if ((i-N/2)*h)**2 + ((j-N/2)*h)**2 > 24.7:
        return False
    if mesh[i+1][j] is None or mesh[i][j+1] is None or mesh[i-1][j] is None or mesh[i][j-1] is None:
        return True
    return False


def rho(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)


def main():
    data = [[], [], []]
    for i in range(N):
        for j in range(N):
            if f(i, j):
                mesh[i][j] = 0

    for i in range(N):
        for j in range(N):
            if mesh[i][j] is not None and cathode(i, j):
                if i > j:
                    mesh[i][j] = -5
                else:
                    mesh[i][j] = 5

    for k in range(400):
        for i in range(N-1):
            for j in range(N-1):
                if mesh[i][j] is not None and mesh[i][j+1] is not None and not cathode(i, j+1):
                    mesh[i][j+1] = (mesh[i][j+1] + mesh[i][j])/2
                if mesh[i][j] is not None and mesh[i+1][j] is not None and not cathode(i+1, j):
                    mesh[i+1][j] = (mesh[i+1][j] + mesh[i][j])/2
        for i in range(N-1, 0, -1):
            for j in range(N-1, 0, -1):
                if mesh[i][j] is not None and mesh[i][j-1] is not None and not cathode(i, j-1):
                    mesh[i][j-1] = (mesh[i][j-1] + mesh[i][j])/2
                if mesh[i][j] is not None and mesh[i-1][j] is not None and not cathode(i-1, j):
                    mesh[i-1][j] = (mesh[i-1][j] + mesh[i][j])/2

    for i in range(N):
        for j in range(N):
            if mesh[i][j] is not None:
                data[0].append(i*h)
                data[1].append(j*h)
                data[2].append(mesh[i][j])


    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection="3d")
    #ax.plot_trisurf(data[0], data[1], data[2], cmap="viridis", linewidth=0, alpha=1)

    intersection_points = []

    for i in range(len(data[0]) - 1):
        x1, y1, z1 = data[0][i], data[1][i], data[2][i]
        x2, y2, z2 = data[0][i + 1], data[1][i + 1], data[2][i + 1]

        if (z1 < 1 and z2 > 1) or (z1 > 1 and z2 < 1):
            t = abs(z1 - 1) / (abs(z1 - 1) + abs(z2 - 1))
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            intersection_points.append((intersection_x, intersection_y, 1))

    intersection_points = np.array(intersection_points).T
    #ax.plot(intersection_points[0], intersection_points[1], intersection_points[2])

    build_points = [[], [], []]
    for i in range(len(intersection_points[0])):
        build_points[0].append(intersection_points[0][i])
        build_points[1].append(intersection_points[1][i])
        build_points[2].append(intersection_points[2][i])

    first = []
    last = []
    for i in range(len(intersection_points[0])//2):
        first.append(build_points[0][2*i+1])
        last.insert(0, build_points[0][2*i])



    build_points[0] = []
    build_points[0].extend(first)
    build_points[0].extend(last)

    first = []
    last = []
    for i in range(len(intersection_points[1]) // 2):
        first.append(build_points[1][2 * i + 1])
        last.insert(0, build_points[1][2 * i])

    build_points[1] = []
    build_points[1].extend(first)
    build_points[1].extend(last)

    length = 0
    for i in range(len(build_points[0])-1):
        length += rho(build_points[0][i], build_points[1][i], build_points[0][i+1], build_points[1][i+1])
    length += rho(build_points[0][0], build_points[1][0], build_points[0][-1], build_points[1][-1])

    print(length)

    #plt.show()


if __name__ == "__main__":
    main()
