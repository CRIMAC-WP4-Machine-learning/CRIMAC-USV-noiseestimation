import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np
from functools import reduce

dr = './navigationdata/'
navfiles = [fil for fil in os.listdir(dr) if fil.split('.')[1] == 'json']
data = []

for i in range(len(navfiles)):
    with open(dr+navfiles[i], 'r') as my_file:
        data.append(json.load(my_file))

dat = []
i=0
# Loop over files
for _data in data:
    # Loop over datasets within the file
    dsets = [_d for _d in _data['datasets']]
    dat2 = []
    for _vars in dsets:
        #print(_vars['coordinateVariable'][0])
        td = _vars[_vars['coordinateVariable'][0]]
        tdi = [int(_td) for _td in td]
        d = _vars[_vars['dataVariable']]
        #print(_vars['dataVariable'])
        df0 = pd.DataFrame(data={'time': tdi, _vars['dataVariable']: d})
        dat2.append(df0)
    df = reduce(lambda left,right: pd.merge(left,right,on=['time'], how='outer'), dat2)
    df['time'] = pd.to_datetime(df['time'],unit='s')
    df['file'] = navfiles[i]
    i+=1
    dat.append(df)


DF = pd.concat(dat, axis = 0)
DF = DF.sort_values(by=['time'])
DF = DF.set_index('time')

DF.groupby(['file'])['vesselSpeed'].plot(legend='true')
plt.show()

