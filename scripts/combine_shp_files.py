import pandas as pd
import geopandas 
import glob

files = glob.glob("../data/map_data/*/*_1.shp")
gdf = pd.concat([
    geopandas.read_file(shp)
    for shp in files
]).pipe(geopandas.GeoDataFrame)

gdf.to_file("../data/map_data/central_america.shp")
