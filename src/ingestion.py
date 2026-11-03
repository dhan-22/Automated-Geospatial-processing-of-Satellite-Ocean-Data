# src/ingestion.py

import os
import xarray as xr
import copernicusmarine

def download_ocean_data(dataset_id: str, variable: str, output_dir="data/raw/", filename="sample.nc"):
    """
    Generic helper to download any dataset subset (SST, SSS, or Surface Wind) from Copernicus Marine.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading {variable} dataset from Copernicus Marine...")
    copernicusmarine.subset(
        dataset_id=dataset_id,
        variable=variable,
        minimum_longitude=80.0,
        maximum_longitude=95.0,
        minimum_latitude=5.0,
        maximum_latitude=25.0,
        start_datetime="2024-01-01T00:00:00",
        end_datetime="2024-01-02T00:00:00",
        output_directory=output_dir,
        output_filename=filename
    )
    print(f"Download complete: {os.path.join(output_dir, filename)}")

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

    return sliced_da
