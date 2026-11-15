import numpy as np
import xarray as xr

def inspect_dataset(
da: xr.DataArray,
valid_min: float = None,
valid_max: float = None
) -> dict:

     """Inspect satellite ocean data for quality, coordinates and physical value ranges."""
     # 1. Basic input validation
     assert da is not None, "Dataset cannot be None"
     assert isinstance(da, xr.DataArray), "Input must be an Xarray DataArray"
     assert da.size > 0, "Input array cannot be empty"
     assert np.issubdtype(da.dtype, np.number), \
     "Array must contain numeric values"
     # 2. Identify variable and assign appropriate limits
     if valid_min is None and valid_max is None:
          if da.name in ("sst", "thetao"):
               valid_min, valid_max = -2.5, 40
          elif da.name in ("sss", "so"):
               valid_min, valid_max = 0, 42
          elif da.name in ("u", "v", "u10", "v10"):
               valid_min, valid_max = -100, 100
          else:
               raise ValueError(
                    "Unknown variable. Please provide valid_min and valid_max."
               )
     elif valid_min is None or valid_max is None:
               raise ValueError(
                         "Please provide both valid_min and valid_max."
                    )
     assert valid_min < valid_max, \
          "Minimum limit must be less than maximum limit"
          # 3. Coordinate validation
     latitude_names = ["latitude", "lat"]
     longitude_names = ["longitude", "lon"]
     assert any(name in da.coords for name in latitude_names), \
          "Latitude coordinate is missing"
     assert any(name in da.coords for name in longitude_names), \
          "Longitude coordinate is missing"
          # 4. Calculate data statistics using Xarray
     finite_mask = np.isfinite(da)
     missing_count = int(da.isnull().sum().compute().item())
     infinite_count = int(np.isinf(da).sum().compute().item())
     valid_count = int(finite_mask.sum().compute().item())
     finite_values = da.where(finite_mask)
     minimum = finite_values.min(skipna=True).compute().item()
     maximum = finite_values.max(skipna=True).compute().item()
               # 5. Check physical value limits
     out_of_bounds = (
               ((da < valid_min) | (da > valid_max))
               & finite_mask
               )
     out_of_bounds_count = int(
               out_of_bounds.sum().compute().item()
               )
               # 6. Generate quality report
     report = {
               "variable": da.name or "Unnamed",
               "dimensions": dict(da.sizes),
               "coordinates": list(da.coords.keys()),
               "units": da.attrs.get("units", "Unknown"),
               "total_pixels": int(da.size),
               "missing_values": missing_count,
               "infinite_values": infinite_count,
               "valid_values": valid_count,
               "minimum": float(minimum) if valid_count else None,
               "maximum": float(maximum) if valid_count else None,
               "out_of_bounds_count": out_of_bounds_count,
               "valid_range_configured": [valid_min, valid_max]
               }
               # 7. Display quality report
     print("\n--- DATA QUALITY REPORT ---")

     for key, value in report.items():
          print(f"{key}: {value}")
     return report