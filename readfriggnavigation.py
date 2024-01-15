import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fil = ['/mnt/c/DATA/USVRVavoidance/20231117_navigation.log.1',
       '/mnt/c/DATA/USVRVavoidance/20231118_navigation.log.1']

df_l = [pd.read_csv(_fil, sep=',') for _fil in fil]
df = pd.concat(df_l)
df = df.rename(columns={'%1:timestamp': 'Time', '2:latitude': 'latitude',
                        '3:longitude': 'longitude', '4:altitude': 'altitue',
                        '5:sog': 'sog', '6:cog': 'cog', '7:roll': 'roll',
                        '8:pitch': 'pitch', '9:yaw':'yaw', '10:p':'p',
                        '11:q':'q', '12:r':'r', '13:stw':'stw',
                        '14:wbeta':'wbeta', '15:depth': 'depth'})

df['roll'] = df['roll']*180/np.pi
df['pitch'] = df['pitch']*180/np.pi
df['Time'] = pd.to_datetime(df['Time'], unit='s')

df = df.set_index('Time')
df = df.reset_index()

df.to_pickle('readfriggnavigation.pk')

df['roll'].plot()
plt.show()

df['Time'].plot()
plt.show()
