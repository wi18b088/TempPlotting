import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import matplotlib

# Import data
sensordata = pd.read_excel("/home/albert/Desktop/Pietro/PythonPlotting/data/sensor-data.xlsx", "data")

# Show data
print(sensordata)
# print(sensordata.describe())
# print(sensordata.count())

# Plot data
# matplotlib.use("TKagg")
sb.displot(sensordata['Set Temperature [°C]'])
plt.show()