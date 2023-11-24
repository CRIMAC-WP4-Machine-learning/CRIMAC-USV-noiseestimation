import os
import annotation_octagon as octa
import matplotlib.pyplot as plt
import filter
import annotation_navigation as obs
import annotation_gosars as sars
import xarray as xr
import numpy as np
import pandas as pd
###FILES###
NAV_PATH=r"./navigationdata/"
SARS_PATH=["./gosarsdata/pos18-11-2023.csv", "./gosarsdata/pos21-11-2023.csv"]
SAVE_PATH="./output/"
PLATFORM="gosars"
#OBS_PATH=r"C:\Users\rabear\OneDrive - NTNU\Campaigns\FriggTromsø2023\day5"
MODE=0 #0=single file read, 1 = multiple
EXP=1
RANGE = [("2023-11-18T16:35:29",'2023-11-18T18:48:44'), ("2023-11-21T20:00:05",'2023-11-21T21:50:00')]

###FILTER###
WINDOW=39 #Filterkernel
THRESH=0.1
DERIV=5
WRAP=False
EXPERIMENT_LENGTH=60*2 #[s]

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
    annotation_obs = obs.AnnotationJSON(NAV_PATH)
    annotation_obs.clean(EXP)
    #annotation_obs.cut_to_timeperiod(RANGE[EXP])
    if EXP != 3:
        annotation_sars = sars.AnnotationGOSars(SARS_PATH[EXP])
        annotation_sars.cut_to_timeperiod(RANGE[EXP])

    #Get leg timestamps based on heading
    time = annotation_obs.data[EXP]["time"].values
    cog =  annotation_obs.data[EXP]["heading"]

    plt.plot(time, cog)
    plt.show()

    time_s, values_s = filter.filter_periods(cog, time, WINDOW, EXPERIMENT_LENGTH, THRESH, DERIV, WRAP)

    #Compute average values per leg
    annotation_obs.filter_heading(WINDOW, EXP, WRAP)
    avg_cog=annotation_obs.average_between_periods(time_s,"heading", EXP)
    avg_sog=annotation_obs.average_between_periods(time_s,"vesselSpeed", EXP)

    if EXP==3:
        avg_true_wind = np.ones(len(avg_sog))*160
    else:
        avg_true_wind = annotation_sars.average_between_periods(time_s,"Wind dir")

    #Collect averaged values per leg in dataframe
    oct=octa.AnnotationOctagon(time_s, np.rad2deg(avg_cog), avg_sog, avg_true_wind)
    if EXP !=3:
        oct.to_csv(SAVE_PATH+RANGE[EXP][EXP][:10]+PLATFORM+str(EXP)+".csv")
    else:
        oct.to_csv(SAVE_PATH + RANGE[1][1][:10] + PLATFORM + str(EXP) + ".csv")
    #Plot
    # DF.groupby(['file'])['vesselSpeed'].plot(legend='true')
    plt.plot(time, annotation_obs.data[EXP]["heading"])
    plt.plot(time_s, values_s, marker='o')
    plt.plot(time_s[:-1], avg_cog, marker='x')
    plt.show()


if __name__ == '__main__':
    run()
