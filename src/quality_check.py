import numpy as np
import xarray as xr


def inspect_dataset(da):
    """Inspect satellite ocean data."""
    assert da is not None, "Dataset cannot be None"
    assert isinstance(da, xr.DataArray), "Input must be an xarray DataArray"
    assert da.size > 0, "Input array cannot be empty"

    values = np.asarray(da.values)
    assert np.issubdtype(values.dtype, np.number), "Array must contain numeric values"

    report = {
        "variable": da.name,
        "dimensions": dict(da.sizes),
        "units": da.attrs.get("units", "Unknown"),
        "missing_values": int(np.isnan(values).sum()),
        "infinite_values": int(np.isinf(values).sum()),
        "valid_values": int(np.isfinite(values).sum()),
    }

    valid_values = values[np.isfinite(values)]

    suspicious_values = valid_values[
        (valid_values < -2) | (valid_values > 40)
    ]

    report["suspicious_values"] = int(suspicious_values.size)
    assert report["suspicious_values"] <= valid_values.size
    if valid_values.size > 0:
        report["minimum"] = float(valid_values.min())
        report["maximum"] = float(valid_values.max())
    else:
        report["minimum"] = None
        report["maximum"] = None

    print("\n--- DATA QUALITY REPORT ---")

    for key, value in report.items():
        print(f"{key}: {value}")

    return report
if __name__ == "__main__":
    import xarray as xr

    sample_data = xr.DataArray(
        [[28.5, 29.1, 30.0],
         [27.8, float("nan"), 29.4],
         [28.2, 30.1, 29.7]],
        dims=["latitude", "longitude"],
        name="sst",
        attrs={"units": "°C"}
    )
    inspect_dataset(sample_data)