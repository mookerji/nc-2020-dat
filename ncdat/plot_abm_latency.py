import sys

from palettable.colorbrewer.sequential import OrRd_9
from matplotlib.colors import ListedColormap, to_hex

import click
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from absentee_sent import read_absentee_voter_file


def plot_request_send_latency(county, results,):
    ax = results.boxplot(column='ballot_send_days', by='ballot_req_dt', grid=False, rot=90)
    ax.set_xlabel('Ballot Request Date')
    ax.set_ylabel('Days To Send Ballot')
    ax.set_title(f'Days to Send ABM Ballot (Ballot Request to Ballot Send), {county} County')
    return ax.get_figure()


@click.command()
@click.option('-f', '--filename', type=str)
def main(filename):
    absentee = read_absentee_voter_file(filename)
    abm = absentee[(absentee.ballot_req_type == 'MAIL') & (absentee['ballot_req_dt'] >= '2020-09-04')]
    abm['ballot_send_days'] = (abm['ballot_send_dt'] - abm['ballot_req_dt']).dt.days

    plt.rcParams["figure.figsize"] = [16, 10]
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16

    for county, results in abm.groupby(by='county_desc'):
        name = county.lower()
        figure = plot_request_send_latency(county, results)
        print(f'assets/images/abm-latency/request-to-mail/{name}.png')
        figure.savefig(
            f'assets/images/abm-latency/request-to-mail/{name}.png',
            bbox_inches='tight')
        plt.close(figure)


if __name__ == '__main__':
    sys.exit(main())
