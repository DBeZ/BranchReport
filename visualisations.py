#########################################
# Generate report visualization (graphs)
#########################################

import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import os

# Line plot of new, existing and pre-existing users since specified track opening
def single_track_opening(data_selected, name_selected):
    data_selected=data_selected[1:].reset_index(drop=True)
    data_selected.plot(title="Activity after "+name_selected+" track opening")
    plt.xticks(np.arange(0,len(data_selected), 1.0))
    plt.ylim(bottom=0)
    plt.xlabel("Weeks from track opening")
    plt.ylabel("Activity")

    plt.tight_layout()
    # plt.show(block=False)
    figure_name = "Activity comparison to same track opening last year"
    # print("Graph generated - %s" %figure_name)

    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    file_formate = 'png'
    plt.savefig(figure_name, bbox_inches='tight', format=file_formate)
    fig_dir=os.getcwd()
    os.chdir("..")
    plt.close()
    return figure_name+"."+file_formate, fig_dir


# Bar plots comparing a selected track opening and the closes one to it a year before.
# Produces three separate graphs (1) new, (2) existing (3)  pre-existing users
def last_year_compare(data_selected, name_selected, data_last_year, name_last_year):
    col_last_year = data_last_year.columns
    cols_selected = data_selected.columns

    # Remove first week
    data_selected=data_selected[1:]
    data_last_year = data_last_year[1:]

    # Create new dataframes for each count to plot easily
    a=data_last_year[col_last_year[0]].to_frame()
    a.columns = [str(name_last_year)]
    b=data_selected[cols_selected[0]].to_frame()
    b.columns=[str(name_selected)]
    df_all=pd.concat([a,b], ignore_index=False, axis=1)

    a=data_last_year[col_last_year[1]].to_frame()
    a.columns = [str(name_last_year)]
    b=data_selected[cols_selected[1]].to_frame()
    b.columns=[str(name_selected)]
    df_new=pd.concat([a,b], ignore_index=False, axis=1)

    a=data_last_year[col_last_year[2]].to_frame()
    a.columns = [str(name_last_year)]
    b=data_selected[cols_selected[2]].to_frame()
    b.columns=[str(name_selected)]
    df_existing=pd.concat([a,b], ignore_index=False, axis=1)

    # Create figure
    graph_no = data_selected.shape[1]
    fig, ax = plt.subplots(nrows=graph_no , ncols=1,constrained_layout=True)

    figure_name = "Activity comparison to track opening last year"
    fig.suptitle(figure_name, fontsize=16)

    ax_list = fig.axes
    # Uncomment to set all figure to same y axes. 1 of 2
    # min_y = 0
    # max_y = max([data_selected.max().max(),data_last_year.max().max()])*1.25

    for n, one_axis in enumerate(ax_list):
        # Uncomment to set all figure to same y axes. 2 of 2
        # Set all figure to same y axes
        # one_axis.set_ylim(min_y, max_y)
        one_axis.axes.set_ylabel("Activity")
        one_axis.axes.get_xaxis().set_visible(True)

        # Plotting
        if n==0:
            min_y = 0
            max_y = df_all.max().max()*1.25
            one_axis.set_ylim(min_y, max_y)
            one_axis.set_title("Total (new + existing)")
            df_all.plot(kind='bar', ax=one_axis)
            # Move legend to left outside of graph and remove box around it
            patches, labels = one_axis.get_legend_handles_labels()
            plt.setp(one_axis.get_xticklabels(), rotation=0)
            one_axis.legend(patches, labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        if n==1:
            min_y = 0
            max_y = df_new.max().max()*1.25
            one_axis.set_ylim(min_y, max_y)
            one_axis.set_title("New from track opening")
            df_new.plot(kind='bar', ax=one_axis, legend=False)
            plt.setp(one_axis.get_xticklabels(), rotation=0)
        if n==2:
            min_y = 0
            max_y = df_existing.max().max()*1.25
            one_axis.set_ylim(min_y, max_y)
            one_axis.set_title("Pre-existing participants")
            df_existing.plot(kind='bar', ax=one_axis, legend=False)
            plt.setp(one_axis.get_xticklabels(), rotation=0)
            one_axis.axes.set_xlabel("Weeks from track opening")

        # Show value on each bar
        for p in one_axis.patches:
            one_axis.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    # plt.tight_layout()
    # plt.show(block=False)

    # print("Graph generated - %s" %figure_name)

    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    file_formate = 'png'
    plt.savefig(figure_name, bbox_inches='tight', format=file_formate)
    fig_dir = os.getcwd()
    os.chdir("..")
    plt.close()
    return figure_name+"."+file_formate, fig_dir


# Heatmap of active users in each branch.
# Colors normalized to min and max value for each branch in the given daterange
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

    # plt.show(block=False)
    fig = plt.gcf()
    figure_name = "Activity by branch Heatmap"
    # print("Graph generated - %s" %figure_name)

    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    file_formate = 'png'
    plt.savefig(figure_name, bbox_inches='tight', format=file_formate)
    fig_dir = os.getcwd()
    os.chdir("..")
    plt.close()
    return figure_name+"."+file_formate, fig_dir

# Stacked brachart of staff and participants in daterange
def populus_and_staff(dataframe):
    plt.figure()
    ax = plt.gca()

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
    # plt.show(block=False)
    fig = plt.gcf()
    figure_name = "Activity Stacked Bar Plot (participants, staff)"
    # print("Graph generated - %s" %figure_name)

    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    file_formate = 'png'
    plt.savefig(figure_name, bbox_inches='tight', format=file_formate)
    fig_dir = os.getcwd()
    os.chdir("..")
    plt.close()
    return figure_name+"."+file_formate, fig_dir

# Barchart of activity in daterange by track opening
# Produces seperate figure for each track opening
def activity_by_registration(dataframe):
    # plt.figure()
    ax = plt.gca()

    # Get max and min values from all branches to be used in all graphs
    min_y = dataframe.min().min()
    max_y = dataframe.max().max()

    # Transpose to plot with pandas built in function
    dataframe = dataframe.transpose()
    series_no = dataframe.shape[1]
    dataframe.plot(kind='bar',subplots=True, layout=(series_no, 1), ax=ax, sharex=True, legend=False)
    # TODO: THis build in dataframe plot function generates a warning.
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

        if one_axis is ax_list[-1]:
            one_axis.axes.get_xaxis().set_visible(True)
            plt.setp(one_axis.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    plt.tight_layout()
    # plt.show(block=False)
    fig = plt.gcf()
    figure_name = "Activity by registration Bar Plot"
    # print("Graph generated - %s" %figure_name)

    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    file_formate='png'
    plt.savefig(figure_name, bbox_inches='tight', format=file_formate)
    fig_dir = os.getcwd()
    os.chdir("..")
    plt.close()
    return figure_name+"."+file_formate, fig_dir
