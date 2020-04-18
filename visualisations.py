import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import math
import numpy as np
import pandas as pd


def branch_activity_heatmap(dataframe):
    plt.figure()
    ax = plt.gca()

    labels = dataframe.to_numpy()
    dataframe_row = dataframe.div(dataframe.max(axis=1), axis=0)
    sns.heatmap(dataframe_row, cmap="coolwarm_r", yticklabels=True, linewidths=.5, robust=True, annot=labels, fmt='',
                annot_kws={'size': 8})  # cbar_kws={'orientation': 'horizontal'}

    # Set plot properties
    ax.set_title('Presence relative to max in each branch')
    ax.figure.set_size_inches((12, 10))
    ax.tick_params(labelsize=8)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right",
             rotation_mode="anchor")
    plt.xlabel("")
    plt.ylabel('')
    plt.tight_layout()

    # Colorbar properties
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, .25, .5, .75, 1])
    cbar.set_ticklabels(['Min', '25%', '50%', '75%', 'Max'])

    plt.show(block=False)
    print("Activity by branch Heatmap Done")


def populus_and_staff(dataframe):
    plt.figure()
    ax = plt.gca()

    # Reverse labels to show in Hebrew
    # If same method is used for columns graph generation fails with error: "Backend Qt5Agg is interactive backend. Turning interactive mode on."
    index_labels = dataframe.index
    name_dict = {}
    for index_name in index_labels:
        index_name_new = index_name[::-1]
        name_dict[index_name] = index_name_new

    dataframe.rename(index=name_dict, inplace=True)

    # Transpose to plot with pandas built in function
    dataframe_tf = dataframe.transpose()

    column_labels = dataframe_tf.columns
    dataframe_tf[[column_labels[0], column_labels[1]]].plot(kind='bar', stacked=True, ax=ax)

    # Plot properties
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.xlabel("Weeks")
    plt.ylabel('Activity')

    plt.tight_layout()
    plt.show(block=False)
    print("Activity Stacked Bar Plot (participants, staff) Done")


def activity_by_registration(dataframe):
    plt.figure()
    ax = plt.gca()
    # In case error about setting backend appears
    # matplotlib.use('qt5agg')
    # matplotlib.get_backend()

    # Get max and min values from all branches to be used in all graphs
    min_y = dataframe.min().min()
    max_y = dataframe.max().max()

    # Transpose to plot with pandas built in function
    dataframe = dataframe.transpose()
    series_no = dataframe.shape[1]
    dataframe.plot.bar(subplots=True, layout=(series_no, 1), ax=ax, sharex=True, legend=False)

    # Adjust each plot in figure
    fig = plt.gcf()
    ax_list = fig.axes

    for one_axis in ax_list:
        one_axis.set_ylim(min_y, max_y)

        # Move legend to left outside of graph and remove box around it
        patches, labels = one_axis.get_legend_handles_labels()
        one_axis.legend(patches, labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

        # Remove x axis labels from all graphs but bottom one
        one_axis.axes.get_xaxis().set_visible(False)
        one_axis.set_title("")
        if one_axis is ax_list[0]:
            one_axis.set_title("Activity each week by registration date (participants+staff)")

        if one_axis is ax_list[math.floor(len(ax_list) / 2)]:
            one_axis.axes.set_ylabel("Activity")
        # one_axis.axes.get_xaxis().set_ticks([])
        if one_axis is ax_list[-1]:
            one_axis.axes.get_xaxis().set_visible(True)
            plt.setp(one_axis.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # for k in range(series_no):
    #     dataframe.iloc[k].plot.bar(ax=axes[k], rot=45)

    plt.tight_layout()
    plt.show(block=False)
    print("Activity by registration Bar Plot Done")
