library(arrow)
library(ggplot2)

data = read_parquet("data.pk")
#data = read_parquet("mediandata.pk")

colnames(data)
# Select CW and 38kHz

data_sub = data[data['Mode']=='CW' & data['Frequency'] == '38' & !is.na(data['Platform']) & data['Experiment'] == 'Dataquality',]
# grouped boxplot
ggplot(data_sub, aes(x=factor(Platform), y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Location)


data_sub = data[data['Mode']=='CW' & !is.na(data['Platform']) & data['Experiment'] == 'Dataquality',]

# grouped boxplot
ggplot(data_sub, aes(x=factor(Platform), y=noiseAverage, fill=factor(Speedbin))) + 
    geom_boxplot() + facet_wrap(~ Location + Frequency)

