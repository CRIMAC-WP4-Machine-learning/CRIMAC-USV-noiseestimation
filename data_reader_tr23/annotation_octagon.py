import numpy as np
import xarray as xr
import pandas as pd

class AnnotationOctagon():
    def __init__(self, timestamps, cog, sog, wind_dir):
        timestamps=timestamps[:-1]
        self.data = self.create_empty_xarray_dataset(timestamps, cog, sog, wind_dir)

    def create_empty_xarray_dataset(self,timestamps, cog, sog, wind_dir):
        """
        Create an xarray dataset with only the time coordinate.

        Parameters:
        - timestamps: numpy.ndarray, array of timestamps.

        Returns:
        - dataset: xarray.Dataset, the created dataset.
        """
        # Create a pandas DataFrame with timestamps
        data_dict = {'time': timestamps, 'coverage': np.floor(np.arange(len(timestamps)) / 32), 'leg': np.arange(len(timestamps)) % 8, 'cog':cog, 'sog':sog, 'true_wind_dir': wind_dir}
        df = pd.DataFrame(data_dict)

        # Convert the DataFrame to an xarray dataset
        dataset = xr.Dataset.from_dataframe(df)

        return dataset

    def add_variable_to_dataset(self, values, variable_name):
        """
        Add a new variable to an xarray dataset.

        Parameters:
        - dataset: xarray.Dataset, input dataset.
        - variable_name: str, name of the new variable.

        Returns:
        - dataset_with_variable: xarray.Dataset, dataset with the added variable.
        """
        self.data[variable_name] = xr.DataArray(values, coords=[self.data['time']], dims=['time'])

    def to_csv(self, file_path):
        """
        Save a pandas DataFrame to a CSV file.

        Parameters:
        - dataframe: pandas.DataFrame, the DataFrame to be saved.
        - file_path: str, the file path (including filename and extension) where the CSV file will be saved.
        - index: bool, whether to include the DataFrame index in the saved CSV file. Default is False.
        """
        dataframe = self.data.to_dataframe()

        dataframe.to_csv(file_path)