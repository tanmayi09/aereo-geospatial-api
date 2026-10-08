import geopandas as gpd
import pandas as pd
import math
import zipfile
import tempfile
from pathlib import Path


def read_geospatial_file(file_path: str):
    """
    Read a KML or zipped Shapefile.
    """

    path = Path(file_path)

    if path.suffix.lower() == ".kml":
        return gpd.read_file(path)

    if path.suffix.lower() == ".zip":

        temp_dir = tempfile.mkdtemp()

        with zipfile.ZipFile(path, "r") as zip_ref:
            for member in zip_ref.infolist():
                target_path = Path(temp_dir) / member.filename

                if not str(target_path.resolve()).startswith(
                    str(Path(temp_dir).resolve())
            ):
                    raise ValueError("Unsafe ZIP file")

            zip_ref.extract(member, temp_dir)

        temp_path = Path(temp_dir)

        shapefiles = list(temp_path.rglob("*.shp"))

        if not shapefiles:
            raise ValueError(
                "No Shapefile (.shp) found inside the ZIP file"
            )

        return gpd.read_file(shapefiles[0])

    raise ValueError(
        "Unsupported file format. Only KML and ZIP files are supported."
    )


def clean_value(value):
    """
    Convert pandas and NumPy values into JSON-safe values.
    """

    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if hasattr(value, "item"):
        return value.item()

    return value


def extract_features(gdf):
    """
    Extract information about each geospatial feature.
    """

    features = []

    for index, row in gdf.iterrows():

        properties = {}

        for column in gdf.columns:

            if column != "geometry":
                properties[column] = clean_value(row[column])

        feature = {
            "feature_id": index,
            "geometry_type": row.geometry.geom_type,
            "geometry": row.geometry.__geo_interface__,
            "crs": str(gdf.crs),
            "properties": properties
        }

        features.append(feature)

    return features


def calculate_measurement(gdf):
    """
    Calculate area for polygons
    and length for LineStrings.
    """

    if gdf.empty:
        return []

    measurement_gdf = gdf.copy()

    # Transform geographic coordinates into a projected CRS
    # before calculating measurements.
    if measurement_gdf.crs and measurement_gdf.crs.is_geographic:

        projected_crs = measurement_gdf.estimate_utm_crs()

        if projected_crs:
            measurement_gdf = measurement_gdf.to_crs(
                projected_crs
            )

    measurements = []

    for index, row in measurement_gdf.iterrows():

        geometry = row.geometry
        geometry_type = geometry.geom_type

        measurement = {
            "feature_id": index,
            "geometry_type": geometry_type
        }

        if geometry_type in ["Polygon", "MultiPolygon"]:

            measurement["area_square_meters"] = geometry.area

        elif geometry_type in ["LineString", "MultiLineString"]:

            measurement["length_meters"] = geometry.length

        elif geometry_type == "Point":

            measurement["measurement"] = None

        else:

            measurement["measurement"] = None

        measurements.append(measurement)

    return measurements