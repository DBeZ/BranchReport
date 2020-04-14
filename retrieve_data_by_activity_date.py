##########################################################################
# SQL query of database - joining date is when First lesson was done
# Requires two date ranges
# Query no loaded from file
# Also removes:
#   Negative lesson numbers
#   Courses of type Other, Web advanced and NG
# Results pickled rather than returned (in case df is very large).
##########################################################################
import pandas as pd
from OldBackups.shecodesLogin import login
from connect_to_database import connect_to_database


# SQL query to receive all activity entries in a given date range
def last_lesson_query_by_activity_date(connection, mindate, maxdate):
    parameters = (mindate, maxdate)
    query = ""
    query += "SELECT "
    query += "  userID, dateJoined, lessonDate, 80precent, shortname AS trackName,serial_number AS lessonNo,branchName, branchType, active "
    query += "FROM ( "
    query += "	SELECT userid_connect, track_id_connect AS trackID,  FROM_UNIXTIME(timestamp, '%Y-%m-%d')  AS lessonDate, lesson_id_connect FROM lessons_followup "
    query += "	) AS lessonDateTable "
    query += "LEFT JOIN (SELECT userid_connect AS userID, FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') AS dateJoined, branch_ID AS BranchID FROM users_new) AS usersSubset "
    query += "ON   userid_connect = userID "
    query += "LEFT JOIN lessons_mapping "
    query += "ON lessons_mapping.lesson_id_connect=lessonDateTable.lesson_id_connect "
    query += "left JOIN "
    query += "	("
    query += "	SELECT id AS branch_ID, short_name AS branchName, branchTypeID, branchTypes AS branchType, active "
    query += "	FROM ( "
    query += "		SELECT id AS branchTypeID, branch_type AS branchTypes FROM branch_types "
    query += "		) AS Branch_Types "
    query += "	RIGHT JOIN branch "
    query += "	ON branch.branch_type=Branch_Types.branchTypeID "
    query += ") AS Branches "
    query += "ON branch_ID=BranchID  "
    query += "LEFT JOIN tracks "
    query += "ON tracks.track_id_connect=lessonDateTable.trackID "
    query += "	WHERE track_category NOT IN (0,8) " # Not Others and not Bagrut
    query += "      AND track_id_connect NOT IN (4,14) " # Not Web and not web_sample
    query += "		AND track_type NOT IN (0,3) " # Not Non-educational and not Next-Generation
    query += "      AND branchTypeID NOT IN (1,9) " # Not NG Regional and not NG High School
    query += "		AND active IS NOT NULL " # Some users do not have an assined value for branch Type, this leads to active state being NULL
    query += "	AND UNIX_TIMESTAMP(lessonDate) BETWEEN UNIX_TIMESTAMP(%s) AND UNIX_TIMESTAMP(%s) " #Loged into a lesson in this time span

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
