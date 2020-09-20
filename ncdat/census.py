import click
import pandas as pd

import sys

cols = ['Estimate!!Total!!Female!!18 years and over!!Foreign born!!Naturalized U.S. citizen',
        'Estimate!!Total!!Female!!18 years and over!!Native',
        'Estimate!!Total!!Male!!18 years and over!!Foreign born!!Naturalized U.S. citizen',
        'Estimate!!Total!!Male!!18 years and over!!Native',
       ]

def read_cvap_data(filename, col='cvap.all_races(count)'):
    cvap_df = pd.read_csv(filename, skiprows=1)
    cvap_df['CountyName'] = cvap_df['Geographic Area Name'].apply(lambda t: t.replace(' County, North Carolina', '').upper())
    cvap_df.set_index('CountyName', inplace=True, drop=False)
    cvap_df[col] = cvap_df[cols].sum(axis=1)
    cvap_df.drop('NORTH CAROLINA', inplace=True)
    return cvap_df[[col, 'CountyName']]


def main():
    filename = 'data/cvap/productDownload_2020-07-28T211825/ACSDT5Y2018.B05003_data_with_overlays_2020-07-28T211821.csv'
    cvap_df = read_cvap_data(filename)
    cvap_df.to_csv('data/cvap2020_all_races.csv', index=False)
    cvap_df

if __name__ == '__main__':
    sys.exit(main())
