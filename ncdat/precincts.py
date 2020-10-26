import geopandas as gpd
import pandas as pd

from shapefiles import to_kml

# ogr2ogr -f KML -simplify 0.001 limbo/eday_precincts_to_2k_simp.kml limbo/eday_precincts_to_2k.kml
# ogr2ogr -f KML -simplify 0.001 limbo/eday_precincts_from_2k_simp.kml limbo/eday_precincts_from_2k.kml

def main():
    polling = pd.read_csv('data/election-day-precincts/polling_place_20201103-ascii-stripped.csv',
                          error_bad_lines=False, sep='\t')
    polling['address'] \
      = polling['house_num'].astype(str) + ' ' + polling['street_name'] + ", " + polling['city'] +  ", " + polling['state'] + " "+ polling['zip'].astype(str)
    cols = ['county_name', 'polling_place_id', 'precinct_name', 'polling_place_name', 'address']

    polling[0:2000][cols].to_csv('data/election2020-general-day-precincts0-1999.csv', index=False)
    polling[2000:][cols].to_csv('data/election2020-general-day-precincts2000-.csv', index=False)

    precincts = gpd.read_file('limbo/SBE_PRECINCTS_20201018/SBE_PRECINCTS_20201018.shp')
    precincts['precinct-index'] = precincts[['county_nam', 'prec_id']].apply(lambda x: '-'.join(x), axis=1)
    precincts.set_index('precinct-index', inplace=True, drop=False)
    to_kml(precincts[['geometry']].iloc[0:2000], 'limbo/eday_precincts_to_2k.kml')
    to_kml(precincts[['geometry']].iloc[2000:], 'limbo/eday_precincts_from_2k.kml')

main()
