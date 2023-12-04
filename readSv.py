import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import xarray as xr
import numpy as np
from datetime import timedelta


def readluf(noisedata):
    df = pd.read_csv(noisedata, header=5)
    d1 = df['DepthStop'][0]
    d0 = df['DepthStart'][0]
    n = int(df['SampleCount'][0])
    depth = pd.Series(range(0, n))*(d1-d0)/n + d0

    df['year'] =  df['Date'] // 10000
    df['month'] =  df['Date'] // 100 - df['year']*100
    df['day'] =  df['Date'] - df['year']*10000 - df['month']*100

    H = df['Time'] // 1000000
    M = df['Time'] // 10000 - H*100
    S = (df['Time'] - H*1000000 - M*10000)/100
    sec = (H*3600 + M*60 + S)
    df['sec'] = sec + 3600
    df['td'] = df['sec'].apply(lambda x: timedelta(seconds=x))
    df['t'] = pd.to_datetime(df[['year', 'month', 'day']]) + df['td']

    df.iloc[:, 11:11+n] = df.iloc[:, 11:11+n].apply(pd.to_numeric,
                                                    errors='coerce')
    # Convert to linear values
    df.iloc[:, 11:11+n] = df.iloc[:, 11:11+n].apply(lambda x: 10**(x/10))

    dat = xr.DataArray(df.iloc[:, 11:11+n].values, dims=(
        'Time', 'Depth'), coords={'Time': df['t'], 'Depth': depth}, name='sa')
    sa = dat.sum(dim='Depth').to_dataframe()
    return sa

'''
Sa.plot()
plt.show()
'''

# These files are found under /data/cruisedata/

# List all data files
drr = 'ACOUSTIC/LSSS/EXPORT/Sv/'
dr = ['/mnt/c/DATA/cruisedata/S2023301002_PFRIGG_10318/'+drr,
      '/mnt/c/DATA/cruisedata/S2023001016_PGOSARS_4174/'+drr]
noisedata = []
for _d in dr:
    noisedata = noisedata + [_d+fil for fil in os.listdir(
        _d) if fil.split('.')[1] == 'txt']

# Read data files
DFbot = pd.DataFrame()
for i in range(len(noisedata)):
    with open(noisedata[i], 'r') as my_file:
        # Use the file names to parse the metadata
        filename = noisedata[i].split('/')[-1].split('_')
        # Remove the Sv files
        if filename[2].split('Echogram')[0][:-2] == 'Sv':
            print(filename)
            dfbot = readluf(noisedata[i])
            dfbot['Platform'] = filename[0]
            dfbot['Location'] = filename[1]
            dfbot['Frequency'] = filename[2][-2:]
            dfbot['Mode'] = 'CW'
            DFbot = pd.concat([DFbot, dfbot], axis=0)

DFbot['sa'] = pd.to_numeric(DFbot['sa'], errors='coerce')

DFbot.loc[(DFbot['Location'] == 'Octagon2') & (
    DFbot['Platform'] == 'GOSars'), 'Location'] =  'Austerhola'
DFbot.loc[(DFbot['Location'] == 'Octagon3') & (
    DFbot['Platform'] == 'GOSars'), 'Location'] =  'Malangen'

DFbot.loc[(DFbot['Location'] == 'Octagon1') & (
    DFbot['Platform'] == 'Frigg'), 'Location'] =  'Malangen'
DFbot.loc[(DFbot['Location'] == 'Octagon2') & (
    DFbot['Platform'] == 'Frigg'), 'Location'] =  'Austerhola'

DFbot.groupby(['Location', 'Platform'])['sa'].plot(legend=True)
plt.show()

DFbot2 = DFbot.reset_index()
DFbot2 = DFbot2.rename(columns = {'index': 'Time'})
DFbot2 = DFbot2.sort_values(by=['Time'])
DFbot2.to_pickle('readSv.pk')
