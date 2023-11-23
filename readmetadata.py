import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate 


def cleanmetadata(fil):
    # Read tagged data for Frigg during Malangen octagons
    df = pd.read_csv(fil, sep=',')
    df = df.rename(columns={"sog": "Speed", "leg": "Leg", "coverage": "Coverage", "time": "Starttime"})
    df['Starttime'] = pd.to_datetime(df['Starttime'])
    df['Coverage'] = df['Coverage'].astype('int')
    # Add stop time based on previous start time
    tmp = df['Starttime'].values[1:]
    df['Stoptime'] = np.append(tmp, tmp[-1]+np.timedelta64(4, 'm'))
    df['Experiment'] = 'Dataquality'
    # Speedbin is not in data
    df['Speedbin'] = 0
    df.loc[np.append(False, np.diff(df['Leg']) < 0), 'Speedbin'] = 1
    df['Speedbin'] = (np.cumsum(df['Speedbin'])-df['Coverage']*4)*2+1
    df['Headingtowind'] =  df['true_wind_dir'] - df['cog']
    # Drop data
    df = df.drop(['cog', 'index'], axis=1)
    return df


# Read tagged data for Frigg during Malangen octagons
fr_ml = cleanmetadata('./data_reader_tr23/2023-11-17.csv')
fr_ml['Location'] = 'Malangen'
fr_ml['Platform'] = 'Frigg'
# Read tagged data for Frigg during Austehola octagons
fr_au = cleanmetadata('./data_reader_tr23/2023-11-18.csv')
fr_au['Location'] = 'Austehola'
fr_au['Platform'] = 'Frigg'

# Read tagged data for GOS during Malangen Octagons

# Read tagged data for GOS during Austehola Octagons

# Read metadata for all experiments except octagons
d1 = pd.read_csv('experimenttiming.csv', sep=';')
d1['Starttime'] = pd.to_datetime(d1['startTime']).dt.tz_localize(None)
d1['Stoptime'] = pd.to_datetime(d1['endTime']).dt.tz_convert(None)

dropcol = ['id', 'name', 'activityTypeId', 'activityTypeName',
           'activityTypeCode', 'activityMainGroupId', 'activityMainGroupName',
           'superstationNumber', 'localstationNumber', 'activityNumber',
           'startTime', 'endTime', 'startLat', 'startLon', 'endLat', 'endLon',
           'comment']
d1 = d1.drop(dropcol, axis=1)
d1.columns

# Merge dataframes
df = pd.concat([fr_ml, fr_au, d1], axis=0).drop_duplicates().reset_index(drop=True)

#df = df.astype({"Starttime": datetime64, "Stoptime": datetime64})
#df['Starttime'] = pd.to_datetime(df['Starttime'])

# Plot overview of experiment
d0 = pd.read_csv('experimentoverview.csv', sep=';')
d0['Starttime'] = pd.to_datetime(d0['Starttime']).dt.strftime('%Y/%m/%d %H:%M')
d0['Stoptime'] = pd.to_datetime(d0['Stoptime']).dt.strftime('%Y/%m/%d %H:%M')
print(tabulate(d0, headers = 'keys', tablefmt = 'plain'))

# Sanity checks

df.groupby(['Experiment', 'Speedbin', 'Platform', 'Location'])[
    'Starttime'].plot(legend='true', style=".")
plt.show()

df['difftime']=df['Stoptime']-df['Starttime']
df.groupby(['Experiment', 'Speedbin', 'Platform', 'Location'])[
    'difftime'].plot(legend='true', style=".")
plt.show()
