library(arrow)
library(ggplot2)

### Read data
data = read_parquet("data.pk")
data['Seastate'] = data['Location']
data['Seastate'][data['Location'] == 'Malangen'] = 'BF2-3'
data['Seastate'][data['Location'] == 'Lyngsfjorden'] = 'BF2'
data['Seastate'][data['Location'] == 'Austerhola'] = 'BF4'
colnames(data)

data_bot = read_parquet('data_botsv.pk')
data_bot['Seastate'] = data_bot['Location']
data_bot['Seastate'][data_bot['Location'] == 'Malangen'] = 'BF2-3'
data_bot['Seastate'][data_bot['Location'] == 'Lyngsfjorden'] = 'BF2'
data_bot['Seastate'][data_bot['Location'] == 'Austerhola'] = 'BF4'
colnames(data_bot)

data_tr = read_parquet('data_tr.pk')
data_tr['Seastate'] = data_tr['Location']
data_tr['Seastate'][data_tr['Location'] == 'Malangen'] = 'BF2-3'
data_tr['Seastate'][data_tr['Location'] == 'Lyngsfjorden'] = 'BF2'
data_tr['Seastate'][data_tr['Location'] == 'Austerhola'] = 'BF4'
colnames(data_tr)

### Select CW and 38kHz and plot the Dataquality experiment
data_sub1 <- data[(data['Mode']=='CW' & data['Frequency']=='38' &
                   data['Experiment'] == 'Dataquality'),]
data_sub1 <- data_sub1[!is.na(data_sub1['Platform']),]
summary(data_sub1)
ggplot(data_sub1, aes(x=Platform, y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Seastate)
ggsave('SeastatePlatformDataquality.png')

### Is the direction to wind important?
data_sub1 <- data_sub1[!is.na(data_sub1['Location']=='Austerhola'),]
summary(data_sub1)
ggplot(data_sub1, aes(x=Platform, y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Seastate)
ggsave('SeastatePlatformDataquality.png')


### Is there a pattern in frequency?


### Lyngsfjorden detailed experiments (varying RPM, towing and propeller disengaged)
LCW38 <- data[(data['Mode']=='CW' & data['Frequency']=='38' & data['Location']=='Lyngsfjorden'),]
LCW38 <- LCW38[!is.na(LCW38['RPM']),]
summary(LCW38)
unique(LCW38['RPM'])

### The effect of variable RPM and motor off (towing)
LCW38_f <- LCW38[LCW38['Platform'] == 'Frigg' & !LCW38['Experiment'] == 'RPMtest',]
ggplot(LCW38_f, aes(x=factor(RPM), y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Platform)
ggsave('RPMvsSpeed.png')

### RPM test while propeller is disenganged
LCW38_rpm <- LCW38[LCW38['Platform'] == 'Frigg' & LCW38['Experiment'] == 'RPMtest',]
summary(LCW38_rpm)

###
### analyze the bottom integrals
###

data_bot1 <- data_bot[(data_bot['Experiment'] == 'Dataquality'),]
data_bot2 <- data_bot1[!is.na(data_bot1['Platform']),]
summary(data_bot2)

data_bot3 <- data_bot2[(data_bot2['Location'] == 'Austerhola')|(data_bot2['Location'] == 'Malangen'),]

#data_bot1 <- data_bot1[(data_bot1['Location'] == 'Austerhola'),]
ggplot(data_bot3, aes(x=factor(Speedbin), y=10*log10(sa), fill=factor(Platform))) + 
    geom_boxplot() + facet_wrap(~ Seastate)
ggsave('IntegratedBottom.png')

###
### Analyse roll data
###

data_tr <- data_tr[!is.na(data_tr['Seastate']),]
data_tr <- data_tr[!is.na(data_tr['Speedbin']),]
ggplot(data_tr, aes(x=factor(Speedbin), y=roll, fill=factor(Leg))) + 
    geom_boxplot() + facet_wrap(~ Seastate)
ggsave('Rolldata.png')
