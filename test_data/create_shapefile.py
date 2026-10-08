import geopandas as gpd
from pathlib import Path

# Paths
kml_path = Path("test_data/test_polygon.kml")
output_dir = Path("test_data/shapefile")

output_dir.mkdir(exist_ok=True)

# Read the existing KML
gdf = gpd.read_file(kml_path)

# Save as Shapefile
output_path = output_dir / "test_polygon.shp"

gdf.to_file(output_path, driver="ESRI Shapefile")

print("Shapefile created successfully!")
print(f"Location: {output_path}")