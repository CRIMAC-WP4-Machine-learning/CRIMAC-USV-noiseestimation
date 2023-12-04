import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import data
df_intervals = pd.read_pickle('readmetadata.pk')
df_data = pd.read_pickle('analyzenoise.pk')
df_bot = pd.read_pickle('svdata.pk')
df_bot['Location'].unique()

# Testing
'''
T0 = df_intervals[df_intervals['Experiment'] == 'Towing']['Starttime'].values
T1 = df_intervals[df_intervals['Experiment'] == 'Towing']['Stoptime'].values
#ind = df_data[(df_data['Time']>T0[0]) & (df_data['Time']<T1[0])]['Time']

# Drift test: 18 20:06 20:15
# Balangen dataq : 19.11 10:00 10:35  12:15-12:15


df = df_data
df = df.set_index('Time')
df[(df['Mode'] == 'CW') & (df['Frequency'] == '38')].groupby([
    'Platform', 'Location'])[
        'noiseAverage'].plot(legend=True)
plt.show()

df_data.columns
'''

# We need to split the data before merging since we merge by timestamps
df_intervals_GOSars = df_intervals[df_intervals['Platform'] == 'GOSars']
df_intervals_Frigg = df_intervals[df_intervals['Platform'] == 'Frigg']

# Delete column names that will be duplicates
df_intervals_GOSars = df_intervals_GOSars.drop(columns = [
    'Platform', 'Location'])
df_intervals_Frigg = df_intervals_Frigg.drop(columns = [
    'Platform', 'Location'])

df_data_GOSars = df_data[df_data['Platform'] == 'GOSars']
df_data_Frigg = df_data[df_data['Platform'] == 'Frigg']
df_bot_GOSars = df_bot[df_bot['Platform'] == 'GOSars']
df_bot_Frigg = df_bot[df_bot['Platform'] == 'Frigg']

# Merge DataFrames on the 'timestamp' column
# This is similar to a left-join except that we match on nearest key rather
# than equal keys. Both DataFrames must be sorted by the key.
merged_df_GOSars = pd.merge_asof(df_data_GOSars, df_intervals_GOSars,
                                 left_on='Time', right_on='Starttime',
                                 direction='backward')
merged_df_Frigg = pd.merge_asof(df_data_Frigg, df_intervals_Frigg,
                                left_on='Time', right_on='Starttime',
                                direction='backward')

merged_bot_GOSars = pd.merge_asof(df_bot_GOSars, df_intervals_GOSars,
                                  left_on='Time', right_on='Starttime',
                                  direction='backward')
merged_bot_Frigg = pd.merge_asof(df_bot_Frigg, df_intervals_Frigg,
                                 left_on='Time', right_on='Starttime',
                                 direction='backward')

'''
# Test data for sanity checking the algorithm
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

# We also need a list of colmns so that we can delete time after the stoptime
mcol = ['Coverage', 'Leg', 'Experiment', 'Speedbin', 'RPM']
# And then we delete the items when after stoptime
merged_df_GOSars.loc[merged_df_GOSars['Time'] > merged_df_GOSars[
    'Stoptime'], mcol] = np.NaN
merged_df_Frigg.loc[merged_df_Frigg['Time'] > merged_df_Frigg[
    'Stoptime'], mcol] = np.NaN
merged_bot_GOSars.loc[merged_bot_GOSars['Time'] > merged_bot_GOSars[
    'Stoptime'], mcol] = np.NaN
merged_bot_Frigg.loc[merged_bot_Frigg['Time'] > merged_bot_Frigg[
    'Stoptime'], mcol] = np.NaN

# Finally we concatenate Frigg and GOSars data frames
df = pd.concat([merged_df_Frigg, merged_df_GOSars], axis=0)
bot = pd.concat([merged_bot_Frigg, merged_bot_GOSars], axis=0)

# And we'll use Time as indices
df.to_parquet('data.pk')
bot.to_parquet('data_botsv.pk')
df.columns

df = df.set_index('Time')
df[(df['Mode'] == 'CW') & (df['Frequency'] == '38')].groupby([
    'Platform', 'Location', 'Coverage', 'Leg', 'Speedbin'])[
        'noiseAverage'].plot(legend=True)
plt.show()

df[(df['Mode'] == 'CW') & (df['Frequency'] == '38')].groupby([
    'Platform', 'Location'])[
        'noiseAverage'].plot(legend=True)
plt.show()

bot = bot.set_index('Time')
bot[(bot['Mode'] == 'CW') & (bot['Frequency'] == '38')].groupby([
    'Platform', 'Location', 'Coverage', 'Leg', 'Speedbin'])[
        'sa'].plot(legend=True)
plt.show()
