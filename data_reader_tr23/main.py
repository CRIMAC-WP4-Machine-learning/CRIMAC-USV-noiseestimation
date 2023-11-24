import os
import annotation_octagon as octa
import matplotlib.pyplot as plt
import filter
import annotation_obs as obs

###FILES###
AIRMAR_PATH=["./friggdata/20231117_weather_report.log.1", "./friggdata/20231118_weather_report.log.1"]
OBS_PATH=["./friggdata/20231117_navigation.log.1","./friggdata/20231118_navigation.log.1"]
#OBS_PATH=r"C:\Users\rabear\OneDrive - NTNU\Campaigns\FriggTromsø2023\day5"
EXP=1 #ADJUST THIS TO GENERATE OUTPUTS PER EXPERIMENT
RANGE = [("2023-11-17T15:45:29",'2023-11-17T22:30:44'), ("2023-11-18T09:51:05",'2023-11-18T16:27:00')]

###FILTER###
WINDOW=1501 #Filterkernel
EXPERIMENT_LENGTH=60*2 #[s]
THRESH=25
DERIV=10
WRAP=True

###PLOTTING###
SAVE=True


def get_filenames_in_folder(folder_path):
    """
    Get a list of filenames in the specified folder.

    Parameters:
    - folder_path: str, the path to the folder.

    Returns:
    - filenames: list, a list of filenames in the folder.
    """
    try:
        filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return filenames
    except OSError as e:
        print(f"Error: {e}")
        return []

def run():
    #Read files
    annotation_obs = obs.AnnotationOBS(OBS_PATH[EXP])
    plt.plot(annotation_obs.data["time"],annotation_obs.data["6:cog"] )
    plt.show()
    annotation_obs.cut_to_timeperiod(RANGE[EXP])
    annotation_weather = obs.AnnotationOBS(AIRMAR_PATH[EXP])
    annotation_weather.cut_to_timeperiod(RANGE[EXP])

    #Get leg timestamps based on heading
    time = annotation_obs.data["time"]
    cog = annotation_obs.data["6:cog"]
    time_s, values_s = filter.filter_periods(cog, time, WINDOW, EXPERIMENT_LENGTH, THRESH, DERIV, WRAP)

    #Compute average values per leg
    annotation_obs.filter_heading(WINDOW)
    avg_cog=annotation_obs.average_between_periods(time_s,"6:cog")
    avg_sog=annotation_obs.average_between_periods(time_s,"5:sog")
    avg_true_wind = annotation_weather.average_between_periods(time_s,"5:wind_dir_true_filtered")

    #Collect averaged values per leg in dataframe
    oct=octa.AnnotationOctagon(time_s, avg_cog, avg_sog, avg_true_wind)
    oct.to_csv(RANGE[EXP][0][:10]+".csv")

    #Plot
    plt.plot(time, annotation_obs.data["6:cog"])
    plt.plot(annotation_weather.data["time"], annotation_weather.data["5:wind_dir_true_filtered"])
    plt.plot(time_s, values_s, marker='o')
    plt.plot(time_s[:-1], avg_cog, marker='x')
    plt.show()


if __name__ == '__main__':
    run()
