import spatialdata
from spatialdata.transformations import Identity
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize
from shapely.geometry import Polygon, mapping
from skimage.draw import polygon_perimeter

def rasterize_shapes_into_image(sdata, shape_key, ref_image_key, name=None):

    gdf = sdata.shapes[shape_key]

    #reference image to get the dimensions of the raster
    width, height = sdata.images[ref_image_key][list(sdata.images[ref_image_key].keys())[0]].image.shape[1:]
    transform = rasterio.transform.from_bounds(*gdf.total_bounds, width, height)
    raster = np.zeros((height, width), dtype=np.uint16)

    polygons = gdf.geometry

    def rasterize_perimeters(raster, polygons, transform, intensity=10000):
        for poly in polygons:
            if isinstance(poly, Polygon):
                exterior_coords = np.array(poly.exterior.coords)
                rows, cols = rasterio.transform.rowcol(transform, exterior_coords[:, 0], exterior_coords[:, 1])
                # Flip the rows on the y-axis
                rows = raster.shape[0] - 1 - np.array(rows)
                rr, cc = polygon_perimeter(rows, cols, shape=raster.shape)
                raster[rr, cc] = intensity
        return raster
    
    raster = rasterize_perimeters(raster, polygons, transform)
    # add a channel dimension to the raster as a numpy array
    raster_expanded = np.expand_dims(raster, axis=0)

    # raster_expanded = raster.expand_dims(dim='c', axis=0)

    if name is None:
        name = f"{shape_key}_raster"
    
    raster_layer = spatialdata.models.Image2DModel.parse(data=raster_expanded, dims=['c','y', 'x'], transformations={"pixels": Identity()})
    sdata.images[name] = raster_layer
    print("Rasterization complete. The raster is saved as 'rasterized_perimeters.tif'.")
    return sdata
    