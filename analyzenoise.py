import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np

dr = '/mnt/c/DATA/cruisedata/S2023301002_PFRIGG_10318/ACOUSTIC/LSSS/KORONA/'
noisedata = [fil for fil in os.listdir(dr) if fil.split('.')[1]=='json']
DF = pd.DataFrame()

for i in range(len(noisedata)):
    print(i)
    with open(dr+noisedata[i], 'r') as my_file:
        data = json.load(my_file)
        time = [datetime.datetime.fromtimestamp(_t) for _t in data["time"]]
        frames = [pd.DataFrame(index=time, data={'noiseAverage': data["noiseAverage"]}),
                  pd.DataFrame(index=time, data={'noiseUpperLimit': data["noiseUpperLimit"]})]
        df = pd.concat(frames, axis=1)
        print(noisedata[i].split('_'))
        df['Platform'] = noisedata[i].split('_')[0]
        df['Location'] = noisedata[i].split('_')[1]
        df['Frequency'] = noisedata[i].split('_')[2].split('Echogram')[0][:-2]
        df['Mode'] = noisedata[i].split('_')[2].split('Echogram')[0][-2:]
        # Add the timing information
        
    DF = pd.concat([DF, df], axis=0)

#DF[(DF['Location'] == 'oktagon1'),'Location'] =  'Malangen'
#DF[DF['Location'] == 'oktagon2','Location'] =  'Austerhola'

DF['noiseAverage_linear'] = 10**(DF['noiseAverage']/10)
DF['noiseUpperLimit_linear'] = 10**(DF['noiseUpperLimit']/10)

# Read timeings for each transect
# DF['leg'] = 
# DF['noiseAverage_linear']


DF[DF['mode'] == 'CW'].groupby(['frequency', 'platform'])['noiseAverage'].plot(legend=True)
plt.show()

DFm = DF[(DF['mode'] == 'CW') & (DF['frequency'] == '38')].groupby([
    'platform', 'oktagon', 'frequency'])[
        'noiseAverage_linear'].mean().transform(lambda x: 10*np.log10(x))

DFm.plot()
plt.show()

'''
# Read FM noise specter
import xml
import xmltodict

FM = pd.read_xml('NoiseSpecter.xml')

with open('NoiseSpecter.xml','r') as NoiseSpecter:
    #read xml content from the file
    xml_content = NoiseSpecter.read()
    print("XML content is:")
    print(xml_content)

#change xml format to ordered dict
#ordered_dict = xmltodict.parse(xml_content)

#val = ordered_dict['NoiseSpecter']['channel'][1]['entry']['@value']

# <channel channelIndex="2">
'''
