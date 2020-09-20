import sys

import fiona
import geopandas as gpd

SHAPEFILE_NAME = "data/shapefiles/NC_Counties-shp/counties.shp"

def load_shapefile_counties(filename=SHAPEFILE_NAME):
    nc_shape = gpd.read_file(filename).set_index('CO_NAME', drop=False).rename(columns={'CO_NAME': 'CountyName'})
    nc_shape['land.area(square_miles)'] = nc_shape['ACRES']/640.
    return nc_shape

DISTRICTS_FILENAME = "data/shapefiles/HB 1020 H Red Comm CSBK-25_Shapefile/HB 1020 H Red Comm CSBK-25.shp"

def load_shapefile_districts(filename=DISTRICTS_FILENAME):
    return gpd.read_file(nc_shapefile).set_index('DISTRICT')


def to_kml(gdf, filename):
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    with fiona.drivers():
        nc_districts.to_file(filename, driver='KML')


@click.command()
def main():
    nc_shape = load_shapefile_counties()
    nc_districts = load_shapefile_districts()
    to_kml(nc_districts, 'data/shapefiles/nc_districts_tmp.kml')

if __name__ == '__main__':
    sys.exit(main())
