import sys

from palettable.colorbrewer.sequential import OrRd_9
from matplotlib.colors import ListedColormap, to_hex

import click
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from absentee_sent import read_absentee_voter_file


def plot_by_party(county, results):
    data = results.groupby(
        by=['site_name', 'voter_party_code']).count().county_desc.unstack()
    data['total'] = data.sum(axis=1)
    cols = ['Democrats', 'Republicans', 'Unaffiliated', 'Other (LIB-GRE-CST)']
    colors = ['deepskyblue', 'tomato', 'slategray', 'green']
    ax = data.sort_values(by='total').plot.barh(y=cols,
                                                stacked=True,
                                                color=colors)
    ax.set_ylabel('Early Voting Site Name, Grouped By Party')
    ax.set_xlabel('Total')
    ax.set_title(
        f'One-Stop Votes, {county} County\n Ballot Status=ACCEPTED, CONFLICT, CANCELLED, NOT VOTED, WRONG VOTER'
    )
    name = county.lower()
    print(f'assets/images/one-stop/county-party-totals/{name}.png')
    ax.get_figure().savefig(
        f'assets/images/one-stop/county-party-totals/{name}.png',
        bbox_inches='tight')


def plot_by_race(county, results):
    data = results.groupby(
        by=['site_name', 'race']).count().county_desc.unstack()
    data['total'] = data.sum(axis=1)
    ax = data.sort_values(by='total').plot.barh(y=results.race.unique(), stacked=True)
    ax.set_ylabel('Early Voting Site Name')
    ax.set_xlabel('Total')
    plt.legend(prop={'size': 6})
    ax.set_title(f'One-Stop Votes, {county} County, Grouped By Race')
    name = county.lower()
    print(f'assets/images/one-stop/county-race-totals/{name}.png')
    ax.get_figure().savefig(
        f'assets/images/one-stop/county-race-totals/{name}.png',
        bbox_inches='tight')


def plot_by_age_group(county, results):
    data = results.groupby(
        by=['site_name', 'age_group']).count().county_desc.unstack()
    # TODO: remove if we coerce to strings at parse time
    to_plot = data.columns.astype(str)
    data.columns = data.columns.astype(str)
    data['total'] = data.sum(axis=1)
    ax = data.sort_values(by='total').plot.barh(y=to_plot, stacked=True)
    ax.set_ylabel('Early Voting Site Name')
    ax.set_xlabel('Total')
    ax.set_title(f'One-Stop Votes, {county} County, Grouped By Age Group')
    name = county.lower()
    print(f'assets/images/one-stop/county-age-totals/{name}.png')
    ax.get_figure().savefig(
        f'assets/images/one-stop/county-age-totals/{name}.png',
        bbox_inches='tight')

@click.command()
@click.option('-f', '--filename', type=str)
def main(filename):
    absentee = read_absentee_voter_file(filename)
    one_stop = absentee[absentee.ballot_req_type == 'ONE-STOP']
    for county, results in one_stop.groupby(by='county_desc'):
        plot_by_party(county, results)
        plot_by_race(county, results)
        plot_by_age_group(county, results)


if __name__ == '__main__':
    sys.exit(main())
