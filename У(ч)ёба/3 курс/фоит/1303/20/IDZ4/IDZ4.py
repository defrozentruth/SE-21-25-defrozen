import numpy as np
import sounddevice as sd
import scipy.signal as signal
import matplotlib.pyplot as plt


# Функция для чтения цифрового сигнала из файла
def read_signal(file_path):
    with open(file_path, 'r') as file:
        signal = []
        for line in file:
            # Разделяем строку на биты и преобразуем их в целые числа
            bits = [int(bit) for bit in line.split()]
            # Преобразуем список битов в десятичное число
            number = int("".join(map(str, bits)), 2)
            signal.append(number)
    return signal


# Функция фильтра Баттерворта


def butterworth_filter(data, sample_rate, cutoff, order):
    # Нормализация частоты среза
    nyquist = 0.5 * sample_rate # Частота Найквиста
    normal_cutoff = cutoff / nyquist  # Нормализованная частота среза

    # Создание фильтра
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)  # Фильтр Баттерворта низких частот 6 порядка

    # Применение фильтра к сигналу
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data


# Визуализация сигнала
def plot_signal(signal, time_axis, title):
    plt.plot(time_axis, signal)
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.title(title)
    plt.grid()
    plt.show()


# Визуализация спектра сигнала
def fftPlot(signal, title='Спектр сигнала'):
    fft_result = np.fft.fft(signal)
    n = len(fft_result)
    freqs = np.fft.fftfreq(n, dt)
    freqs = freqs[:n // 2]  # Берем только половину спектра (положительные частоты)
    fft_result = fft_result[:n // 2]

    plt.figure(figsize=(8, 6))
    plt.plot(freqs, np.abs(fft_result))
    plt.title(title)
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда')
    plt.grid()
    plt.show()



def plot_butterworth_response(sample_rate, cutoff, order):
    # Получаем коэффициенты фильтра
    b, a = signal.butter(order, cutoff / (0.5 * sample_rate), btype='low')
    # Получаем частотную характеристику
    w, h = signal.freqz(b, a, worN=8000)
    # Рисуем АЧХ
    plt.semilogx(w * sample_rate / (2 * np.pi), np.abs(h))  # Переводим частоту в Гц
    plt.title('АЧХ фильтра Баттерворта')
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда')
    plt.grid()
    plt.show()


t = 2.75

# Путь к файлу с вашим сигналом
file_path = "signaldigit20.txt"
# Чтение и преобразование сигнала
digital_signal = read_signal(file_path)

# Расчет частоты дискретизации
dt = t / len(digital_signal)  # Время дискретизации
sample_rate = 1 / dt  # Частота дискретизации

# Нормализация сигнала к диапазону от -1 до 1
analog_signal = np.array(digital_signal)
analog_signal = (analog_signal - np.min(analog_signal)) / (
        np.max(analog_signal) - np.min(analog_signal))  # Нормализация
analog_signal = 2 * analog_signal - 1  # Приведение к диапазону от -1 до 1

# Визуализация сигнала
time_axis = np.linspace(0, t, len(analog_signal))
plot_signal(analog_signal, time_axis, 'Сигнал')
fftPlot(analog_signal)

# Применение фильтра Баттерворта
cutoff_frequency = 1200  # Частота среза в Гц
filter_order = 6  # Порядок фильтра
filtered_signal = butterworth_filter(analog_signal, sample_rate, cutoff_frequency, filter_order)

# Визуализация отфильтрованного сигнала
plot_signal(filtered_signal, time_axis, 'Отфильтрованный сигнал')
fftPlot(filtered_signal, 'Спектр сигнала после')

# ачх фильтра
plot_butterworth_response(sample_rate, cutoff_frequency, filter_order)

sd.play(analog_signal, samplerate=int(sample_rate))
sd.wait()

sd.play(filtered_signal, samplerate=int(sample_rate))
sd.wait()
