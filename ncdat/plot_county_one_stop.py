import sys

from palettable.colorbrewer.sequential import OrRd_9
from matplotlib.colors import ListedColormap, to_hex

import click
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from absentee_sent import read_absentee_voter_file


def plot_by_party(county,
                  results,
                  horizontal=True,
                  groupby='site_name',
                  ylabel='Early Voting Site Name'):
    data = results.groupby(
        by=[groupby, 'voter_party_code']).count().voter_reg_num.unstack()
    data['total'] = data.sum(axis=1)
    cols = ['Democrats', 'Republicans', 'Unaffiliated', 'Other (LIB-GRE-CST)']
    colors = ['deepskyblue', 'tomato', 'slategray', 'green']
    if horizontal:
        ax = data.sort_values(by='total').plot.barh(y=cols,
                                                    stacked=True,
                                                    color=colors)
    else:
        ax = data.sort_values(by='total').plot.bar(y=cols,
                                                   stacked=True,
                                                   color=colors)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Total')
    ax.set_title(f'One-Stop Votes, {county} County, Grouped by Party')
    return ax.get_figure()


def plot_by_race(county,
                 results,
                 horizontal=True,
                 groupby='site_name',
                 ylabel='Early Voting Site Name'):
    data = results.groupby(
        by=[groupby, 'race']).count().voter_reg_num.unstack()
    data['total'] = data.sum(axis=1)
    if horizontal:
        ax = data.sort_values(by='total').plot.barh(y=results.race.unique(),
                                                stacked=True)
    else:
        ax = data.sort_values(by='total').plot.bar(y=results.race.unique(),
                                                stacked=True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Total')
    #plt.legend(prop={'size': 6})
    ax.set_title(f'One-Stop Votes, {county} County, Grouped By Race')
    return ax.get_figure()


def plot_by_age_group(county,
                      results,
                      horizontal=True,
                      groupby='site_name',
                      ylabel='Early Voting Site Name'):
    data = results.groupby(
        by=[groupby, 'age_group']).count().voter_reg_num.unstack()

    to_plot = data.columns
    # TODO: remove if we coerce to strings at parse time
    #data.columns = data.columns.astype(str)
    data['total'] = data.sum(axis=1)
    if horizontal:
        ax = data.sort_values(by='total').plot.barh(y=to_plot, stacked=True)
    else:
        ax = data.sort_values(by='total').plot.bar(y=to_plot, stacked=True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Total')
    ax.set_title(f'One-Stop Votes, {county} County, Grouped By Age Group')
    return ax.get_figure()


def plot_one_stop_counts_by_week(county, results):
    figure, axs = plt.subplots(2, 2)
    axs = [axs[0][0], axs[0][1], axs[1][0], axs[1][1]]
    ax_index = 0
    results_ = results[(results.ballot_rtn_dt >= '2020-10-15')
                       & (results.ballot_rtn_dt <= pd.datetime.now())]
    results_ = results_[results_.age_group != np.isnan]
    col_types = ['party', 'race', 'gender', 'age_group']
    for col_type in col_types:
        daily = results_.groupby(pd.Grouper(freq='1D', key='ballot_rtn_dt'))
        summed = daily.apply(lambda v: v.groupby(col_type)['ballot_rtn_dt'].count())
        if isinstance(summed.index, pd.MultiIndex):
            summed = summed.unstack()
        summed = summed.resample('1D').asfreq().fillna(0)
        summed.plot.bar(stacked=True, ax=axs[ax_index])
        axs[ax_index].legend()
        axs[ax_index].set_xlabel('')
        if ax_index < 2:
            axs[ax_index].set_xticks([])
        ax_index += 1
    figure.suptitle(
        f'One-Stop Votes (All Statuses), {county} County\nGrouped By Demographics, Party Affiliation (since 10/15/2020)'
    )
    return figure


def plot_state(results):
    county = 'Every'
    groupby = 'county_desc'
    ylabel = 'County'
    horizontal=False
    figure = plot_by_party(county, results, horizontal, groupby, ylabel)
    print(f'assets/images/one-stop/county-party-totals.png')
    figure.savefig(f'assets/images/one-stop/county-party-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_by_race(county, results, horizontal, groupby, ylabel)
    print(f'assets/images/one-stop/county-race-totals.png')
    figure.savefig(f'assets/images/one-stop/county-race-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_by_age_group(county, results, horizontal, groupby, ylabel)
    print(f'assets/images/one-stop/county-age-totals.png')
    figure.savefig(f'assets/images/one-stop/county-age-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_one_stop_counts_by_week(county, results)
    print(f'assets/images/one-stop/per-week-totals.png')
    figure.savefig(f'assets/images/one-stop/per-week-totals.png',
                   bbox_inches='tight')
    plt.close(figure)


@click.command()
@click.option('-f', '--filename', type=str)
def main(filename):
    absentee = read_absentee_voter_file(filename)
    one_stop = absentee[absentee.ballot_req_type == 'ONE-STOP']
    plt.rcParams["figure.figsize"] = [16, 10]
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16

    plot_state(one_stop)

    for county, results in one_stop.groupby(by='county_desc'):
        name = county.lower()

        figure = plot_by_party(county, results)
        print(f'assets/images/one-stop/county-party-totals/{name}.png')
        figure.savefig(
            f'assets/images/one-stop/county-party-totals/{name}.png',
            bbox_inches='tight')
        plt.close(figure)

        figure = plot_by_race(county, results)
        print(f'assets/images/one-stop/county-race-totals/{name}.png')
        figure.savefig(f'assets/images/one-stop/county-race-totals/{name}.png',
                       bbox_inches='tight')
        plt.close(figure)

        figure = plot_by_age_group(county, results)
        print(f'assets/images/one-stop/county-age-totals/{name}.png')
        figure.savefig(f'assets/images/one-stop/county-age-totals/{name}.png',
                       bbox_inches='tight')
        plt.close(figure)

        figure = plot_one_stop_counts_by_week(county, results)
        print(f'assets/images/one-stop/per-week-totals/{name}.png')
        figure.savefig(f'assets/images/one-stop/per-week-totals/{name}.png',
                       bbox_inches='tight')
        plt.close(figure)


if __name__ == '__main__':
    sys.exit(main())
