import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import matplotlib

# Import data
sensordata = pd.read_excel("data/sensor-data.xlsx", "data")
sensordata.rename(columns={
    'Set Temperature [°C]':'Temperature',
    'Humidity [%]':'Humidity',
    'Heater? [1=on, 0=nothing, -1=ventilator]':'Heater',
}, inplace=True)

# Show data
print(sensordata.columns.values)
# print(sensordata.describe())
# print(sensordata.count())

# Plot data
# matplotlib.use("TKagg")
# sb.displot(sensordata['Set Temperature [°C]'])

figure = sb.lineplot(data = sensordata['Temperature'])
figure = sb.lineplot(data = sensordata['Humidity'])
# figure = sb.lineplot(data = sensordata['Heater'])
# plt.yticks([0,20,40,60,80,100])
temp = 0
for i, val in enumerate(sensordata['Heater']):
    if val != temp:
        plt.axvline(i)
        temp = val
plt.show()