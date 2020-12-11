import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import matplotlib

# Import data
sensordata = pd.read_excel("data/humi.xlsx")
# sensordata = pd.read_excel("data/sensor-data.xlsx", "data")
sensordata.rename(columns={
    'Set Temperature [°C]':'Temperature',
    'Humidity [%]':'Humidity',
    'Heater? [1=on, 0=nothing, -1=ventilator]':'Heater',
    'Air Quality [-]':'Air Quality',
}, inplace=True)

# Show data
print(sensordata.columns.values)
# print(sensordata.describe())
# print(sensordata.count())

# Plot data
# matplotlib.use("TKagg")
# sb.displot(sensordata['Set Temperature [°C]'])

figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Temperature'])
figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Humidity']*100)
# figure = sb.lineplot(data = sensordata['Heater'])
figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Air Quality'])
# plt.yticks([0,20,40,60,80,100])
temp = 0
for i, val in enumerate(sensordata['Heater']):
    if val != temp:
        plt.axvline(sensordata.iloc[i]['Timestamp [s]'])
        temp = val
plt.show()