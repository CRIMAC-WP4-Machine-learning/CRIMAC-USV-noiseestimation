import numpy as np
from scipy.signal import medfilt
import tools
from scipy.signal import find_peaks
import scipy.stats as stats
import matplotlib.pyplot as plt


def remove_redundant_indices(time_array, indices_array, time_period):
    """
    Remove redundant indices based on a given time period.

    Parameters:
    - time_array: 1D numpy array, the array of timestamps.
    - indices_array: 1D numpy array, the array of indices.
    - time_period: float, the minimum time separation between indices to be considered non-redundant.

    Returns:
    - filtered_indices: 1D numpy array, the non-redundant indices.
    """
    # Initialize the list to store non-redundant indices
    filtered_indices = [indices_array[0]]

    # Iterate through the indices and keep only non-redundant ones
    for i in range(1, len(indices_array)):
        time_delta=time_array[indices_array[i]] - time_array[filtered_indices[-1]]
       # time_delta = int(time_delta) / 10e9
        time_delta = time_delta /np.timedelta64(1, 's')
        if time_delta >= time_period:
            filtered_indices.append(indices_array[i])

    return np.array(filtered_indices)

def filter_angles(angular_values, window_size):
    filtered_signal = np.zeros_like(angular_values)
    angular_values = [s if s>3 else 360 for s in angular_values]
    for i in range(len(angular_values)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(angular_values), i + window_size // 2 + 1)
        window_data = angular_values[start_idx:end_idx]
        circular_mean = np.degrees(stats.circmean(np.radians(window_data)))
        filtered_signal[i] = circular_mean
    return filtered_signal

def filter_moving_avg(signal, window_size):
    return np.convolve(signal, np.ones(window_size) / window_size, mode='same')

def filter_median(signal, window_size):
    return medfilt(signal, kernel_size=window_size)
def remove_wrap_180(degree_vector):
    result_vector = []
    for index, element in enumerate(degree_vector):
        if len(result_vector)==0:
            result_vector.append(element)
        else:
            if abs(result_vector[index-1]) - abs(element) < 150:
                result_vector.append(element)
            else:
                result_vector.append(result_vector[index-1])
    return result_vector

def remove_wrap_360(degree_vector):
    result_vector = []
    for index, element in enumerate(degree_vector):
        if len(result_vector)==0:
            result_vector.append(element)
        else:
            if abs(result_vector[index-1]) - abs(element) < 320:
                result_vector.append(element)
            else:
                result_vector.append(360)
    return result_vector

def filter_heading(heading_array, window, wrap, mode='median'):
    cog = heading_array

    #cog = [tools.radians_to_degrees(s) for s in cog]
    if wrap:
        cog = np.rad2deg(cog)
        cog = np.unwrap(cog)
    window_size = window
    if mode == 'median':
        cog = filter_median(cog, window_size)
    elif mode == 'avg':
        cog = filter_angles(cog, window_size)
    #cog = [tools.wrap_degrees(c) for c in cog]
    #cog = remove_wrap_360(cog)
    if wrap:
        cog =np.mod(cog, 360)
    return cog

def detect_step(values):
    dary = np.array([*map(float, values)])

    dary -= np.average(dary)

    step = np.hstack((np.ones(len(dary)), -1 * np.ones(len(dary))))

    dary_step = np.convolve(dary, step, mode='valid')

    # get the peak of the convolution, its index

    step_indx = np.argmax(dary_step)

    plt.plot(dary)

    plt.plot(dary_step / 10)

    plt.plot((step_indx, step_indx), (dary_step[step_indx] / 10, 0), 'r')
    return step_indx

def filter_periods(values, time, window, period, thresh, deriv, wrap=True,plot_set=True, exp=-1, platform="none"):
    '''Takes noisy step signal. Returns list of timestamps of the periods
    '''
    #Thou shalt not adjust the magic numbers
    values_orig = values
    values=filter_heading(values, window, wrap)
    significant_changes = np.where(np.abs(np.diff(values,deriv)) > thresh)[0]
    if plot_set:
        plt.plot(time[:-deriv], np.abs(np.diff(values,deriv)))
        plt.plot(time,values)
        plt.plot(np.array(time)[significant_changes], np.array(values)[significant_changes], marker='o')
        plt.show()
    peaks = remove_redundant_indices(time, significant_changes, time_period=period)
    print(peaks)
    #prepend first element
    print(len(peaks))
    #peaks =np.insert(peaks,0,0)
    if exp == 0 and platform == "gosars":
        peaks = np.insert(-3,4000)
    peaks=np.append(peaks, len(time)-1)
    print(len(peaks))
    return np.array(time)[peaks], np.array(values_orig)[peaks]

# def filter_periods(values, time, window, period, plot_set=True):
#     '''Takes noisy step signal. Returns list of timestamps of the periods
#     '''
#     #Thou shalt not adjust the magic numbers
#     values_orig = values
#     values=filter_heading(values, window)
#     significant_changes = np.where(np.abs(np.diff(values,10)) > 20)[0]
#     if plot_set:
#         plt.plot(time[:-10], np.abs(np.diff(values,10)))
#         plt.plot(time,values)
#         plt.plot(np.array(time)[significant_changes], np.array(values)[significant_changes], marker='o')
#         plt.show()
#     peaks = remove_redundant_indices(time, significant_changes, time_period=period)
#     print(peaks)
#     return np.array(time)[peaks], np.array(values_orig)[peaks]