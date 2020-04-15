import pandas as pd
from shecodesLogin import login
from connect_to_database import connect_to_database


# SQL query to receive all activity entries in a given date range
def last_lesson_query_by_activity_date(connection, mindate, maxdate):
    parameters = (mindate, maxdate)
    fields_final_display = "userID, dateJoined, lessonDate, 80precent, shortname AS trackName,serial_number AS lessonNo, role, roleID, assignRoleDate, branchName, branchType, active"

    fields_updating_progress = "userid_connect, track_id_connect AS trackID,  FROM_UNIXTIME(timestamp, '%Y-%m-%d') AS lessonDate, lesson_id_connect"
    table_updating_progress = "shecodes_monster_2_0.lessons_followup"

    table_updating_users = "shecodes_monster_2_0.users_new"
    fields_updating_users = "userid_connect AS userID, FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') AS dateJoined, branch_ID AS BranchID"
    on_user = "userid_connect = userID"

    table_lessons = "shecodes_monster_2_0.lessons_mapping"
    on_lesson = "lessons_mapping.lesson_id_connect=lessonDateTable.lesson_id_connect"

    fields_branch_final = "id AS branch_ID, short_name AS branchName, branchTypeID, branchTypes AS branchType, active"
    fields_branches_type = "id AS branchTypeID, branch_type AS branchTypes"
    table_branch_type = "shecodes_monster_2_0.branch_types"
    table_branches = "shecodes_monster_2_0.branch"
    on_branch_type = "branch.branch_type=Branch_Types.branchTypeID"
    on_branch = "branch_ID=BranchID"

    fields_role_final = "user_ID, shortname AS role, roleid as roleID, assignRoleDate"
    fields_updating_roles = "userid as user_ID , roleid , FROM_UNIXTIME(timemodified, '%Y-%m-%d') AS assignRoleDate"
    table_updating_roles = "shecodes_shecodes.mdl_role_assignments"
    table_role_types = "shecodes_shecodes.mdl_role"
    on_role = "userRoleSubset.roleid=mdl_role.id"
    condition_role = "roleid NOT IN (8, 21, 23, 24)"
    on_user2 = "lessonDateTable.userid_connect=user_ID"

    table_track = "shecodes_monster_2_0.tracks"
    on_track = "tracks.track_id_connect=lessonDateTable.trackID"
    condition_track = "track_category NOT IN (0,8)	"
    condition_track_type = "track_type NOT IN (0,3) "
    condition_branch_type = "branchTypeID NOT IN (1,9) "
    condition_track_id = "AND track_id_connect NOT IN (4,14) "
    condition_branch_active = "AND active IS NOT NULL "
    condition_registration_date_range = "AND UNIX_TIMESTAMP(lessonDate) BETWEEN UNIX_TIMESTAMP(%s) AND UNIX_TIMESTAMP(%s)"

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

        f"left JOIN (SELECT {fields_role_final} "
        f"FROM (SELECT {fields_updating_roles} "
        f"FROM {table_updating_roles} "
        f") AS userRoleSubset "
        f"RIGHT JOIN {table_role_types} "
        f"ON {on_role} "
        f"WHERE {condition_role} "
        f") AS roles "
        f"ON {on_user2} "

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
    return query_res_df


## Login to database and query to recive all activity enteries in a given date range
def retrieve_data_by_activity_date(loginFileName, dateStart, dateEnd):
    loginUsername, password, databaseName, hostName, _, portNumber, _ = login(loginFileName)
    connection = connect_to_database(loginUsername, password, databaseName, hostName, portNumber)
    data_df=last_lesson_query_by_activity_date(connection, dateStart, dateEnd)
    return data_df

