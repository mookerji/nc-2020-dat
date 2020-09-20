import click
import pandas as pd

import sys

PARTIES = [
    'registered.democrats(count)',
    'registered.republicans(count)',
    'registered.libertarians(count)',
    'registered.green(count)',
    'registered.constitution(count)',
    'registered.unaffiliated(count)',
    'registered.total(count)',
]

rename = {
    'Democrats': 'registered.democrats(count)',
    'Republicans': 'registered.republicans(count)',
    'Libertarians': 'registered.libertarians(count)',
    'Green': 'registered.green(count)',
    'Constitution': 'registered.constitution(count)',
    'Unaffiliated': 'registered.unaffiliated(count)',
    'White': 'registered.white(count)',
    'Black': 'registered.black(count)',
    'AmericanIndian': 'registered.american_indian(count)',
    'Other': 'registered.other(count)',
    'Hispanic': 'registered.hispanic(count)',
    'Male': 'registered.male(count)',
    'Female': 'registered.female(count)',
    'UnDisclosedGender': 'registered.undisclosed_gender(count)',
    'Total': 'registered.total(count)',
}


def registrations_to_csv(year='2020'):
    files = glob.glob('data/registration/*.json')
    data = []
    for f in files:
        if year not in f:
            continue
        df = pd.read_json(f)
        df['date'] = pd.to_datetime(f.split('/')[2].rstrip('.json'))
        data.append(df.rename(columns=rename))
    return pd.concat(data)


@click.command()
def main():
    # 2020
    registrations = registrations_to_csv()
    registrations.to_csv('data/registrations2020.csv', index=False)
    # 2016?
    registrations_2016 = registrations_to_csv(year='2016')
    registrations_2016.to_csv('data/registrations2016.csv', index=False)
    registrations_2016.head()


if __name__ == '__main__':
    sys.exit(main())
