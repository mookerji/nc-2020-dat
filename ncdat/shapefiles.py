import sys

import click
import fiona
import geopandas as gpd

# ZIP_FILENAME = '/Users/mookerji/Downloads/ZIP_Code_Tabulation_Areas-shp/ZIP_Code_Tabulation_Areas.shp'

# def read_precints(filename='limbo/voter_precinct/Voter_Precinct.shp'):
#     precincts = gpd.read_file(filename)
#     precints.index = precints['ZCTA5CE10'].astype('int')
#     return precints

ZIP_FILENAME = '/Users/mookerji/Downloads/ZIP_Code_Tabulation_Areas-shp/ZIP_Code_Tabulation_Areas.shp'


def read_zip_codes(filename=ZIP_FILENAME):
    zip_codes = gpd.read_file(filename)
    zip_codes.index = zip_codes['ZCTA5CE10'].astype('int')
    return zip_codes


COUNTY_SHAPEFILE_NAME = "data/shapefiles/NC_Counties-shp/counties.shp"


def load_shapefile_counties(filename=COUNTY_SHAPEFILE_NAME):
    nc_shape \
      = gpd.read_file(filename).set_index('CO_NAME', drop=False).rename(columns={'CO_NAME': 'CountyName'})
    nc_shape['land.area(square_miles)'] = nc_shape['ACRES'] / 640.
    return nc_shape


DISTRICTS_FILENAME = "data/shapefiles/HB 1020 H Red Comm CSBK-25_Shapefile/HB 1020 H Red Comm CSBK-25.shp"


def load_shapefile_districts(filename=DISTRICTS_FILENAME):
    return gpd.read_file(filename).set_index('DISTRICT')


def load_meck_polling_locations():
    df = gpd.read_file(
        'limbo/voter_polling_location/Voter_Polling_Location.shp')
    df['address'] = df['address'] + ', ' + df['city'] + ', NC'
    return df


def to_kml(gdf, filename):
    print(filename)
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    with fiona.drivers():
        gdf.to_file(filename, driver='KML')


@click.command()
def main():
    nc_shape = load_shapefile_counties()
    nc_districts = load_shapefile_districts()
    to_kml(nc_districts, 'data/shapefiles/nc_districts_tmp.kml')
    to_kml(nc_shape[['CountyName', 'geometry']],
           'data/shapefiles/nc_counties.kml')
    locs = load_meck_polling_locations()
    cols = ['precno', 'name', 'type', 'location', 'address']
    locs[cols].to_csv('data/shapefiles/meck_polling_locations.csv')


if __name__ == '__main__':
    sys.exit(main())
