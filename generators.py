##########################################################################
# Generates the reports by calling analysis functions and creating graphs
##########################################################################
# Returns dataframes and figures so they can be exported

import pandas as pd
from input_converters import ask_date_range_month_year, ask_num
from weekly_calender import week_date_start_end, track_opening_start_end
from retrieve_data_by_activity_date import retrieve_data_by_activity_date
from weekly_analysis import column_converter, remove_user_duplicates, populus_counter_by_weeks, add_role, activity_by_track_opening_counter, activity_by_branch_counter, activity_this_track_opening, activity_this_track_opening_by_branch
from user_specific_extractor import login_sql
import datetime as dt
from calendar import monthrange
from dateutil import relativedelta

import numpy as np
import visualisations

## Generates report for single track opening
def generator_single_track_opening(user_sql_login_dict):
    ## Used to replace SQL query if needed
    # fields = {
    #     "user": "userID",  # user connect ID
    #     "registration": "dateJoined",  # date registered to sheconnect
    #     "lesson_date": "lessonDate",  # date lesson was taken
    #     "graduation_threshold": "80precent",  # lesson no which marks 80% of course milestone
    #     "track_name": "trackName",  # short name of the track
    #     "lesson_no": "lessonNo",  # lesson number
    #     "branch": "branchName",  # short name of the branch
    #     "branch_type": "branchType",  # branch type
    #     "branch_active": "active"  # 0 if branch is no longer active
    # }
    #
    # field_datatpypes = {
    #      "user": "int",  # user connect ID
    #      "registration": "datetime",  # date registered to sheconnect
    #      "lesson_date": "datetime",  # date lesson was taken
    #      "graduation_threshold": "int",  # lesson no which marks 80% of course milestone
    #      "track_name": "string",  # short name of the track
    #      "lesson_no": "int",  # lesson number
    #      "branch": "string",  # short name of the branch
    #      "branch_type": "string",  # branch type
    #      "branch_active": "binary"  # 0 if branch is no longer active
    # }
    # data_query_selected = pd.read_csv("selected.csv")
    # fields_dict_selected=fields
    # field_datatypes_dict_selected=field_datatpypes
    ## End of SQL replacment

    print("*** Compare two track openings ***")
    print("Enter track opening:")
    min_date_selected, max_date_selected = ask_date_range_month_year()
    # TODO correct input so only one month is accepted input
    # TODO if input is not a track opening display possible track openings around it
    print("How many weeks forward would you like to examine?")
    weeks_to_analyze=ask_num()

    # Get track opening dates
    reg_start_selected, reg_end_selected=track_opening_start_end(min_date_selected, max_date_selected)
    # Get week dates
    start_week_dates_selected, end_week_dates_selected = week_date_start_end(reg_end_selected[0], reg_end_selected[0]+relativedelta.relativedelta(weeks=weeks_to_analyze))

    # # Retrieve data from database for week range in both years
    data_query_selected, fields_dict_selected, field_datatypes_dict_selected= retrieve_data_by_activity_date(sql_details_file_name="sql_login_monster.txt", user_specific_dir=user_sql_login_dict["certificates_folder"], dateStart=min(start_week_dates_selected), dateEnd=max(end_week_dates_selected))


    # Remove user duplicates and convert columns
    data_query_selected_no_duplicates = remove_user_duplicates(data_query_selected, fields_dict_selected["user"], fields_dict_selected["lesson_date"])
    data_query_selected_converted = column_converter(data_query_selected_no_duplicates, fields_dict_selected, field_datatypes_dict_selected)

    activity_by_track_opening_selected, selected_reg_name = activity_this_track_opening(data=data_query_selected_converted,
                                                                               registration_col=fields_dict_selected["registration"],
                                                                               activity_col=fields_dict_selected["lesson_date"],
                                                                               reg_start=reg_start_selected,
                                                                               reg_end=reg_end_selected,
                                                                               week_start_list=start_week_dates_selected,
                                                                               week_end_list=end_week_dates_selected)

    activity_by_track_opening_selected_by_branch, _=activity_this_track_opening_by_branch(data=data_query_selected_converted,
                                                                            registration_col=fields_dict_selected["registration"],
                                                                            activity_col=fields_dict_selected["lesson_date"],
                                                                            branch_col=fields_dict_selected["branch"],
                                                                            reg_start=reg_start_selected,
                                                                            reg_end=reg_end_selected,
                                                                            week_start_list=start_week_dates_selected,
                                                                            week_end_list=end_week_dates_selected)


    figure1, fig_dir=visualisations.single_track_opening(data_selected=activity_by_track_opening_selected, name_selected=selected_reg_name)
    figure_names=[figure1]
    return activity_by_track_opening_selected_by_branch, figure_names, selected_reg_name, fig_dir


## Generates report comaring a track opening to the one before
def generator_compare_last_year_report(user_sql_login_dict):
    ## Used to replace SQL query if needed
    # fields = {  # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
    #     "user": "userID",  # user connect ID
    #     "registration": "dateJoined",  # date registered to sheconnect
    #     "lesson_date": "lessonDate",  # date lesson was taken
    #     "graduation_threshold": "80precent",  # lesson no which marks 80% of course milestone
    #     "track_name": "trackName",  # short name of the track
    #     "lesson_no": "lessonNo",  # lesson number
    #     "branch": "branchName",  # short name of the branch
    #     "branch_type": "branchType",  # branch type
    #     "branch_active": "active"  # 0 if branch is no longer active
    # }
    #
    # field_datatpypes = {
    #     "user": "int",  # user connect ID
    #     "registration": "datetime",  # date registered to sheconnect
    #     "lesson_date": "datetime",  # date lesson was taken
    #     "graduation_threshold": "int",  # lesson no which marks 80% of course milestone
    #     "track_name": "string",  # short name of the track
    #     "lesson_no": "int",  # lesson number
    #     "branch": "string",  # short name of the branch
    #     "branch_type": "string",  # branch type
    #     "branch_active": "binary"  # 0 if branch is no longer active
    # }
    # data_query_selected = pd.read_csv("selected.csv")
    # data_query_last_year = pd.read_csv("lastyear.csv")
    # fields_dict_selected=fields
    # fields_dict_last_year=fields
    # field_datatpypes_dict_selected=field_datatpypes
    # field_datatpypes_last_year=field_datatpypes
    ## End of SQL replacment

    print("*** Compare two track openings ***")
    print("Enter track opening or track openings to compare to last year's")
    min_date_selected, max_date_selected = ask_date_range_month_year()
    # TODO: correct input so only one month is accepted input
    # TODO: if input is not a track opening display possible track openings around it
    print("How many weeks forward would you like to examine?")
    weeks_to_analyze=ask_num()

    # Get track opening to compare last year to
    reg_start_selected, reg_end_selected=track_opening_start_end(min_date_selected, max_date_selected)
    # Get analogous track openings from last year
    min_date_last_year = min_date_selected - relativedelta.relativedelta(years=1)
    max_date_last_year = dt.date(min_date_last_year.year,  min_date_last_year.month,monthrange(min_date_last_year.year, min_date_last_year.month)[1])
    reg_start_last_year, reg_end_last_year = track_opening_start_end(min_date_last_year, max_date_last_year)

    # Get week dates for analysis in selected year and last year
    start_week_dates_selected, end_week_dates_selected = week_date_start_end(reg_end_selected[0], reg_end_selected[0]+relativedelta.relativedelta(weeks=weeks_to_analyze))
    start_week_dates_last_year, end_week_dates_last_year=week_date_start_end(reg_end_last_year[0], reg_end_last_year[0]+relativedelta.relativedelta(weeks=weeks_to_analyze))

    # # Retrieve data from database for week range in both years
    data_query_selected, fields_dict_selected, field_datatpypes_dict_selected= retrieve_data_by_activity_date(sql_details_file_name="sql_login_monster.txt", user_specific_dir=user_sql_login_dict["certificates_folder"], dateStart=min(start_week_dates_selected), dateEnd=max(end_week_dates_selected))
    data_query_last_year, fields_dict_last_year, field_datatpypes_last_year=retrieve_data_by_activity_date(sql_details_file_name="sql_login_monster.txt", user_specific_dir=user_sql_login_dict["certificates_folder"], dateStart=min(start_week_dates_last_year), dateEnd=max(end_week_dates_last_year))

    # Remove user duplicates and convert columns for both datasets
    data_query_selected_no_duplicates = remove_user_duplicates(data_query_selected, fields_dict_selected["user"], fields_dict_selected["lesson_date"])
    data_query_selected_converted = column_converter(data_query_selected_no_duplicates, fields_dict_selected, field_datatpypes_dict_selected)

    data_query_last_year_no_duplicates = remove_user_duplicates(data_query_last_year, fields_dict_last_year["user"], fields_dict_last_year["lesson_date"])
    data_query_last_year_converted = column_converter(data_query_last_year_no_duplicates, fields_dict_last_year, field_datatpypes_last_year)

    # Add roles
    data_selected_with_roles, role_dict, role_type_dict=add_role(data=data_query_selected_converted,sql_filename="sql_login_shecodes_shecodes.txt", user_specific_dir=user_google_login_dict["certificates_folder"])
    fields_dict_selected.update(role_dict)
    field_datatpypes_dict_selected.update(role_type_dict)

    data_last_year_with_roles, role_dict, role_type_dict=add_role(data=data_query_selected_converted,sql_filename="sql_login_shecodes_shecodes.txt", user_specific_dir=user_google_login_dict["certificates_folder"])
    fields_dict_last_year.update(role_dict)
    field_datatpypes_last_year.update(role_type_dict)

    activity_by_track_opening_selected, selected_reg_name = activity_this_track_opening(data=data_query_selected_converted,
                                                                                        registration_col=fields_dict_selected["registration"],
                                                                                        activity_col=fields_dict_selected["lesson_date"],
                                                                                        reg_start=reg_start_selected,
                                                                                        reg_end=reg_end_selected,
                                                                                        week_start_list=start_week_dates_selected,
                                                                                        week_end_list=end_week_dates_selected)

    activity_by_track_opening_last_year, last_year_reg_name = activity_this_track_opening(data=data_query_last_year_converted,
                                                                                          registration_col=fields_dict_last_year["registration"],
                                                                                          activity_col=fields_dict_last_year["lesson_date"],
                                                                                          reg_start=reg_start_last_year,
                                                                                          reg_end=reg_end_last_year,
                                                                                          week_start_list=start_week_dates_last_year,
                                                                                          week_end_list=end_week_dates_last_year)

    figure_name1, fig_dir = visualisations.last_year_compare(data_selected=activity_by_track_opening_selected,
                                     name_selected=selected_reg_name,
                                     data_last_year=activity_by_track_opening_last_year,
                                     name_last_year=last_year_reg_name)

    figure_names = [figure_name1]
    return figure_names, fig_dir


## Generates attendance tab in weekly report
def generator_weekly_report(user_google_login_dict):
    ## Used to replace SQL query if needed
    # fields = {
    #     "user": "userID",  # user connect ID
    #     "registration": "dateJoined",  # date registered to sheconnect
    #     "lesson_date": "lessonDate",  # date lesson was taken
    #     "graduation_threshold": "80precent",  # lesson no which marks 80% of course milestone
    #     "track_name": "trackName",  # short name of the track
    #     "lesson_no": "lessonNo",  # lesson number
    #     "branch": "branchName",  # short name of the branch
    #     "branch_type": "branchType",  # branch type
    #     "branch_active": "active"  # 0 if branch is no longer active
    # }
    #
    # field_data_types = {
    #     "user": "int",  # user connect ID
    #     "registration": "datetime",  # date registered to sheconnect
    #     "lesson_date": "datetime",  # date lesson was taken
    #     "graduation_threshold": "int",  # lesson no which marks 80% of course milestone
    #     "track_name": "string",  # short name of the track
    #     "lesson_no": "int",  # lesson number
    #     "branch": "string",  # short name of the branch
    #     "branch_type": "string",  # branch type
    #     "branch_active": "binary"  # 0 if branch is no longer active
    # }
    # data_query_orig = pd.read_csv("sql_data.csv")
    ## End of SQL replacment

    print("*** Weekly report generator ***")
    print("Enter range of weeks in which to analyze activity")
    [min_date_weeks, max_date_weeks]=ask_date_range_month_year()
    print("Enter registration range for sub-classification")
    [min_date_registration, max_date_registration]=ask_date_range_month_year()
    # TODO correct input so only one month is accepted input
    # TODO if input is not a track opening display possible track openings around it
    min_date_registration = dt.datetime(2018, 1, 1)
    min_date_weeks = dt.datetime(2020, 1, 1)
    max_date_registration = dt.datetime(2020, 4, 1)
    max_date_weeks = dt.datetime(2020, 4, 4)
    [week_begin_list, week_end_list] = week_date_start_end(min_date_weeks, max_date_weeks)
    [reg_start_dates, reg_end_dates] = track_opening_start_end(min_date_registration, max_date_registration)

    # Calling the analysis functions
    data_query_orig, fields, field_data_types=retrieve_data_by_activity_date(sql_details_file_name="sql_login_monster.txt", user_specific_dir=user_google_login_dict["certificates_folder"], dateStart=min(week_begin_list), dateEnd=max(week_end_list))
    data_no_duplicates = remove_user_duplicates(data_query_orig, fields["user"], fields["lesson_date"])
    # Do not use groupby. Using groupby
    # data_query.groupby([fields["lesson_date"], fields["registration"]]).count()
    # eliminates the other data used for sub-classificaitons
    data_converted_partial = column_converter(data_no_duplicates, fields, field_data_types)

    data_with_roles, role_dict, role_type_dict=add_role(data=data_converted_partial,sql_filename="sql_login_shecodes_shecodes.txt", user_specific_dir=user_google_login_dict["certificates_folder"])
    fields.update(role_dict)
    field_data_types.update(role_type_dict)

    # The following function loop on week dates
    populus_by_weeks = populus_counter_by_weeks(data=data_with_roles, staff_col=role_dict["team"],particip_col=role_dict["particip"],
                                                activity_col=fields["lesson_date"], week_start=week_begin_list,
                                                week_end=week_end_list)

    activity_by_branch = activity_by_branch_counter(data=data_with_roles, branch_col=fields["branch"],
                                                    activity_col=fields["lesson_date"], week_start=week_begin_list,
                                                    week_end=week_end_list)

    # The following function loops on week dates and registration date
    activity_by_track_opening = activity_by_track_opening_counter(data=data_with_roles,
                                                                  registration_col=fields["registration"],
                                                                  activity_col=fields["lesson_date"],
                                                                  reg_start_date_list=reg_start_dates,
                                                                  reg_end_date_list=reg_end_dates,
                                                                  week_start=week_begin_list,
                                                                  week_end=week_end_list)

    print("Analysis Done")

    # Output visualizations
    figure_name1, _ = visualisations.populus_and_staff(populus_by_weeks)
    figure_name2, _ = visualisations.activity_by_registration(activity_by_track_opening)
    figure_name3, fig_dir = visualisations.branch_activity_heatmap(activity_by_branch)
    figure_names = [figure_name1, figure_name2, figure_name3]

    # Combine all dataframes to a single one mimicking the google sheet table form
    all_results_dataframe = populus_by_weeks
    all_results_dataframe = pd.concat(
        [all_results_dataframe, pd.DataFrame(index=["** Track Opening **"], columns=populus_by_weeks.columns)],
        ignore_index=False)
    all_results_dataframe = pd.concat([all_results_dataframe, activity_by_track_opening], ignore_index=False)
    all_results_dataframe = pd.concat(
        [all_results_dataframe, pd.DataFrame(index=["** Branch **"], columns=populus_by_weeks.columns)],
        ignore_index=False)
    all_results_dataframe = pd.concat([all_results_dataframe, activity_by_branch], ignore_index=False)
    all_results_dataframe = all_results_dataframe.fillna(" ")


    return all_results_dataframe, figure_names, fig_dir

