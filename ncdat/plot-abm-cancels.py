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
@click.option('-z', '--zip-file', type=click.Path(exists=True))
@click.option('-c', '--county', type=str, default=None)
@click.option('-p', '--party', type=str, default='Democrats')
def main(filename, zip_file, county, party):
    # Get absentee
    absentee = read_absentee_voter_file(filename)
    if county:
        absentee = absentee[absentee.county_desc == county]
        prefix = county
    else:
        prefix = 'state'
    # Only mail ballots
    absentee = absentee[absentee.ballot_req_type == 'MAIL']
    absentee.dropna(subset=['ballot_rtn_status'], inplace=True)
    absentee \
      = absentee[~absentee.ballot_rtn_status.str.contains('ACCEPTED') & (absentee.party == party)]

    reasons = {}
    for zip_code, group in absentee.groupby(by='voter_zip'):
        reasons[zip_code] = group.groupby(
            by='ballot_rtn_status').county_desc.count()
    reasons = pd.DataFrame(reasons).T.fillna(0)

    # Zipcodes
    count_by_zip_code = absentee.groupby(by='voter_zip').county_desc.count()
    zips = read_zip_codes(zip_file)
    zips['total'] = count_by_zip_code
    zips.dropna(subset=['total'], inplace=True)
    bins = [0, 5, 20, 40, 60, 200]
    zips['quantile'] \
      = pd.cut(zips['total'], bins, duplicates='drop').astype('str')

    zips = zips.join(reasons).fillna(0)
    ts = pd.Timestamp.now().isoformat()
    prefix = party.lower()
    out = zips[['total', 'quantile', 'geometry'] +list(reasons.columns.values)]
    to_kml(out, f'limbo/{prefix}_rejected_zip_{ts}.kml')


if __name__ == '__main__':
    sys.exit(main())
