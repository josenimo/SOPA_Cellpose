import rasterio
import geopandas as gpd
from shapely.geometry import shape
from rasterio.features import shapes
import numpy as np
import pandas as pd

def raster_to_geodataframe(tif_path, output_path, crs='EPSG:4326'):
    """
    Convert a TIFF file with segmentation labels to a GeoDataFrame.
    
    Parameters:
    - tif_path: str, path to the input TIFF file.
    - crs: str, the Coordinate Reference System of the output GeoDataFrame.
    
    Returns:
    - GeoDataFrame containing the polygons and their associated labels.
    """

    assert tif_path.endswith('.tif'), "Input file must be a TIFF file"
    assert output_path.endswith('.geojson'), "Output file must end in .geojson"

    with rasterio.open(tif_path) as src:
        # Read the image data
        image = src.read(1)  # Read the first band
        
        # Define the affine transformation
        transform = src.transform
        
        # Extract the shapes and values from the raster
        results = list(shapes(image.astype(np.int32), transform=transform))
        
        # Create a DataFrame from the shapes and values
        geometries = [shape(geom) for geom, value in results]
        values = [value for geom, value in results]

        # Filter out polygons with a value of 0.0
        filtered_geometries = [geom for geom, value in zip(geometries, values) if value != 0.0]
        filtered_values = [value for value in values if value != 0.0]
        
        # Create a DataFrame with required columns
        df = pd.DataFrame({
            'geometry': filtered_geometries,
            'objectType': ['annotation'] * len(filtered_geometries),
            'name': filtered_values
        })
        
        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        
        # Set the coordinate reference system (CRS)
        gdf.crs = crs

    print(f"GeoDataFrame created, now saving to {output_path}")
    gdf.to_file(output_path)
    
    return gdf