import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate 
from datetime import timedelta


def cleanmetadata(fil):
    # Read tagged data for Frigg during Malangen octagons
    df = pd.read_csv(fil, sep=',')
    df = df.rename(columns={"sog": "Speed", "leg": "Leg",
                            "coverage": "Coverage", "time": "Starttime"})
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

'''
2023-11-17.csv
2023-11-18.csv
2023-11-18gosars.csv
2023-11-18gosars0_manual_anotation.csv
2023-11-21gosars1_manual_annoation.csv
2023-11-21gosars3_manual_annotation.csv
'''

# Read tagged data for Frigg during Malangen octagons
fr_ml = cleanmetadata('./data_reader_tr23/output/2023-11-17.csv')
fr_ml['Location'] = 'Malangen'
fr_ml['Platform'] = 'Frigg'

# Read tagged data for Frigg during Austehola octagons
fr_au = cleanmetadata('./data_reader_tr23/output/2023-11-18.csv')
fr_au['Location'] = 'Austerhola'
fr_au['Platform'] = 'Frigg'

# Add drifting part for Frigg
fr_au0 = pd.DataFrame({'Starttime': '2023-11-18T19:06:32.588Z', 'Coverage': 1,
                       'Leg': 1, 'Speed': 0,
                       'true_wind_dir': 'NaN',
                       'Stoptime': '2023-11-18T19:17:01.468Z',
                       'Experiment': 'Dataquality', 'Speedbin': '0',
                       'Headingtowind': 'NaN', 'Location': 'Austerhola',
                       'Platform': 'Frigg'}, index=[0])
fr_au0['Starttime'] = pd.to_datetime(fr_au0['Starttime']).dt.tz_localize(None)
fr_au0['Stoptime'] = pd.to_datetime(fr_au0['Stoptime']).dt.tz_localize(None)

# Read tagged data for GOS during Austerola Octagons
gos_au0 = cleanmetadata('./data_reader_tr23/output/2023-11-18gosars0_manual_anotation.csv')
gos_au0['Location'] = 'Austerhola'
gos_au0['Platform'] = 'GOSars'
gos_au0['Coverage'] = 0

# Read tagged data for GOS during Austehola Octagons
gos_au1 = cleanmetadata('./data_reader_tr23/output/2023-11-21gosars1_manual_annoation.csv')
gos_au1['Location'] = 'Austerhola'
gos_au1['Platform'] = 'GOSars'
gos_au1['Coverage'] = 1

# Read tagged data for GOS during Malangen Octagons
gos_ml = cleanmetadata('./data_reader_tr23/output/2023-11-21gosars3_manual_annotation.csv')
gos_ml['Location'] = 'Malangen'
gos_ml['Platform'] = 'GOSars'

# Read metadata for all experiments except octagons
d1 = pd.read_csv('experimenttiming.csv', sep=';')
d1['Starttime'] = pd.to_datetime(d1['startTime']).dt.tz_localize(None)
d1['Stoptime'] = pd.to_datetime(d1['endTime']).dt.tz_convert(None)

dropcol = ['id', 'name', 'activityTypeId', 'activityTypeName',
           'activityTypeCode', 'activityMainGroupId', 'activityMainGroupName',
           'superstationNumber', 'localstationNumber', 'activityNumber',
           'startTime', 'endTime', 'startLat', 'startLon', 'endLat', 'endLon',
           'comment']
frigg_ly = d1.drop(dropcol, axis=1)
frigg_ly['Coverage'] = frigg_ly['Coverage'] - 1

# Get the metadata for GOS for the Lyngsfjorden experiment (copy the Frigg data)
gos_ly = frigg_ly[frigg_ly['Experiment'] == 'Dataquality']
gos_ly['Platform'] = 'GOSars'
gos_ly['RPM'] = 'Fixed'

# Merge dataframes
df = pd.concat([fr_ml, fr_au, gos_au0, fr_au0, frigg_ly, gos_ly, gos_au1, gos_ml], axis=0).drop_duplicates().reset_index(drop=True)
fr_au.columns

# Fix time errors:

df['Starttime'] = df['Starttime'] + timedelta(hours=1)
df['Stoptime'] = df['Stoptime'] + timedelta(hours=1)

print(tabulate(df, headers = 'keys', tablefmt = 'plain'))

# Change data types
df = df.convert_dtypes()
df['Speedbin'] = pd.to_numeric(df['Speedbin'])
df['Headingtowind'] = pd.to_numeric(df['Headingtowind'], errors='coerce')
df['true_wind_dir'] = pd.to_numeric(df['true_wind_dir'], errors='coerce')

df = df.sort_values(by=['Starttime'])
df.to_pickle('readmetadata.pk')

# Plot overview of experiment
d0 = pd.read_csv('experimentoverview.csv', sep=';')
d0['Starttime'] = pd.to_datetime(d0['Starttime']).dt.strftime('%Y/%m/%d %H:%M')
d0['Stoptime'] = pd.to_datetime(d0['Stoptime']).dt.strftime('%Y/%m/%d %H:%M')
print(tabulate(d0, headers = 'keys', tablefmt = 'plain'))
#print(tabulate(d0, headers = 'keys'))

# Sanity checks
fig, ax = plt.subplots()
df.groupby(['Location', 'Platform', 'Experiment', 'Speedbin'])[
    'Starttime'].plot(legend='true', style=".")
ax.legend(title='(Location, Platform, Experiment, Speedbin)')
plt.show()
df.columns
df['difftime'] = df['Stoptime']-df['Starttime']

fig, ax = plt.subplots()
df.groupby(['Location', 'Platform', 'Experiment', 'Speedbin'])[
    'difftime'].plot(legend='true', style=".", ax=ax)
ax.legend(title='(Location, Platform, Experiment, Speedbin)')
plt.show()

fig, ax = plt.subplots()
df.groupby(['Location', 'Platform', 'Experiment', 'Speedbin'])[
    'Starttime'].plot(legend='true', style=".", ax=ax)
ax.legend(title='(Location, Platform, Experiment, Speedbin)')
plt.show()
df['Experiment'].unique()
