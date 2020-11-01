import sys

import click
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from absentee_sent import read_absentee_voter_file


def plot_accepted_demographics_by_week(county, results):
    figure, axs = plt.subplots(2, 2)
    axs = [axs[0][0], axs[0][1], axs[1][0], axs[1][1]]
    ax_index = 0
    results_ = results[results.age_group != np.isnan]
    col_types = ['party', 'race', 'gender', 'age_group']
    for col_type in col_types:
        ax = axs[ax_index]
        counted = results.groupby(['ballot_rtn_dt',
                                   col_type]).voter_reg_num.count().unstack()
        counted = counted.resample('1D').asfreq().fillna(0)
        if col_type == 'party':
            colors = ['deepskyblue', 'slategray', 'tomato', 'green']
            counted.plot.bar(stacked=True, ax=ax, color=colors)
        else:
            counted.plot.bar(stacked=True, ax=ax)
        ax.legend()
        ax.set_xlabel('')
        if ax_index < 2:
            ax.set_xticks([])
        else:
            n = 5
            ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            ax.xaxis.set_ticks(ticks[::n])
            ax.xaxis.set_ticklabels(ticklabels[::n])
        ax_index += 1
    figure.suptitle(
        f'Weekly Accepted Votes, {county} County\nGrouped By Demographics, Party Affiliation (since 09/01/2020)'
    )
    return figure


def plot_accepted_demographics_cumulative(county, results):
    figure, axs = plt.subplots(2, 2)
    axs = [axs[0][0], axs[0][1], axs[1][0], axs[1][1]]
    ax_index = 0
    results_ = results[results.age_group != np.isnan]
    col_types = ['party', 'race', 'gender', 'age_group']
    for col_type in col_types:
        ax = axs[ax_index]
        counted = results.groupby(['ballot_rtn_dt',
                                   col_type]).voter_reg_num.count().unstack()
        counted = counted.resample('1D').asfreq().fillna(0)
        sum_ = counted.cumsum()
        sum_['total'] = sum_.sum(axis=1)
        if col_type == 'party':
            colors = ['deepskyblue', 'slategray', 'tomato', 'green', 'mediumorchid']
            sum_.plot(ax=ax, color=colors)
        else:
            sum_.plot(ax=ax)
        ax.legend()
        if ax_index < 2:
            ax.set_xticks([])
            ax.set_xlabel('')
        else:
            ax.set_xlabel('Ballot Return Date (day of month)')
            n = 5
            ticks = ax.xaxis.get_ticklocs()
            ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
            ax.xaxis.set_ticks(ticks[::n])
            ax.xaxis.set_ticklabels(ticklabels[::n])
        ax_index += 1
    figure.suptitle(
        f'Cumulative Accepted Votes, {county} County\nGrouped By Demographics, Party Affiliation (since 09/01/2020)'
    )
    return figure


def plot_accepted_types_by_week(county, results):
    figure, axs = plt.subplots(1, 2, figsize=(18, 8))
    axs = [axs[0], axs[1]]
    counted = results.groupby(['ballot_rtn_dt', 'ballot_req_type'
                               ]).voter_reg_num.count().unstack()
    counted = counted.resample('1D').asfreq().fillna(0)
    # Plot weekly numbers
    counted.plot.bar(stacked=True, ax=axs[0])
    axs[0].legend()
    axs[0].set_xlabel('Date')
    axs[0].set_title('Weekly')
    n = 5
    ticks = axs[0].xaxis.get_ticklocs()
    ticklabels = [l.get_text() for l in axs[0].xaxis.get_ticklabels()]
    axs[0].xaxis.set_ticks(ticks[::n])
    axs[0].xaxis.set_ticklabels(ticklabels[::n])
    # Plot total cumluative numbers
    sum_ = counted.cumsum()
    sum_['total'] = sum_.sum(axis=1)
    sum_.plot(ax=axs[1])
    axs[1].legend()
    axs[1].set_xlabel('Date')
    axs[1].set_title('Cumulative')
    figure.suptitle(
        f'Accepted Absentee Votes, {county} County\nGrouped by Ballot Request Type (MAIL, ONE-STOP) ,since 09/01/2020'
    )
    return figure


def plot_accepted_by_county_party(results):
    counted = results.groupby(['county_desc',
                               'party']).voter_reg_num.count().unstack()
    to_plot = counted.columns
    counted['total'] = counted.sum(axis=1)
    colors = ['deepskyblue', 'slategray', 'tomato', 'green']
    ax = counted.sort_values(by='total').plot.bar(y=to_plot,
                                                  stacked=True,
                                                  color=colors)
    ax.set_ylabel('Total Votes Cast')
    ax.set_xlabel('County')
    ax.set_title(f'Total Votes Cast, Grouped By County')
    return ax.get_figure()


def plot_state(results):
    county = 'Every'
    figure = plot_accepted_types_by_week(county, results)
    print(f'assets/images/accepted/type-per-week-totals.png')
    figure.savefig(f'assets/images/accepted/type-per-week-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_accepted_demographics_by_week(county, results)
    print(f'assets/images/accepted/demographic-per-week-totals.png')
    figure.savefig(f'assets/images/accepted/demographic-per-week-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_accepted_demographics_cumulative(county, results)
    print(f'assets/images/accepted/demographic-cumulative-totals.png')
    figure.savefig(f'assets/images/accepted/demographic-cumulative-totals.png',
                   bbox_inches='tight')
    plt.close(figure)

    figure = plot_accepted_by_county_party(results)
    print(f'assets/images/accepted/cumulative-by-county-party.png')
    figure.savefig(f'assets/images/accepted/cumulative-by-county-party.png',
                   bbox_inches='tight')
    plt.close(figure)


@click.command()
@click.option('-f', '--filename', type=str)
def main(filename):
    absentee = read_absentee_voter_file(filename)
    accepted = absentee[absentee.ballot_rtn_status == 'ACCEPTED']
    accepted = accepted[(accepted.ballot_rtn_dt >= '2020-09-01')
                        & (accepted.ballot_rtn_dt <= pd.datetime.now())]
    plt.rcParams["figure.figsize"] = [16, 10]
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16

    plot_state(accepted)

    for county, results in accepted.groupby(by='county_desc'):
        name = county.lower()
        figure = plot_accepted_types_by_week(county, results)
        print(f'assets/images/accepted/type-per-week-totals/{name}.png')
        figure.savefig(
            f'assets/images/accepted/type-per-week-totals/{name}.png',
            bbox_inches='tight')
        plt.close(figure)

        figure = plot_accepted_demographics_by_week(county, results)
        print(f'assets/images/accepted/demographic-per-week-totals/{name}.png')
        figure.savefig(
            f'assets/images/accepted/demographic-per-week-totals/{name}.png',
            bbox_inches='tight')
        plt.close(figure)

        figure = plot_accepted_demographics_cumulative(county, results)
        print(
            f'assets/images/accepted/demographic-cumulative-totals/{name}.png')
        figure.savefig(
            f'assets/images/accepted/demographic-cumulative-totals/{name}.png',
            bbox_inches='tight')
        plt.close(figure)


if __name__ == '__main__':
    sys.exit(main())
