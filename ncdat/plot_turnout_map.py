import sys

import click
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from absentee_sent import read_absentee_voter_file

def load_precincts_shapes():
    precincts = gpd.read_file('limbo/SBE_PRECINCTS_20201018/SBE_PRECINCTS_20201018.shp')
    precincts['precinct-index'] = precincts[['county_nam', 'prec_id']].apply(lambda x: '-'.join(x), axis=1)
    precincts.set_index('precinct-index', inplace=True, drop=False)
    return precincts


def get_accepted_by_precinct(accepted):
    df = accepted.groupby(['county_desc', 'precinct_desc']).voter_reg_num.count().reset_index()
    df['VOTED'] = df['voter_reg_num']
    return df.drop(labels=['voter_reg_num'], axis=1).set_index(['county_desc', 'precinct_desc'])


def load_registered(filename):
    return pd.read_csv(filename).set_index(['county_desc', 'precinct_desc'])

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-r', '--registered-filename', type=str, default='limbo/registered-per-precinct-latest.csv')
@click.option('-p', '--party', type=str, default='Democrats')
def main(filename, registered_filename, party):
    absentee = read_absentee_voter_file(filename)
    accepted = absentee[(absentee.ballot_rtn_dt >= '2020-09-01')
                        & (absentee.ballot_rtn_status == 'ACCEPTED')
                        & (absentee.ballot_rtn_dt <= pd.datetime.now())]
    accepted = accepted[accepted.voter_party_code == party]
    by_precinct = get_accepted_by_precinct(accepted)
    precinct_shapes = load_precincts_shapes()
    registered = load_registered(registered_filename)
    ts = pd.Timestamp.now().isoformat()
    turnout = registered.join(by_precinct)
    turnout['ACTIVE+VOTED(%)'] = 100.*turnout['ACTIVE']/turnout['TOTAL']
    ts = pd.Timestamp.now().isoformat()
    print(f'limbo/turnout-per-precinct-{ts}.csv')
    turnout.to_csv(f'limbo/turnout-per-precinct-{ts}.csv')
    print(f'limbo/turnout-per-precinct-latest.csv')
    turnout.to_csv(f'limbo/turnout-per-precinct-latest.csv')




if __name__ == '__main__':
    sys.exit(main())
