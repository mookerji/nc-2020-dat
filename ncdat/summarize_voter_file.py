import sys

import click
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from absentee_sent import read_absentee_voter_file

def read_polling_place_info():
    polling = pd.read_csv('data/election-day-precincts/polling_place_20201103-ascii-stripped.csv',
                          error_bad_lines=False, sep='\t')
    polling['address'] \
      = polling['house_num'].astype(str) + ' ' + polling['street_name'] + ", " + polling['city'] +  ", " + polling['state'] + " "+ polling['zip'].astype(str)
    polling['county_desc'] = polling['county_name']
    polling['precinct_desc'] = polling['precinct_name']
    cols = ['county_desc', 'precinct_desc', 'polling_place_name', 'address']
    return polling[cols]


def load_voter_file(filename, party):
    voters = pd.read_csv(filename, error_bad_lines=False, warn_bad_lines=False, sep='\t')
    cols = ['county_desc', 'voter_status_desc', 'party_cd', 'precinct_desc', 'race_code']
    voters = voters[cols]
    voters = voters[(voters['party_cd'] == party) & voters['voter_status_desc'].isin(['ACTIVE', 'INACTIVE'])]
    group_cols = ['county_desc',  'precinct_desc', 'voter_status_desc']
    precinct_counts \
      = voters.groupby(['county_desc',  'precinct_desc', 'voter_status_desc'])['party_cd'].count().unstack().reset_index()
    precinct_counts['TOTAL'] = precinct_counts[['ACTIVE', 'INACTIVE']].sum(axis=1)
    return precinct_counts


@click.command()
@click.option('-f', '--filename', type=str, default='limbo/nc-voter-file-stripped.csv')
@click.option('-p', '--party', type=str, default='DEM')
def main(filename, party):
    voters = load_voter_file(filename, party).set_index(['county_desc', 'precinct_desc'])
    locations = read_polling_place_info().set_index(['county_desc', 'precinct_desc'])
    ts = pd.Timestamp.now().isoformat()
    locations.join(voters).to_csv(f'limbo/registered-per-precinct-{ts}.csv')
    print(f'limbo/registered-per-precinct-latest.csv')
    locations.join(voters).to_csv(f'limbo/registered-per-precinct-latest.csv')


if __name__ == '__main__':
    sys.exit(main())
