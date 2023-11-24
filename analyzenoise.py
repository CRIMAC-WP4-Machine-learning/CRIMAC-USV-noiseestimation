import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np

# These files are found under /data/cruisedata/
dr = ['/mnt/c/DATA/cruisedata/S2023301002_PFRIGG_10318/',
      '/mnt/c/DATA/cruisedata/S2023001016_PGOSARS_4174/']
drr = 'ACOUSTIC/LSSS/EXPORT/EchogramPlot/'

noisedata = [dr[0]+drr+fil for fil in os.listdir(dr[0]+drr) if fil.split('.')[
    1] == 'json']
noisedata = noisedata + [dr[1]+drr+fil for fil in os.listdir(dr[1]+drr) if fil.split('.')[
    1] == 'json']


DF = pd.DataFrame()
for i in range(len(noisedata)):
    with open(noisedata[i], 'r') as my_file:

        filename = noisedata[i].split('/')[-1].split('_')
        # An extra _ is added for the towing noise

        #print(filename)
        
        # Remove Sv files
        if filename[2].split('Echogram')[0][:-2] != 'Sv':
            data = json.load(my_file)
            time = [datetime.datetime.fromtimestamp(_t) for _t in data["time"]]
            frames = [pd.DataFrame(index=time, data={
                'noiseAverage': data["noiseAverage"]}),
                      pd.DataFrame(index=time, data={
                          'noiseUpperLimit': data["noiseUpperLimit"]})]
            df = pd.concat(frames, axis=1)
            df['Platform'] = filename[0]
            df['Location'] = filename[1]
            # This is a hack to handle stupid file convension in the input files
            # Frigg_Octagon1_noise_70FM_EchogramPlot_T20231117_15522790-20231117_22263754
            # Frigg_Lyngsfjorden_towing_noise_38CW_EchogramPlot_T20231119_13315279-20231119_14134131
            # GOSars_Octagon1_18CW_EchogramPlot_T20231118_16442578-20231118_18424024
            nn = 0
            nnn = 0
            if filename[0] == 'Frigg':
                nn = 1
                if filename[2] == 'towing':
                    nnn = 1
                    #print(filename)
            df['Frequency'] = filename[2+nn+nnn].split('Echogram')[0][:-2]
            df['Mode'] = filename[2+nn+nnn].split('Echogram')[0][-2:]
            # Concatenate
            DF = pd.concat([DF, df], axis=0)

'''
DF['noiseAverage'] = DF['noiseAverage']
DF['noiseUpperLimit'] = pd.as_float(DF['noiseUpperLimit'])
# Change to correct structure
DF[(DF['Location'] == 'oktagon1'), 'Location'] =  'Malangen'
DF[DF['Location'] == 'oktagon2', 'Location'] =  'Austerhola'
DF[DF['Location'] == 'oktagon3', 'Location'] =  'Austerhola'
DF[DF['Location'] == 'Drifting', 'Location'] =  'Austerhola'

# Drifting -> Austerhola
DF['noiseAverage_linear'] = 10**(DF['noiseAverage']/10)
DF['noiseUpperLimit_linear'] = 10**(DF['noiseUpperLimit']/10)

# Read timeings for each transect
# DF['leg'] = 
# DF['noiseAverage_linear']


DF[DF['Mode'] == 'CW'].groupby(['Frequency', 'Platform'])['noiseAverage'].plot(legend=True)
plt.show()

DFm = DF[(DF['mode'] == 'CW') & (DF['frequency'] == '38')].groupby([
    'platform', 'oktagon', 'frequency'])[
        'noiseAverage_linear'].mean().transform(lambda x: 10*np.log10(x))

DFm.plot()
plt.show()
'''

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
