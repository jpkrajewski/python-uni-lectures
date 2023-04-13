import pandas as pd

from conn import Database
from config import Config
from matplotlib import pyplot as plt


conn = Database()

# get the data from database
ID = Config('config.ini').get_param('id')
array = conn.fetch(f"SELECT time, temperature, humidity, voltage FROM data WHERE device_id = {ID}")

# transpose array to the DataFrame using Pandas
df = pd.DataFrame(array, columns=['time', 'temperature', 'humidity', 'voltage'])
print("Transposed array to DataFrame:")
print(df)

# draw plots
plt.rcParams["figure.figsize"] = (16, 9)

plt.subplot(3, 1, 1)
plt.plot(df['time'], df['temperature'])
plt.title('Temperature')
plt.xlabel('Time')
plt.ylabel('Temperature [degrees Celsius]')

plt.subplot(3, 1, 2)
plt.plot(df['time'], df['humidity'], '-g')
plt.title('Humidity')
plt.xlabel('Time')
plt.ylabel('Humidity [%]')

plt.subplot(3, 1, 3)
plt.plot(df['time'], df['voltage'], '-r')
plt.title('Voltage [V]')
plt.xlabel('Time')
plt.ylabel('Voltage [V]')

plt.subplots_adjust(hspace=0.5)  # add some space between plots
plt.show()
