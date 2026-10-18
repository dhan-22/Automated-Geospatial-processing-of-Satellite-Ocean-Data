import xarray as xr


def slice_bay_of_bengal(
    da: xr.DataArray,
    min_lat: float = 5.0,
    max_lat: float = 25.0,
    min_lon: float = 80.0,
    max_lon: float = 95.0,
) -> xr.DataArray:
    """Slices an xarray DataArray to the Bay of Bengal bounding box.

    Dynamically handles latitude direction (ascending vs. descending).
    """
    # Detect coordinate names (lat vs latitude, lon vs longitude)
    lat_name = next((c for c in ["lat", "latitude"] if c in da.coords), None)
    lon_name = next((c for c in ["lon", "longitude"] if c in da.coords), None)

    if lat_name is None or lon_name is None:
        raise ValueError(
            f"Coordinate names not recognized. Found: {list(da.coords.keys())}"
        )

    # Check whether latitude is ordered south-to-north or north-to-south
    lat_vals = da[lat_name].values
    is_lat_ascending = lat_vals[0] < lat_vals[-1]

    # Assign slice order accordingly
    lat_slice = (
        slice(min_lat, max_lat) if is_lat_ascending else slice(max_lat, min_lat)
    )
    lon_slice = slice(min_lon, max_lon)

    # Extract the subset
    sliced_da = da.sel({lat_name: lat_slice, lon_name: lon_slice})

    return sliced_da