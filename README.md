# Aereo Geospatial File Measurement API

A backend API for uploading, processing, and measuring geospatial files such as KML and Shapefile ZIP archives.

## Features

- Upload KML files
- Upload ZIP files containing Shapefiles
- Extract geospatial features
- Detect geometry types
- Extract feature properties
- Detect Coordinate Reference System (CRS)
- Calculate polygon area
- Calculate LineString length
- Handle Point geometries without measurements
- Transform geographic CRS to a projected CRS before measurement
- Store processed file information in SQLite
- Retrieve uploaded file information using a file ID
- Retrieve measurements separately
- Safe ZIP extraction
- Automated tests using pytest

## Technology Stack

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Fiona
- SQLAlchemy
- SQLite
- Pytest

## Project Structure

```text
aereo-geospatial-api/
│
├── app/
│   ├── api/
│   │   └── upload.py
│   │
│   ├── models/
│   │   └── file.py
│   │
│   ├── services/
│   │   └── geospatial_service.py
│   │
│   ├── utils/
│   │
│   ├── database.py
│   └── main.py
│
├── test_data/
│   ├── create_shapefile.py
│   └── test_polygon.kml
│
├── tests/
│   ├── conftest.py
│   └── test_geospatial.py
│
├── uploads/
├── requirements.txt
├── .gitignore
└── README.md