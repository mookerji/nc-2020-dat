import click
import pandas as pd

import sys

DEFAULT_FILENAME = 'limbo/absentee_demo_stats_20201103.csv'


def read_absentee_req(filename=DEFAULT_FILENAME, start_date='2020-01-01'):
    df = pd.read_csv(filename, parse_dates=['election_dt'])
    df['request_week_date'] \
      = pd.to_datetime('2020-01-01') + df['request_week_num'].apply(lambda t: pd.Timedelta(weeks=t))
    final_date = pd.datetime.now() + pd.Timedelta(weeks=1)
    df = df[(df['request_week_date'] <= final_date)
            & (df['request_week_date'] >= start_date)]
    other = ['GREEN', 'LIBERTARIAN', 'CONSTITUTION']
    df['party_desc'] = df['party_desc'].apply(lambda t: 'other'
                                              if t in other else t)
    return df.sort_values(by='request_week_date')


@click.command()
def main():
    # 2020
    pass


if __name__ == '__main__':
    sys.exit(main())
