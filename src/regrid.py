import numpy as np
import xarray as xr


def regrid_to_025(da):
    """
    Regrid ocean data to 0.25-degree resolution.
    """

    # Make sure latitude and longitude are in ascending order
    da = da.sortby("latitude").sortby("longitude")

    # Find the common coordinate limits
    lat_min = np.ceil(float(da.latitude.min()) * 4) / 4
    lat_max = np.floor(float(da.latitude.max()) * 4) / 4

    lon_min = np.ceil(float(da.longitude.min()) * 4) / 4
    lon_max = np.floor(float(da.longitude.max()) * 4) / 4

    # Create the new 0.25-degree grid
    new_lat = np.arange(lat_min, lat_max + 0.001, 0.25)
    new_lon = np.arange(lon_min, lon_max + 0.001, 0.25)

    # Interpolate data onto the new grid
    regridded = da.interp(
        latitude=new_lat,
        longitude=new_lon,
        method="linear"
    )

    return regridded