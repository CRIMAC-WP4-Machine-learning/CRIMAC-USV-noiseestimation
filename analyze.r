library(arrow)
library(ggplot2)

### Read data
data = read_parquet("data.pk")
data['Seastate'] = data['Location']
data['Seastate'][data['Location'] == 'Malangen'] = 'BF2-3'
data['Seastate'][data['Location'] == 'Lyngsfjorden'] = 'BF2'
data['Seastate'][data['Location'] == 'Austerhola'] = 'BF4'
colnames(data)

### Select CW and 38kHz and plot the Dataquality experiment
data_sub1 <- data[(data['Mode']=='CW' & data['Frequency']=='38' &
                   data['Experiment'] == 'Dataquality'),]
data_sub1 <- data_sub1[!is.na(data_sub1['Platform']),]
summary(data_sub1)
ggplot(data_sub1, aes(x=Platform, y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Seastate)
ggsave('SeastatePlatformDataquality.png')

### Lyngsfjorden detailed experiments
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

