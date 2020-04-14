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

def last_lesson_query_by_join_date(connection, mindate, maxdate, pickelName="queryRes"):
    parameters = (mindate, maxdate)
    query=(
    '''
   

select userID,
regDate,
highestLessonDate,
max(highestLesson) highestLessonFromAllTracks,
track,
leavingDate,
branch

FROM
(Select userID,
regDate,
highestLessonDate,
highestLesson,
track_name as track,
lastLessonDate as leavingDate,
branch_name as branch

From (

select userID, highestLessonDate, highestLesson, track_name, lastLessonDate, track_nameID
from (

select UserID,  
	lessonDate as highestLessonDate, 
	max(serial_number) as highestLesson,  
	track_name as track_nameID
from 
(
    select userid_connect as userID, FROM_UNIXTIME(timestamp, '%Y-%m-%d') as lessonDate, lesson_id_connect as lessonID, track_id_connect as trackID from lessons_followup
    )as x
    left join lessons_mapping on lessons_mapping.lesson_id_connect=x.lessonID
left join tracks on x. trackID = track_id_connect
    where track_type in (1,2) AND tracks.track_name not in(0,6,8)
group by userID, track_name
) as maxLessonT
    
Left join
(

select userid_connect, max(lessonDate) as lastLessonDate
from 
(
    select userid_connect, FROM_UNIXTIME(timestamp, '%Y-%m-%d') as lessonDate from lessons_followup
    )as y
group by userid_connect
) as lastLessonT
On lastLessonT.userid_connect= maxLessonT.userID
left join track_name on track_nameID = track_name.id 

  
) as z



left JOIN 
    (select userid_connect, branch_id as branchID, FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') as regDate 
    from users 
     ) as  w on z.userID=w.userid_connect
left join branch on branch.id = branchID
where branch_type != 1 AND UNIX_TIMESTAMP(regDate) BETWEEN UNIX_TIMESTAMP(%s) AND UNIX_TIMESTAMP(%s)
    ) as g
    group by userID
 '''
    )

    cursor = connection.cursor()
    cursor.execute(query, parameters)
    columns = cursor.column_names
    res= pd.DataFrame(cursor.fetchall())
    res.columns = list(columns)

    connection.close()
    cursor.close()
    res.to_pickle("./"+pickelName+".pkl")



def retrieve_data_by_join_date(loginFileName, dateRanges,  pickelFileName):
    loginUsername, password, databaseName, hostName, _, portNumber, _ = login(loginFileName)
    connection = connect_to_database(loginUsername, password, databaseName, hostName, portNumber)
    last_lesson_query_by_join_date(connection, dateRanges[0], dateRanges[1], pickelFileName)

