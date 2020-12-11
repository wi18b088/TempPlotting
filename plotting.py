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
    'Humidex [°C]':'Humidex',
}, inplace=True)

# Show data
print(sensordata.columns.values)
# print(sensordata.describe())
# print(sensordata.count())

# Plot data
# matplotlib.use("TKagg")
# sb.displot(sensordata['Set Temperature [°C]'])

figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Temperature'], label="Temperature")
figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Humidity']*100, label="Humidity")
# figure = sb.lineplot(data = sensordata['Heater'])
figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Air Quality'], label="Air Quality")
figure = sb.lineplot(x = sensordata['Timestamp [s]'], y = sensordata['Humidex'], label="Humidex")
# plt.yticks([0,20,40,60,80,100])
temp = 0
for i, val in enumerate(sensordata['Heater']):
    if val != temp:
        plt.axvline(sensordata.iloc[i]['Timestamp [s]'])
        temp = val
figure.legend()
figure.set_title("Parameters over Time")
figure.set_ylabel("")
plt.show()