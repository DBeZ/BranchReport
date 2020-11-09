#####################################################################################################################
# Query for getting all activity in daterange, with track, user registration, branch details, and graduation cutoff
#####################################################################################################################

import pandas as pd
from connect_to_database import connect_to_database
from user_specific_extractor import login_sql


# SQL query to receive all activity entries in a given date range
def last_lesson_query_by_activity_date(connection, mindate, maxdate):
    parameters = (mindate, maxdate)
    fields_final_display = "userID, dateJoined, lessonDate, 80precent, shortname AS trackName,serial_number AS lessonNo,   branchName, branchType, active"

    fields_updating_progress = "userid_connect, track_id_connect AS trackID,  FROM_UNIXTIME(timestamp, '%Y-%m-%d') AS lessonDate, lesson_id_connect "
    table_updating_progress = "shecodes_monster_2_0.lessons_followup "

    table_updating_users = "shecodes_monster_2_0.users_new "
    fields_updating_users = "userid_connect AS userID, FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') AS dateJoined, branch_ID AS BranchID "
    on_user = "userid_connect = userID "

    table_lessons = "shecodes_monster_2_0.lessons_mapping "
    on_lesson = "lessons_mapping.lesson_id_connect=lessonDateTable.lesson_id_connect "

    fields_branch_final = "id AS branch_ID, short_name AS branchName, branchTypeID, branchTypes AS branchType, active "
    fields_branches_type = "id AS branchTypeID, branch_type AS branchTypes "
    table_branch_type = "shecodes_monster_2_0.branch_types "
    table_branches = "shecodes_monster_2_0.branch "
    on_branch_type = "branch.branch_type=Branch_Types.branchTypeID "
    on_branch = "branch_ID=BranchID "

    table_track = "shecodes_monster_2_0.tracks "
    on_track = "tracks.track_id_connect=lessonDateTable.trackID "
    condition_track = "track_category NOT IN (0,8)	"
    condition_track_type = "track_type NOT IN (0,3) "
    condition_branch_type = "branchTypeID NOT IN (1,9) "
    condition_track_id = "track_id_connect NOT IN (14) "
    condition_branch_active = "active IS NOT NULL "
    condition_registration_date_range = "UNIX_TIMESTAMP(lessonDate) BETWEEN UNIX_TIMESTAMP(%s) AND UNIX_TIMESTAMP(%s) "

    query = (
        f"SELECT {fields_final_display} "

        f"FROM (SELECT {fields_updating_progress} "
        f"FROM {table_updating_progress} "
        f") AS lessonDateTable "

        f"LEFT JOIN (SELECT {fields_updating_users} "
        f" FROM {table_updating_users} "
        f") AS usersSubset "
        f"ON {on_user} "

        f"LEFT JOIN {table_lessons} "
        f"ON {on_lesson} "

        f"left JOIN (SELECT {fields_branch_final} "
        f"FROM (SELECT {fields_branches_type} "
        f"FROM {table_branch_type} "
        f") AS Branch_Types "
        f"RIGHT JOIN {table_branches} "
        f"ON {on_branch_type} "
        f") AS Branches "
        f"ON {on_branch} "

        f"LEFT JOIN {table_track} "
        f"ON {on_track} "
        f"WHERE {condition_track} "
        f"AND {condition_track_type} "
        f"AND {condition_branch_type} "
        f"AND {condition_track_id} "
        f"AND {condition_branch_active} "
        f"AND {condition_registration_date_range} "
    )
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    columns = cursor.column_names
    query_res_df = pd.DataFrame(cursor.fetchall())
    query_res_df.columns = list(columns)

    connection.close()
    cursor.close()

    fields_dict = {  # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
        "user": "userID",  # user connect ID
        "registration": "dateJoined",  # date registered to sheconnect
        "lesson_date": "lessonDate",  # date lesson was taken
        "graduation_threshold": "80precent",  # lesson no which marks 80% of course milestone
        "track_name": "trackName",  # short name of the track
        "lesson_no": "lessonNo",  # lesson number
        "branch": "branchName",  # short name of the branch
        "branch_type": "branchType",  # branch type
        "branch_active": "active"  # 0 if branch is no longer active
    }

    field_datatpypes_dict = {
        "user": "int",  # user connect ID
        "registration": "datetime",  # date registered to sheconnect
        "lesson_date": "datetime",  # date lesson was taken
        "graduation_threshold": "int",  # lesson no which marks 80% of course milestone
        "track_name": "string",  # short name of the track
        "lesson_no": "int",  # lesson number
        "branch": "string",  # short name of the branch
        "branch_type": "string",  # branch type
        "branch_active": "binary"  # 0 if branch is no longer active
    }
    return query_res_df, fields_dict, field_datatpypes_dict


## Login to database and query to recive all activity enteries in a given date range
def retrieve_data_by_activity_date(sql_details_file_name,  user_specific_dir, dateStart, dateEnd):
    sql_login_dict = login_sql(sql_details_file_name, user_specific_dir)
    connection = connect_to_database(sql_login_dict["User"], sql_login_dict["Pass"], sql_login_dict["Database"], sql_login_dict["Host"], sql_login_dict["Port"])
    print("User activity data being retrieved")
    data_df, fields_dict, field_datatpypes_dict =last_lesson_query_by_activity_date(connection, dateStart, dateEnd)
    print("Data retrieval done!")
    return data_df, fields_dict, field_datatpypes_dict

