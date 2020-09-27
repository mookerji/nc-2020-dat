import sys

import click
import pandas as pd


def read_responses(filename):
    dfg = pd.read_csv(filename, parse_dates=['Timestamp'])
    columns = {
        'Zip Code ':
        'zip_code',
        'Would you be comfortable serving as an INSIDE poll observer?':
        'inside_out',
        'County (please select the COUNTY where you will be  in during Early Voting (Oct. 15-31) and Election Day (Nov. 3)':
        'county',
    }
    dfg.rename(columns=columns, inplace=True)
    dfg['weekofyear'] = dfg.Timestamp.dt.weekofyear
    return dfg


def count_vols(dfg, county='Mecklenburg'):
    meck = dfg[dfg.county == 'Mecklenburg']
    where_key = 'inside_out'
    elect_day_col = 'Which of these ELECTION DAY (November 3rd) shifts work for you?'
    for date, week in meck.groupby(pd.Grouper(freq='W-SAT', key='Timestamp')):
        # Inside or out
        both = week[week[where_key] == 'EITHER Inside OR Outside']
        counts = both[both.columns[both.columns.str.contains(
            'Early Voting is')]].count(axis=1)
        early_both = counts[counts > 0].count()

        # Inside or out - election day
        f = both[elect_day_col]
        elect_both = f[f != 'None'].count()

        # Outside only
        outside = week[week[where_key] == 'Outside Only']
        counts = outside[outside.columns[outside.columns.str.contains(
            'Early Voting is')]].count(axis=1)
        early_outside = counts[counts > 0].count()

        # Outside - election day
        f = outside[elect_day_col]
        elect_outside = f[f != 'None'].count()
        dt = date - pd.Timedelta(days=6)
        print(dt.strftime('%m/%d/%Y'), week.shape[0], early_both,
              early_outside, elect_both, elect_outside)


@click.command()
@click.option('-f', '--filename', type=str)
def main(filename):
    count_vols(read_responses(filename))


if __name__ == '__main__':
    sys.exit(main())
