import click
import pandas as pd

DEFAULT_ONE_STOP_FILE = 'data/one-stop-absentee/StatewideList.txt'

def read_one_stop(filename = DEFAULT_ONE_STOP_FILE):
    df = pd.read_csv(filename, header=None, error_bad_lines=False,
                 engine='c',  sep='\t', parse_dates=[6])
    names = {0: 'election_date', 1: 'CountyName', 3: 'LocationName', 4: 'Address1', \
             5: 'Address2', 6: 'date', 7: 'hours'}
    df = df.rename(columns=names)
    df['hours_date'] = df[['date', 'hours']].apply(lambda t: ', '.join([t[0].strftime('%D'), t[1]]), axis=1)
    grouped = []
    for location, loc_group in df.groupby(['Address1', 'Address2']):
        record = {'County': loc_group.CountyName.unique()[0],
                  'LocationName': loc_group.LocationName.unique()[0],
                  'Address': location[0] + ', ' + location[1],
                  'Dates': loc_group.hours_date.str.cat(sep='\n '),
                 }
        grouped.append(record)
    return pd.DataFrame(grouped)

@click.command()
def main():
    one_stop = read_one_stop()
    one_stop.to_csv('data/one-stop-absentee.csv', index=False)
    return one_stop

if __name__ == '__main__':
    sys.exit(main())
