import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import data
df_intervals = pd.read_pickle('readmetadata.pk')
df_data = pd.read_pickle('analyzenoise.pk')

# We need to split the data before merging since we merge by timestamps
df_intervals_GOSars = df_intervals[df_intervals['Platform'] == 'GOSars']
df_intervals_Frigg = df_intervals[df_intervals['Platform'] == 'Frigg']

df_data_GOSars = df_data[df_data['Platform'] == 'GOSars']
df_data_Frigg = df_data[df_data['Platform'] == 'Frigg']

mcol = ['noiseAverage', 'noiseUpperLimit', 'Platform_y', 'Location_y',
        'Frequency', 'Mode', 'noiseAverage_linear', 'noiseUpperLimit_linear',
        'Coverage', 'Leg', 'Speed', 'true_wind_dir',
        'Experiment', 'Speedbin', 'Headingtowind', 'Location_y', 'Platform_y',
        'RPM'],
mcol = ['RPM', 'Leg','Speedbin']
# Merge DataFrames on the 'timestamp' column
# This is similar to a left-join except that we match on nearest key rather
# than equal keys. Both DataFrames must be sorted by the key.
merged_df_GOSars = pd.merge_asof(df_data_GOSars, df_intervals_GOSars,
                                 left_on='Time', right_on='Starttime',
                                 direction='backward')
merged_df_GOSars.loc[merged_df_GOSars['Time'] > merged_df_GOSars[
    'Stoptime'], mcol] = np.NaN

merged_df_Frigg = pd.merge_asof(df_data_Frigg, df_intervals_Frigg,
                                left_on='Time', right_on='Starttime',
                                direction='backward')
merged_df_Frigg.loc[merged_df_Frigg['Time'] > merged_df_Frigg[
    'Stoptime'], mcol] = np.NaN

df = pd.concat([merged_df_Frigg, merged_df_GOSars], axis=0)


# Calculate the average within each time interval
result = df.groupby(['Experiment', 'Location_x',])['noiseAverage'].mean()
df.columns
df = df.set_index('Time')


df[(df['Mode'] == 'CW') & (df['Frequency'] == '38')].groupby([
    'Platform_y', 'Location_y'])['noiseAverage'].plot(legend=True)
plt.show()
df.loc[df['Location_y'] != df['Location_x'], 'Location_y']

#.plot(legend=True)

#plt.plot()
#mean().reset_index()

# Plot the dataQuality figures
#Index(['Starttime', 'Coverage', 'Leg', 'Speed', 'true_wind_dir', 'Stoptime',
#       'Experiment', 'Speedbin', 'Headingtowind', 'Location', 'Platform',
#       'RPM'],

df.columns


'''
# Test data
data = {'timestamp': pd.to_datetime([
    '2023-01-01 11:00:00', '2023-01-01 11:15:00',
    '2023-01-01 11:30:00', '2023-01-01 11:45:00',
    '2023-01-01 12:00:00', '2023-01-01 12:15:00',
    '2023-01-01 12:30:00', '2023-01-01 12:45:00',
    '2023-01-01 13:00:00', '2023-01-01 13:15:00',
    '2023-01-01 13:30:00', '2023-01-01 13:45:00']),
        'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]}
df = pd.DataFrame(data)

# Sample DataFrame with time intervals
intervals = {'start_time': pd.to_datetime(['2023-01-01 12:01:00',
                                           '2023-01-01 12:36:00',
                                           '2023-01-01 13:31:00']),
             'end_time': pd.to_datetime(['2023-01-01 12:34:00',
                                         '2023-01-01 13:01:00',
                                         '2023-01-01 13:46:00']),
             'geir': ['A','B','C']}
df_i = pd.DataFrame(intervals)

# Merge DataFrames on the 'timestamp' column
merged_df = pd.merge_asof(df, df_i, left_on='timestamp', right_on='start_time', direction='backward')
merged_df.loc[merged_df['timestamp'] > merged_df['end_time'], 'geir'] = np.NaN

'''



# Calculate the average within each time interval
#result = filtered_df.groupby(['start_time', 'end_time'])['value'].mean().reset_index()



