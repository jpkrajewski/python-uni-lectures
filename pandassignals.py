import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
csv = pd.read_csv('data.csv')

# Dodaj na początek kolumnę czasu oraz na koniec kolumnę z
# przyspieszeniem wypadkowym oraz zapisz całość jako nowy plik csv

csv['time'] = pd.date_range(start='1/1/2018', periods=len(csv), freq='S')
csv['acceleration'] = csv['ax'] + csv['ay'] + csv['az']
csv.to_csv('data_with_time.csv', index=False)

# Oblicz FFT dla wszystkich osi, a wyniki
# zaprezentuj na wykresie oraz zapisz je do pliku.
# Napisz fragment kodu, który znajduje częstotliwość wiodącą

series_axis = ['ax', 'ay', 'az']
df = pd.DataFrame()
fs = 6666  # częstotliwość próbkowania

for serie in series_axis:
    window = np.hamming(len(csv[serie]))  # okno czasowe
    fft = np.abs(np.fft.rfft(csv[serie] * window))  # wartość FFT
    freq = np.fft.rfftfreq(len(csv[serie]), 1 / fs)
    df[serie] = fft
    # Częstotliwość wiodąca
    print(fft.max())
    # Wykres FFT
    plt.plot(freq, fft)
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("FFT")
    plt.title("FFT dla osi " + serie)
    plt.show()

df.to_csv('fft.csv', index=False)
