from datetime import datetime
from time import sleep
from tqdm import tqdm

# Code to record time and treatment for the noise testing

dt = 10 # seconds per treatment should be 60 sec
speed = [str(_speed)+' knots' for _speed in range(2, 10, 2)] 
headingtowind = [str(_headingtowind)+' degrees' for
                 _headingtowind in range(0, 181, 45)]
eksettings = ['CW passive', 'CW active', 'FM passive', 'FM active']
now = datetime.now().isoformat()
logfile = 'Logfile'+now+'.txt'

with open(logfile, 'w') as my_file:
    print(my_file.write('starttime;stoptime;headingtowind;eksettings;speed'))

for _headingtowind in headingtowind:
    for _eksettings in eksettings:
        for _speed in speed:
            print('EK settings:'+_eksettings+'; Headingtowind:'+str(
                _headingtowind)+'; Speed:'+str(_speed))
            print('Press enter to start logging '+str(dt)+' sec interval')
            input()
            starttime = datetime.now().isoformat()
            for i in tqdm(range(dt)):
                sleep(1)
            stoptime = datetime.now().isoformat()
            with open(logfile, 'a') as my_file:
                my_file.write('\n'+starttime+';'+stoptime+';'+_headingtowind+';'+_eksettings+';'+_speed)
            print(' ')
