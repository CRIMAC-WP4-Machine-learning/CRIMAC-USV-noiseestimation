import pandas as pd
import json
import matplotlib.pyplot as plt
noisedata = 'EchogramPlot_T20051118_06201006-20051118_11251826.json'

with open(noisedata, 'r') as my_file:
    data = json.load(my_file)

frames = [pd.DataFrame(index=data["time"], data={'noiseAverage': data["noiseAverage"]}),
          pd.DataFrame(index=data["time"], data={'noiseUpperLimit': data["noiseUpperLimit"]})]
df = pd.concat(frames, axis=1)

#data["time"]

df.keys()
df.plot()
plt.show()
