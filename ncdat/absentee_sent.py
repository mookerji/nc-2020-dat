
colors = {'Democratic': 'DeepSkyBlue', 'Republican': 'Tomato', 'Unaffiliated': 'DarkGray', 'Other': 'mediumseagreen'}

def plot_vm_counts(absentee, start_date='2020-02-25'):
    col_types = ['party_desc', 'race_desc', 'gender_desc', 'age_range']
    figure, axs = plt.subplots(2,2)
    axs = [axs[0][0], axs[0][1], axs[1][0], axs[1][1]]
    ax_index = 0
    for col_type in col_types:
        for group in np.sort(absentee[col_type].unique()):
            grouped = absentee[absentee[col_type] == group].groupby(pd.Grouper(key='request_week_date', freq='W-SAT'))
            cumulative = grouped['group_count'].sum().cumsum()
            cumulative = cumulative[cumulative.index >= start_date]
            label = group.title()
            if col_type == 'party_desc':
                cumulative.plot(label=label, color=colors.get(group.title()), ax=axs[ax_index])
            else:
                cumulative.plot(label=label, ax=axs[ax_index])
        grouped = absentee.groupby(pd.Grouper(key='request_week_date', freq='W-SAT'))
        cumulative = grouped['group_count'].sum().cumsum()
        cumulative = cumulative[cumulative.index >= start_date]
        cumulative.plot(label='Total', color='Black', ax=axs[ax_index], style='--')
        axs[ax_index].legend()
        axs[ax_index].set_xlabel('')
        ax_index += 1
    figure.suptitle('Cumulative Absentee (VBM) Request Counts\nGrouped By Demographics, Party Affiliation (since 01/01/2020)', fontsize=14)
    return figure
