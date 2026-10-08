from app.services.geospatial_service import (
    read_geospatial_file,
    calculate_measurement
)


def test_read_kml():
    gdf = read_geospatial_file(
        "test_data/test_polygon.kml"
    )

    assert len(gdf) == 1
    assert gdf.geometry.iloc[0].geom_type == "Polygon"


def test_polygon_area():
    gdf = read_geospatial_file(
        "test_data/test_polygon.kml"
    )

    measurements = calculate_measurement(gdf)

    assert len(measurements) == 1
    assert measurements[0]["geometry_type"] == "Polygon"
    assert measurements[0]["area_square_meters"] > 0


def test_read_shapefile_zip():
    gdf = read_geospatial_file(
        "test_data/test_shapefile.zip"
    )

    assert len(gdf) == 1
    assert gdf.geometry.iloc[0].geom_type == "Polygon"


def test_shapefile_zip_area():
    gdf = read_geospatial_file(
        "test_data/test_shapefile.zip"
    )

    measurements = calculate_measurement(gdf)

    assert len(measurements) == 1
    assert measurements[0]["geometry_type"] == "Polygon"
    assert measurements[0]["area_square_meters"] > 0