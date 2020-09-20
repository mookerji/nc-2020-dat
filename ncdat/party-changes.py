import click
import pandas as pd

import sys

DEFAULT_FILENAME = 'data/changes/2020_party_change_list.csv'


def parse_party_changes(filename=DEFAULT_FILENAME):
    rename = {
        'UNA': 'unaffiliated',
        'DEM': 'democrats',
        'REP': 'republicans',
        'LIB': 'libertarians',
        'CST': 'constitution',
        'GRE': 'green'
    }
    changes_df = pd.read_csv(filename)
    changes_df['date'] = pd.to_datetime(changes_df.change_dt)
    changes_df.drop(
        labels=['change_dt', 'voter_reg_num', 'year_change', 'county_id'],
        axis=1,
        inplace=True)
    changes_df['party_from'] = changes_df['party_from'].apply(rename.get)
    changes_df['party_to'] = changes_df['party_to'].apply(rename.get)
    changes_df['event'] \
      = changes_df['party_from'] + '-to-' + changes_df['party_to']
    changes_df['county_name'] = changes_df[' county_name']
    # There must be a better way to do this...
    changes_df['net_democrats'] = 0
    changes_df['net_republicans'] = 0
    changes_df['net_unaffiliated'] = 0
    changes_df['net_other'] = 0
    for p in ['democrats', 'republicans', 'unaffiliated']:
        changes_df[f'net_{p}'] \
          += -1 * (changes_df['party_from'] == p).astype('int')
        changes_df[f'net_{p}'] += (changes_df['party_to'] == p).astype('int')
    for p in ['libertarians', 'green', 'constitution']:
        changes_df['net_other'] \
          += -1 * (changes_df['party_from'] == p).astype('int')
        changes_df['net_other'] += (changes_df['party_to'] == p).astype('int')
    return changes_df.drop(labels=[' county_name'], axis=1)


@click.command()
def main():
    # 2020
    party_changes = parse_party_changes()
    party_changes.to_csv('data/party-changes-2020.csv')


if __name__ == '__main__':
    sys.exit(main())
