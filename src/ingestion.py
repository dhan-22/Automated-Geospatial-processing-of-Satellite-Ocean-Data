# src/ingestion.py

import os
import xarray as xr

def load_ocean_dataset(file_path: str, variable_name: str) -> xr.DataArray:
    """
    Loads a NetCDF (.nc) file using xarray and extracts the specified variable array.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")
        
    ds = xr.open_dataset(file_path, engine="netcdf4")
    if variable_name not in ds:
        raise KeyError(f"Variable '{variable_name}' not found in dataset. Available: {list(ds.data_vars)}")
    return ds[variable_name]