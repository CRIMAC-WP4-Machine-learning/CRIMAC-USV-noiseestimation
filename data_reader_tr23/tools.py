import math
import numpy as np
def radians_to_degrees(radians):
    degrees = radians * 180 / math.pi
    return degrees

def wrap_degrees(degree, center=180):
    if degree < 180:
        return degree
    else:
        return -(degree%180)

def subset_array_by_time(dataset, start_time_str, end_time_str):
    """
    Subset a NumPy array of datetime64 values based on a specified time range.

    Parameters:
    - time_array: numpy.ndarray, array of datetime64 values.
    - start_time_str: str, start time in the format 'YYYY-MM-DD HH:mm:ss'.
    - end_time_str: str, end time in the format 'YYYY-MM-DD HH:mm:ss'.

    Returns:
    - subset_array: numpy.ndarray, subset of time_array within the specified time range.
    """
    # Convert start and end time strings to numpy datetime64
    start_time = np.datetime64(start_time_str)
    end_time = np.datetime64(end_time_str)
    time_array = dataset["time"]
    # Create a boolean mask for the time range
    mask = (time_array >= start_time) & (time_array <= end_time)

    # Apply the mask to obtain the subset array
    subset_dataset = dataset.sel(time=mask)

    return subset_dataset