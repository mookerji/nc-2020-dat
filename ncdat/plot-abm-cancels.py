import sys

from palettable.colorbrewer.sequential import OrRd_9
from matplotlib.colors import ListedColormap, to_hex

import click
import geopandas as gpd
import matplotlib
import pandas as pd

from absentee_sent import read_absentee_voter_file
from shapefiles import load_shapefile_counties, to_kml, read_zip_codes

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-c', '--county', type=str, default=None)
@click.option('-p', '--party', type=str, default='Democrats')
def main(filename, county, party):

    # Get absentee
    absentee = read_absentee_voter_file(filename)
    if county:
        absentee = absentee[absentee.county_desc == county]
        prefix = county
    else:
        prefix = 'state'

    absentee.dropna(subset=['ballot_rtn_status', 'ballot_mail_street_address'], inplace=True)
    absentee \
      = absentee[~absentee.ballot_rtn_status.str.contains('ACCEPTED') & (absentee.party == party)]
    address \
      = absentee.ballot_mail_street_address.apply(lambda s: s if s.rfind('#') == -1 else s[:s.rfind('#')].rstrip())

    absentee['location'] \
      = address + ', ' + absentee.ballot_mail_city + ', ' +  absentee.ballot_mail_state + " " + absentee.ballot_mail_zip.round().astype(str)
    try:
        absentee['precinct'] = absentee.precinct_desc.str.lstrip('PCT').dropna().astype(int)
    except:
        absentee['precinct'] = absentee.precinct_desc
    absentee.index.name = 'row_number'

    # Output
    cols = ['race', 'age_group', 'gender', 'location', 'ballot_rtn_status']
    absentee[cols].to_csv(f'limbo/{prefix}_rejected_all.csv')

    # Precints

    # precincts = gpd.read_file('limbo/voter_precinct/Voter_Precinct.shp')
    # precincts = precincts[['precno', 'geometry']]
    # precincts['name'] = precincts['precno']
    # precincts.set_index('precno', inplace=True)
    # precincts['count'] = absentee.groupby(by='precinct').county_desc.count()
    # precincts.dropna(subset=['count'], inplace=True)
    # bins = [0, 2, 10, 20]
    # precincts['quantile'] \
    #   = pd.cut(precincts['count'], bins, duplicates='drop').astype('str')
    # cols = ['name', 'count', 'quantile', 'geometry']
    # to_kml(precincts[cols], f'limbo/{prefix}_rejected_precincts.kml')

    # Zipcodes
    count_by_zip_code = absentee.groupby(by='voter_zip').county_desc.count()
    zips = read_zip_codes()
    zips['count'] = count_by_zip_code
    zips.dropna(subset=['count'], inplace=True)
    bins = [0, 5, 20, 40, 60, 200]
    zips['quantile'] \
      = pd.cut(zips['count'], bins, duplicates='drop').astype('str')
    ts = pd.Timestamp.now().isoformat()
    to_kml(zips[['count', 'quantile', 'geometry']], f'limbo/{prefix}_rejected_zip_{ts}.kml')


if __name__ == '__main__':
    sys.exit(main())
