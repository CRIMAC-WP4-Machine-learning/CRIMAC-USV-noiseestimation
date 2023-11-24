import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np
from functools import reduce
import filter
import xarray as xr
import tools as tls

class AnnotationJSON:
    def __init__(self, dir):
        self.data = self.read(dir)
    def read(self, dr):

        navfiles = [fil for fil in os.listdir(dr) if fil.split('.')[1] == 'json']
        data = []

        for i in range(len(navfiles)):
            with open(dr+navfiles[i], 'r') as my_file:
                data.append(json.load(my_file))

        dat = []
        i=0
        # Loop over files
        for _data in data:
            # Loop over datasets within the file
            dsets = [_d for _d in _data['datasets']]
            dat2 = []
            for _vars in dsets:
                #print(_vars['coordinateVariable'][0])
                td = _vars[_vars['coordinateVariable'][0]]
                tdi = [int(_td) for _td in td]
                d = _vars[_vars['dataVariable']]
                #print(_vars['dataVariable'])
                df0 = pd.DataFrame(data={'time': tdi, _vars['dataVariable']: d})
                dat2.append(df0)
            df = reduce(lambda left,right: pd.merge(left,right,on=['time'], how='outer'), dat2)
            df['time'] = pd.to_datetime(df['time'],unit='s')
            df['file'] = navfiles[i]
            i+=1
            dat.append(df)
        return dat

    def clean(self, exp):
        df = self.data[exp]
        self.data[exp]['time'] = [pd.to_datetime(t, format='%Y-%m-%dT%h:%m:%s') for t in self.data[exp]['time']]
        self.data[exp]['heading'] = np.deg2rad(self.data[exp]['heading'].values.astype(float))
        df = df.dropna(subset='time')
        df = df.dropna(subset='heading')
        df = xr.Dataset.from_dataframe(df.set_index('time'))
        self.data[exp] = df

    def _convert_timestamp(self, timestamp):
        unix_epoch_seconds = int(timestamp)

        # Create a Python datetime object
        python_datetime = datetime.utcfromtimestamp(unix_epoch_seconds)

        # Convert to NumPy datetime64
        return np.datetime64(python_datetime)

    def cut_to_timeperiod(self, timerange):
        ''''Takes xarray dataset and a timerange (start,stop) and returns the cut down dataset'''
        start, stop = timerange
        self.data = tls.subset_array_by_time(self.data, start, stop)

    def average_between_periods(self, periods, variablename, exp):
        """
        Calculate the average 'cog' value between each pair of timestamps in the given periods.

        Parameters:
        - dataframe: pandas.DataFrame, input DataFrame with 'time' as a coordinate and 'cog' as a variable.
        - periods: numpy.ndarray or list, array of timestamps representing periods.

        Returns:
        - average_cog_values: numpy.ndarray, array of average 'cog' values between each pair of timestamps in periods.
        """
        average_cog_values = []

        for i in range(len(periods) - 1):
            start_time = periods[i]
            end_time = periods[i + 1]

            mask = (self.data[exp]['time'] >= start_time) & (self.data[exp]['time'] <= end_time)

            # Apply the mask to obtain the subset array
            subset_dataset = self.data[exp].sel(time=mask)
            # Filter dataframe for the specified period

            # Calculate the average 'cog' value for the period
            average_cog = subset_dataset[variablename].mean()

            average_cog_values.append(average_cog.values)

        return average_cog_values

    def filter_heading(self, window, exp, wrap):
        fitlered_cog = filter.filter_heading(self.data[exp]["heading"].astype(float), window, wrap)
        self.data[exp]["heading"] = xr.DataArray(data=fitlered_cog,
                                          dims=('time'),
                                          coords=dict(
                                              time=self.data[exp]['time']))



