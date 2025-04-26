import matplotlib.pyplot as plot
import numpy as np

N = 8192
dt = 0.0196349540849362
L1 = 12.6488778185597
L2 = 0.451427837343368
C1 = 1.15154953201999E-05
C2 = 1.07110850608727E-05
R1 = 116.145703538366
R2 = 30.975023601527
R3 = 1076.85895580541
R4 = 539.745493386786

signalR = np.loadtxt("C:\\Users\\Полина\\PycharmProjects\\foit3\\23.txt")
spectre = np.fft.fft(signalR)
spectre_module = [abs(number) for number in spectre]

def signal(signal):
    time = [dt * i for i in range(N)]
    plot.title('Сигнал')
    plot.xlabel('t')
    plot.ylabel('s')
    plot.plot(time, signal)
    plot.show()

def amplitude(seq,is_stop):
    plot.title('Амплитуда')
    plot.xlabel('ω')
    plot.ylabel('A')
    plot.plot(seq[:is_stop], spectre_module[:is_stop])
    plot.show()

def h(w):
    j= complex(0, 1)
    Z_C1= 1 / (j * w * C1)
    Z_C2= 1 / (j * w * C2)
    Z_L1= j * w * L1
    Z_L2= j * w * L2
    R_input= R1 + Z_L1 + (R4 + Z_C2) * (R2 + R3 + Z_C1 + Z_L2) / (R2 + R3 + R4 + Z_C1 + Z_C2 + Z_L2)
    R_output= (R4 + Z_C2) * R2 / (R2 + R3 + R4 + Z_C1 + Z_C2 + Z_L2)
    return R_output / R_input

def draw_afr(is_stop, seq):
    plot.title('|H|')
    plot.xlabel('ω, рад/c')
    plot.ylabel('|H|')
    plot.plot(seq[1:is_stop], H[:is_stop-1])
    plot.show()

df= 1 / (dt * N)
seq= [2 * np.pi * df * i for i in range(N)]
H = [abs(h(omega)) for omega in seq[1:]]

def main():
    is_stop = round(50 / (np.pi * df)) + 1
    result= h(35)
    signal(signalR)
    amplitude(seq, is_stop)
    draw_afr(is_stop, seq)
    print(abs(result))

main()

