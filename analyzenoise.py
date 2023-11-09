import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime

noisedata = 'EchogramPlot_T20051118_06201006-20051118_11251826.json'

with open(noisedata, 'r') as my_file:
    data = json.load(my_file)

time = [datetime.datetime.fromtimestamp(_t) for _t in data["time"]]

frames = [pd.DataFrame(index=time, data={'noiseAverage': data["noiseAverage"]}),
          pd.DataFrame(index=time, data={'noiseUpperLimit': data["noiseUpperLimit"]})]
df = pd.concat(frames, axis=1)

df.keys()
df.plot()
plt.show()
