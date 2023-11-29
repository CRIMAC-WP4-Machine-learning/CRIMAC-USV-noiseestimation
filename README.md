# CRIMAC-USV-noiseestimation

## time sync issues
There is a problem with the time stamps. Frigg ran on local time and GOS on UTC, but the data seems to be ok. Probably something with python time zone handling that needs attention.
Frigg.Malangen: 17.11.2023 16:52 - 23:26  Metadata: 15:45-22:15
Frigg.Austerhola: 18.11.2023 10:53 - 17:28 Metadata: 09:51- 18:30
Frigg.Austerhola.Drifting: 18.11.2023 20:06 - 20:17 Metadata: 19:06 - ...
GOS.Austerhola: 18.11.2023 17:44 - 19:43 Metadata: 16:44 - 18:40
GOS.Lyngsfjorden: 19.11.2023 10:38 - 13:15 Metadata: 10:02 - 12:07
Frigg.Lyngsfjorden 19.11.2023 10:34 - 13:23 Metadata: 10:02 - 12:07
Frigg.Lyngsfjorden.RMP/noise 19.11.2023 14:30 - 15:13:45 Metadata: 13:30 - 19:19 Missing data!!!
GOS.Austerhola 21.11.2023 20:59 - 22:59:30 Metadata: 20:03 - 21:48
GOS.Malangen 21.11.2023 00:37 - 02:46:30 Metadata: 23:30-01:35

Missing data: 19.11.2023 15:13-20:20


## GOS Navigational data
Run the readnavigation.py to process the GOS navigation data. This is handled through Rabeas scripts.

## GOS and Frigg time intervals per treatment
Run readmetadata.py to prepare time intervals and treatments to a pandas dataframe. Writes the result to a pickle file readmetadata.pk

## REad the noise files from LSSS
Run analyzenoise.py. This generates a Pandas data frame for the noise estimates as a function of time. Writes the results to a pickle file analyzenoise.pk

## Merge files
Run mergedfs.py to merge the noise data and the metadata and save to parquet.

## Plot in R
Run analyze.r to plot the figures in R (ggplot).

# Variables
|Variable|Values|Description|
|-|-|-|
|Frequency | 18, 38, 120, 200, 333 | Echosounder channel |
|Mode|CW,FM| Frequency modulated or contious wave |
|Experiment|Dataquality, Towing, RPMtest, Noisetest| The different experiments
|Location |Malangen, Austerhola, Lyngsfjorden| The location of the experimen |
|Platform	| Frigg, GOSars | The platform | 
|Coverage|1,2,3| Coverage of the same octagon (1..3) or transect (1) |
|Speedbin| 0,3,5,7,9| Speeds, (3,5,7,9) for the Dataquality and Towing, and 0 for RPM test and Noisetest |
|Leg|1,..., 8| 1..8 for octagon, 1..2 for transect |
|RPM|Off, #RPM| The engine RPM | 
|Speed| #speed| the measured speed from sensors |
|Starttime| time| Time for start of treatment |
|Stoptime| time | Time for end of treatment |
