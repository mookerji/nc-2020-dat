import click
import pandas as pd

import sys

cols = [
    'Estimate!!Total!!Female!!18 years and over!!Foreign born!!Naturalized U.S. citizen',
    'Estimate!!Total!!Female!!18 years and over!!Native',
    'Estimate!!Total!!Male!!18 years and over!!Foreign born!!Naturalized U.S. citizen',
    'Estimate!!Total!!Male!!18 years and over!!Native',
]


def read_cvap_data(filename, col='cvap.all_races(count)'):
    cvap_df = pd.read_csv(filename, skiprows=1)
    cvap_df['CountyName'] \
      = cvap_df['Geographic Area Name'].apply(lambda t: t.replace(' County, North Carolina', '').upper())
    cvap_df.set_index('CountyName', inplace=True, drop=False)
    cvap_df[col] = cvap_df[cols].sum(axis=1)
    cvap_df.drop('NORTH CAROLINA', inplace=True)
    return cvap_df[[col, 'CountyName']]


def main():
    # Everyone
    filename = 'data/cvap/productDownload_2020-07-28T211825/ACSDT5Y2018.B05003_data_with_overlays_2020-07-28T211821.csv'
    cvap_df = read_cvap_data(filename)
    cvap_df.to_csv('data/cvap2020_all_races.csv', index=False)

    # African Americans
    filename = 'data/cvap/productDownload_2020-08-08T010026/ACSDT5Y2018.B05003B_data_with_overlays_2020-08-08T005955.csv'
    cvap_aa_df = read_cvap_data(filename, col='cvap.black_aa(count)')
    cvap_aa_df.to_csv('data/cvap2020_black_aa.csv', index=False)

    filename = 'data/cvap/productDownload_2020-08-09T170305/ACSDT5Y2018.B05003H_data_with_overlays_2020-08-09T170249.csv'
    cvap_white_df = read_cvap_data(filename, col='cvap.white(count)')
    cvap_white_df.to_csv('data/cvap2020_white.csv', index=False)

    cvap = cvap_df.join(cvap_aa_df, rsuffix='_r').drop(
        ['CountyName_r'], axis=1).join(cvap_white_df,
                                       rsuffix='_r').drop(['CountyName_r'],
                                                          axis=1)
    cvap['pct_cvap.black_aa(%)'] \
      = 100 * cvap['cvap.black_aa(count)'] / cvap['cvap.all_races(count)']
    cvap['pct_cvap.white(%)'] \
      = 100 * cvap['cvap.white(count)'] / cvap['cvap.all_races(count)']
    cvap['pct_cvap.all_races.within_state(%)'] \
      = 100 * cvap['cvap.all_races(count)'] / cvap['cvap.all_races(count)'].sum()
    cvap.to_csv('data/cvap2020.csv', index=False)
    return cvap


if __name__ == '__main__':
    sys.exit(main())
