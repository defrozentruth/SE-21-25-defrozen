import math
import matplotlib.pyplot as plt
import numpy as np

R = 1.8
n2 = 1
w = 3.5 * 10 ** 14
initial_y = -0.5
alpha_deg = -42
length = 0
hop = 0.00001
direction = 1 if alpha_deg > 0 else -1


def f1(y):
    return 1.4 + 0.3 * math.cos(0.8 * y) ** 2


def Zf(y):
    return 12 + 3 * math.sin(17.951958020513104 * y)


def n1(y):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)


def angle_refraction(input_angle, next_refractive_index, current_refractive_index):
    angle = (math.sin(input_angle) * current_refractive_index) / next_refractive_index
    if angle > 1:
        global direction
        direction *= -1
        return input_angle
    return math.asin(angle) if -1 <= angle <= 1 else input_angle


def calculate_optical_path():
    global length
    global direction
    n1_input = n1(initial_y)
    entry_angle = angle_refraction(math.radians(alpha_deg), n1_input, n2)
    print("Угол β = %.6f " % math.degrees(entry_angle))
    entry_angle = math.pi / 2 - entry_angle

    Y_values, Z_values = [], []
    current_Y, current_Z, current_N = initial_y, 0, n1_input

    while current_Z < Zf(current_Y):
        Y_values.append(current_Y)
        Z_values.append(current_Z)
        next_Y = current_Y + math.cos(entry_angle) * hop * direction
        next_Z = current_Z + abs(math.sin(entry_angle)) * hop
        next_N = n1(next_Y) if R >= abs(next_Y) else n2
        next_angle = angle_refraction(entry_angle, next_N, current_N)
        length += hop
        current_Y, current_Z, entry_angle, current_N = next_Y, next_Z, next_angle, next_N

    plt.plot(Z_values, Y_values, color="red")



plt.figure(figsize=(8, 3))
plt.xlim(-2, 17)
plt.ylim(-2, 2)

plt.plot([0, 9.6545], [-R, -R], color='green')
plt.plot([0, 14.34], [R, R], color='green')
plt.yticks([-R, 0, R], ['-1.8', '0', '1.8'])


plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.plot([-2, 0], [initial_y + math.tan(math.radians(alpha_deg)) * (-2), initial_y], color='black', linewidth=2)


Y_array = np.linspace(-R, R, 100)
Z_array = [Zf(v) for v in Y_array]
plt.plot(Z_array, Y_array, color="green")

calculate_optical_path()
print(f"Длина пути = {length}")
plt.show()
