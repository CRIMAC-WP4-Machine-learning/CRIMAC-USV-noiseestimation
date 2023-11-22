import pandas as pd
import xarray as xr
from datetime import datetime
import numpy as np
import tools as tls
import filter

class AnnotationOBS:
    def __init__(self, filename):
        self.data = self._read_csv_file_auto_headers(filename)

    def _read_csv_file_auto_headers(self,file_path):
        # Read the CSV file using pandas with automatic header detection
        df = pd.read_csv(file_path)

        x=df['%1:timestamp']
        # df = df.dropna(subset=[df['%1:timestamp']])
        # x=df['%1:timestamp']
        df = df.dropna(subset=[df.columns[0]])
        df['%1:timestamp'] = [self._convert_timestamp(t) for t in df['%1:timestamp']]

        attributes = df.columns[1:]
        # Convert DataFrame to xarray dataset
        dataset = self._add_dataset(df, attributes)
        return dataset

    def _add_dataset(self, df, attributes_to_add):
        '''Adds a dataset to a given dataframe df. Returns dataframe with added dataset'''
        #df = df[df['Name'] == name_to_filter]

        ds = xr.Dataset(
            coords={'time': ('time', df['%1:timestamp']),
        })

        for attr in attributes_to_add:
            df[attr] = pd.to_numeric(df[attr], errors='coerce')
            ds[attr] = xr.DataArray(data=df[attr],
                                    dims=('time'),
                                    coords=dict(
                                        time=df['%1:timestamp']))
        return ds

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

    def average_between_periods(self,periods, variablename):
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

            mask = (self.data['time'] >= start_time) & (self.data['time'] <= end_time)

            # Apply the mask to obtain the subset array
            subset_dataset = self.data.sel(time=mask)
            # Filter dataframe for the specified period

            # Calculate the average 'cog' value for the period
            average_cog = subset_dataset[variablename].mean()

            average_cog_values.append(average_cog.values)

        return average_cog_values

    def filter_heading(self, window):
        fitlered_cog=filter.filter_heading(self.data["6:cog"], window)
        self.data["6:cog"] = xr.DataArray(data=fitlered_cog,
                                dims=('time'),
                                coords=dict(
                                    time=self.data['time']))

