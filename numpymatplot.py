import numpy as np
import matplotlib.pyplot as plt

def rozkład_normalny(sigma, mu, minimum, maximum):
    x_values = np.linspace(minimum, maximum, 1000)
    y_values = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x_values - mu) ** 2) / (2 * sigma ** 2))
    return x_values, y_values

sigma = float(input("odchylenie standardowe σ: "))
mu = float(input("średnia rozkładu µ: "))
minimum = float(input("przedział dla obliczeń MIN: "))
maximum = float(input("przedział dla obliczeń MAKS: "))

x_values, y_values = rozkład_normalny(sigma, mu, minimum, maximum)

plt.plot(x_values, y_values)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("rozkład normalny")
plt.show()