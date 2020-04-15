import pandas as pd
from input_converters import ask_date_range_month_year
from weekly_calender import week_date_start_end, track_opening_start_end
from retrieve_data_by_activity_date import retrieve_data_by_activity_date
from weekly_analysis import column_converter, remove_user_duplicates, populus_counter_by_weeks, \
    activity_by_track_opening_counter, activity_by_branch_counter
import datetime as dt
import numpy as np

## Generates attendance tab in weekly report
def generator_weekly_report():
    loginFileName = "Login.txt"
    # field names used in SQL query
    fields = {  # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
        "user": "userID",  # user connect ID
        "registration": "dateJoined",  # date registered to sheconnect
        "lesson_date": "lessonDate",  # date lesson was taken
        "graduation_threshold": "80precent",  # lesson no which marks 80% of course milestone
        "track_name": "trackName",  # short name of the track
        "lesson_no": "lessonNo",  # lesson number
        "role_name": "role",  # role name
        "staff": "roleID",  # role ID - converted after retrieval to binary - 1 for staff 0 for student
        "role_assigned_date": "assignRoleDate",  # date role was assigned
        "branch": "branchName",  # short name of the branch
        "branch_type": "branchType",  # branch type
        "branch_active": "active"  # 0 if branch is no longer active
    }

    field_datatpypes = {
        "user": "int",  # user connect ID
        "registration": "datetime",  # date registered to sheconnect
        "lesson_date": "datetime",  # date lesson was taken
        "graduation_threshold": "int",  # lesson no which marks 80% of course milestone
        "track_name": "string",  # short name of the track
        "lesson_no": "int",  # lesson number
        "role_name": "string",  # role name
        "staff": "binary",  # converted so 1 for staff, 0 for student
        "role_assigned_date": "datetime",  # date role was assigned
        "branch": "string",  # short name of the branch
        "branch_type": "string",  # branch type
        "branch_active": "binary"  # 0 if branch is no longer active
    }

    print("*** Weekly report generator ***")
    # print("Enter range of weeks to be analyzed")
    # [min_date_weeks, max_date_weeks]=ask_date_range_month_year()
    # print("Enter registration range for sub-classification")
    # [min_date_registration, max_date_registration]=ask_date_range_month_year()
    min_date_registration = dt.datetime(2020, 1, 1)
    min_date_weeks = dt.datetime(2020, 1, 1)
    max_date_registration = dt.datetime(2020, 4, 1)
    max_date_weeks = dt.datetime(2020, 4, 4)
    [week_begin_list, week_end_list] = week_date_start_end(min_date_weeks, max_date_weeks)

    # Calling the analysis functions
    data_query_orig = pd.read_csv("sql_data.csv")
    # TODO: Get data from SQL query
    # data_query=retrieve_data_by_activity_date(loginFileName, min_date_weeks, max_date_weeks)

    # Convert staff column to binary
    mask_staff = (data_query_orig[fields["staff"]] == 1) | (data_query_orig[fields["staff"]] == 22)
    mask_students = ~mask_staff
    data_query_orig.loc[mask_staff, fields["staff"]] = 1
    data_query_orig.loc[mask_students, fields["staff"]] = 0

    data_no_duplicates = remove_user_duplicates(data_query_orig, fields["user"], fields["lesson_date"])
    # Using groupby eliminates the other data used for sub-classificaitons data_query.groupby([fields["lesson_date"], fields["registration"]]).count()
    data_converted = column_converter(data_no_duplicates, fields, field_datatpypes)
    [reg_start_dates, reg_end_dates] = track_opening_start_end(min_date_registration, max_date_registration)

    # The following functions loop on week dates
    populus_by_weeks = populus_counter_by_weeks(data=data_converted, staff_col=fields["staff"],
                                                activity_col=fields["lesson_date"], week_start=week_begin_list,
                                                week_end=week_end_list)
    activity_by_branch = activity_by_branch_counter(data=data_converted, branch_col=fields["branch"],
                                                    activity_col=fields["lesson_date"], week_start=week_begin_list,
                                                    week_end=week_end_list)

    # The following function loops on week dates and registration date
    activity_by_track_opening = activity_by_track_opening_counter(data=data_converted,
                                                                  registration_col=fields["registration"],
                                                                  activity_col=fields["lesson_date"],
                                                                  reg_start_date_list=reg_start_dates,
                                                                  reg_end_date_series=reg_end_dates,
                                                                  week_start=week_begin_list,
                                                                  week_end=week_end_list)

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
    print("Analysis Done")
    # TODO: Why is march20 opening empty
    # TODO: Why so few staff members
    return all_results_dataframe
