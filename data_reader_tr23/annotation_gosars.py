import pandas as pd
import xarray as xr
from datetime import datetime
import numpy as np
import tools as tls
import filter
import re

class AnnotationGOSars:
    def __init__(self, filename):
        date = self._get_date(filename)
        self.data = self._read_csv_file_auto_headers(filename, date)

    def _get_date(self, file_path):
        # Read the first two lines to extract the date
        with open(file_path, 'r') as file:
            # Read the first line
            first_line = file.readline().strip()

            # Use a regular expression to extract the date
            date_pattern = re.compile(r'Date:","(\d{2}.\d{2}.\d{4})')

            # Match the date pattern
            match = date_pattern.search(first_line)

            # Extract the date if a match is found
            date_string = match.group(1)
            date = pd.to_datetime(date_string, format='%d.%m.%Y')
        return date

    def _read_csv_file_auto_headers(self,file_path, date):
        # Read the CSV file using pandas with automatic header detection
        df = pd.read_csv(file_path, encoding = "ISO-8859-1",skiprows=2)

        x=df["Time"]
        # df = df.dropna(subset=[df['%1:timestamp']])
        # x=df['%1:timestamp']
        df = df.dropna(subset=[df.columns[0]])
        df['Time'] = pd.to_datetime(df['Time'])
        date_object = pd.to_datetime(date, format='%d.%m.%Y')
        df['Time'] = df['Time'].apply(lambda x: self._change_date(x, date_object))

        attributes = df.columns[2:]
        # Convert DataFrame to xarray dataset
        dataset = self._add_dataset(df, attributes)
        return dataset

    def _add_dataset(self, df, attributes_to_add):
        '''Adds a dataset to a given dataframe df. Returns dataframe with added dataset'''
        #df = df[df['Name'] == name_to_filter]

        ds = xr.Dataset(
            coords={'time': ('time', df['Time']),
        })

        for attr in attributes_to_add:
            df[attr] = pd.to_numeric(df[attr], errors='coerce')
            ds[attr] = xr.DataArray(data=df[attr],
                                    dims=('time'),
                                    coords=dict(
                                        time=df['Time']))
        return ds

    def _convert_timestamp(self, times_array, date):
        """
           Combine a date in the format '%d.%m.%Y' with an array of times in the format 'hh:mm:ss'.

           Parameters:
           - date_string: str, the date in the format '%d.%m.%Y'.
           - times_array: array-like, an array of times in the format 'hh:mm:ss'.

           Returns:
           - datetime_array: numpy.ndarray, an array of concatenated datetime objects.
           """
        date_object = pd.to_datetime(date, format='%d.%m.%Y')
        times_datetime = pd.to_datetime(times_array, format='%H:%M:%S').time
        datetime_array = np.array([pd.Timestamp.combine(date_object, time) for time in times_datetime])
        return datetime_array

    def cut_to_timeperiod(self, timerange):
        ''''Takes xarray dataset and a timerange (start,stop) and returns the cut down dataset'''
        start, stop = timerange
        self.data = tls.subset_array_by_time(self.data, start, stop)

    def _change_date(self, dt, new_date):
        return pd.Timestamp(new_date) + pd.DateOffset(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

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

    def filter_heading(self, window, data):
        fitlered_cog=filter.filter_heading(data, window)
        self.data["Heading"] = xr.DataArray(data=fitlered_cog,
                                dims=('time'),
                                coords=dict(
                                    time=self.data['time']))

