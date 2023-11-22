import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np
from tabulate import tabulate 

d0 = pd.read_csv('experimentoverview.csv', sep=';')
d0['Starttime'] = pd.to_datetime(d0['Starttime']).dt.strftime('%Y/%m/%d %H:%M')
d0['Stoptime'] = pd.to_datetime(d0['Stoptime']).dt.strftime('%Y/%m/%d %H:%M')
print(tabulate(d0, headers = 'keys', tablefmt = 'plain'))

# Read metadata for all experiments except octagons
d1 = pd.read_csv('experimenttiming.csv', sep=';')
d1['Starttime'] = pd.to_datetime(d1['startTime'])
d1['Stoptime'] = pd.to_datetime(d1['endTime'])
d1.columns

# Read tagged data for Frigg during Malangen octagons
fr_ml = pd.read_csv('./data_reader_tr23/2023-11-17.csv', sep=',')
fr_ml['Location'] = 'Malangen'
fr_ml = fr_ml.rename(columns={"leg": "Leg", "coverage": "Coverage", "time": "Starttime"})
fr_ml['Starttime'] = pd.to_datetime(fr_ml['Starttime'])
# Add stop time based on previous start time
tmp = fr_ml['Starttime'].values[1:]
fr_ml['Stoptime'] = np.append(tmp, tmp[-1]+np.timedelta64(4, 'm'))

# Read tagged data for Frigg during Austehola octagons
fr_au = pd.read_csv('./data_reader_tr23/2023-11-17.csv', sep=',')
fr_au['Location'] = 'Austehola'
fr_au = fr_ml.rename(columns={"leg": "Leg", "coverage": "Coverage", "time": "Starttime"})
fr_au['Starttime'] = pd.to_datetime(fr_ml['Starttime'])
# Add stop time based on previous start time
tmp = fr_ml['Starttime'].values[1:]
fr_au['Stoptime'] = np.append(tmp, tmp[-1]+np.timedelta64(4, 'm'))

# Read tagged data for GOS during Malangen Octagons

# Read tagged data for GOS during Austehola Octagons

