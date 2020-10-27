import pandas as pd

colors = {
    'Democratic': 'DeepSkyBlue',
    'Republican': 'Tomato',
    'Unaffiliated': 'DarkGray',
    'Other': 'mediumseagreen'
}


def read_absentee_voter_file(filename):
    date_cols = [
        'ballot_req_dt', 'ballot_rtn_dt', 'ballot_rtn_status', 'ballot_send_dt'
    ]
    absentee = pd.read_csv(filename, parse_dates=date_cols)
    age_groups = {
        pd.Interval(17, 25, closed='right'): '18 - 25',
        pd.Interval(25, 40, closed='right'): '26 - 40',
        pd.Interval(40, 65, closed='right'): '41 - 65',
        pd.Interval(65, 120, closed='right'): 'Over 65',
    }
    parties = {
        'DEM': 'Democrats',
        'UNA': 'Unaffiliated',
        'REP': 'Republicans',
        'LIB': 'Other (LIB-GRE-CST)',
        'GRE': 'Other (LIB-GRE-CST)',
        'CST': 'Other (LIB-GRE-CST)',
    }
    gender = {'M': 'Male', 'F': 'Female', 'U': 'Undesignated'}
    absentee['gender'] = absentee['gender'].map(gender)
    absentee['ballot_request_party'] = absentee['ballot_request_party'].map(
        parties)
    absentee['voter_party_code'] = absentee['voter_party_code'].map(parties)
    absentee['age_group'] \
      = pd.cut(absentee.age, bins=[17, 25, 40, 65, 120]).map(age_groups).astype(str)
    absentee['party'] = absentee['voter_party_code']
    return absentee


def summarize_absentee(absentee):
    all_submitted = absentee.groupby('voter_party_code').count().county_desc
    all_submitted['Total'] = all_submitted.sum()
    all_accepted = absentee[absentee.ballot_rtn_status == 'ACCEPTED'].groupby(
        'voter_party_code').count().county_desc
    all_accepted['Total'] = all_accepted.sum()
    all_returned = absentee[absentee.ballot_rtn_status != 'ACCEPTED'].groupby(
        'voter_party_code').count().county_desc
    all_returned['Total'] = all_returned.sum()
    return pd.DataFrame({
        'VBM Submitted': all_submitted,
        'VBM Accepted': all_accepted,
        'VBM Returned': all_returned
    }).T.round()


def plot_vm_counts(absentee, start_date='2020-02-25'):
    col_types = ['party_desc', 'race_desc', 'gender_desc', 'age_range']
    figure, axs = plt.subplots(2, 2)
    axs = [axs[0][0], axs[0][1], axs[1][0], axs[1][1]]
    ax_index = 0
    for col_type in col_types:
        for group in np.sort(absentee[col_type].unique()):
            grouped = absentee[absentee[col_type] == group].groupby(
                pd.Grouper(key='request_week_date', freq='W-SAT'))
            cumulative = grouped['group_count'].sum().cumsum()
            cumulative = cumulative[cumulative.index >= start_date]
            label = group.title()
            if col_type == 'party_desc':
                cumulative.plot(label=label,
                                color=colors.get(group.title()),
                                ax=axs[ax_index])
            else:
                cumulative.plot(label=label, ax=axs[ax_index])
        grouped = absentee.groupby(
            pd.Grouper(key='request_week_date', freq='W-SAT'))
        cumulative = grouped['group_count'].sum().cumsum()
        cumulative = cumulative[cumulative.index >= start_date]
        cumulative.plot(label='Total',
                        color='Black',
                        ax=axs[ax_index],
                        style='--')
        axs[ax_index].legend()
        axs[ax_index].set_xlabel('')
        ax_index += 1
    figure.suptitle(
        'Cumulative Absentee (VBM) Request Counts\nGrouped By Demographics, Party Affiliation (since 01/01/2020)',
        fontsize=14)
    return figure
