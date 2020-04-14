import pandas as pd
from input_converters import ask_date_range_month_year
from weekly_calender import week_date_start_end, track_opening_start_end
from retrieve_data_by_activity_date import retrieve_data_by_activity_date
from weekly_analysis import column_converter, remove_user_duplicates, populus_counter, activity_by_track_opening_counter
import datetime as dt

## Generates attendance tab in weekly report
def generator_weekly_report():
    loginFileName = "Login.txt"
    #field names used in SQL query
    fields = { # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
        "user": "userID", # user connect ID
        "staff": "staff", # 1 for staff, 0 for student
        "registration": "dateJoined", # date registered to sheconnect
        "lesson_date": "lessonDate", # date lesson was taken
        "graduation_threshold": "80precent", # lesson no which markes 80% of course milestone
        "track_name": "trackName", # short name of the track
        "lesson_no": "lessonNo", # lesson number
        "branch": "branchName", # short name of the branch
        "branch_type": "branchType", # branch type
        "branch_active": "active" # 0 if branch is no longer active
    }

    field_datatpypes = {
        "user": "int",  # user connect ID
        "staff": "binary",  # 1 for staff, 0 for student
        "registration": "datetime",  # date registered to sheconnect
        "lesson_date": "datetime",  # date lesson was taken
        "graduation_threshold": "int",  # lesson no which markes 80% of course milestone
        "track_name": "string",  # short name of the track
        "lesson_no": "int",  # lesson number
        "branch": "string",  # short name of the branch
        "branch_type": "string",  # branch type
        "branch_active": "binary"  # 0 if branch is no longer active
    }

    print("*** Weekly report generator ***")
    # [min_date, max_date]=ask_date_range_month_year()
    min_date = dt.datetime(2019, 8, 1)
    # max_date = dt.datetime(2019, 11, 1)
    max_date = dt.datetime(2019, 12, 1)
    [week_begin_list, week_end_list]=week_date_start_end(min_date, max_date)
    for ind in range(len(week_begin_list)):
        data_query = pd.read_csv("sampleDataQuery2.csv")
        #TODO: Get data from SQL query
        data_query = column_converter(data_query, fields, field_datatpypes)
        data_no_duplicates = remove_user_duplicates(data_query, fields["user"])
        [tot_no, staff_no, stud_no] = populus_counter(data_no_duplicates, fields["staff"])
        # TODO: Create dataframe with rows as tot_no, staff_no, stud_no and colums as weeks
        activity_by_branch=data_no_duplicates[fields["branch"]].value_counts().sort_index(ascending=True)
        # TODO: Create dataframe with rows as branches and colums as weeks

    [reg_start_dates, reg_end_dates] = track_opening_start_end(min_date, max_date)
    activity_by_track_opening = activity_by_track_opening_counter(data=data_no_duplicates, registration_col=fields["registration"], activity_col=fields["lesson_date"], reg_start_date_list=reg_start_dates, reg_end_date_series=reg_end_dates, week_start=week_begin_list, week_end=week_end_list)
    # TODO: Combine all dataframes to one dataframe
    # TODO: Export this dataframe to google sheets
    # TODO: visualsations
    print("done")


generator_weekly_report()