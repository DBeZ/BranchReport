
# Creates SQL query
date_four_months_ago='2016-08-07'
date_now='2016-08-07'
final_columns = '''
    userID, 
    firstname_eng, 
    lastname_eng, 
    email, 
    dateJoined, 
    track, 
    lessonDate, 
    lessonNo, 
    branchID, 
    branchName, 
    role_ID, 
    roleName
    '''
all_columns = '''
    userID,
    firstname_eng,
    lastname_eng,
    email,
    dateJoined,
    track,
    lessonDate,
    serial_number AS lessonNo,
    branchID,
    branchName
    '''
lesson_followup_columns = '''
    userid_connect,
    track_id_connect AS trackID,
    FROM_UNIXTIME(TIMESTAMP, '%Y-%m-%d') AS lessonDate,
    lesson_id_connect
    '''
lesson_followup_table = "shecodes_monster_2_0.lessons_followup"
new_users_columns = '''
    userid_connect AS userID,
    firstname_eng,
    lastname_eng,
    email,
    FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') AS dateJoined,
    branch_ID AS BranchID
    '''
new_users_table = "shecodes_monster_2_0.users_new"
lesson_mapping_table = "shecodes_monster_2_0.lessons_mapping"
branch_type_select = '''
    id AS branch_ID,
    short_name AS branchName,
    branchTypeID,
    branchTypes AS branchType,
    active
    '''
branch_type_columns = '''
    id AS branchTypeID,
    branch_type AS branchTypes
    '''
branch_type_table = "shecodes_monster_2_0.branch_types"
branch_table = "shecodes_monster_2_0.branch"
track_name_columns = '''
    ID,
    track_name AS track
    '''
track_name_table = "shecodes_monster_2_0.track_name"
where_clause = '''
    track_category NOT IN(0, 8) AND
    track_type NOT IN(0, 3) AND
    branchTypeID NOT IN(1, 9) AND
    track_id_connect NOT IN(14) AND
    active IS NOT NULL AND
    serial_number IS NOT NULL
    '''
order_clause = "lessonNo"
group_clause = '''
    userID,
    lessondate
    '''
user_max_type_no_assignment_date_select = '''
    user_ID, maxRoleID AS role_ID, shortname AS roleName
    '''
user_max_type_select = '''
    user_ID, MAX(replaced_role_ids) as maxRoleID, assignRoleDate
    '''
user_type_select = '''
    userid as user_ID , 
    FROM_UNIXTIME(timemodified, '%Y-%m-%d') AS assignRoleDate
    ''' + ","
cases_clause = ''' 
WHEN roleid = 28 THEN 0 
WHEN roleid = 25 THEN 0 
WHEN roleid = 24 THEN 0 
ELSE roleid 
'''
roles_table = "shecodes_shecodes.mdl_role_assignments"
group_clause2 = 'user_ID'
where_clause2 = "user_ID IS NOT NULL"

query_text = (
    f'SELECT {final_columns} '
    f'FROM (SELECT * '
    f'FROM (SELECT * '
    f'FROM(SELECT {all_columns} '
    f'FROM(SELECT {lesson_followup_columns} '
    f'FROM {lesson_followup_table} '
    f') AS lessonDateTable '
    f'LEFT JOIN (SELECT {new_users_columns} '
    f'FROM {new_users_table} '
    f') AS usersSubset '
    f'ON userid_connect = userID '
    f'LEFT JOIN {lesson_mapping_table} '
    f'ON lessons_mapping.lesson_id_connect = lessonDateTable.lesson_id_connect '
    f'LEFT JOIN (SELECT {branch_type_select} '
    f'FROM(SELECT {branch_type_columns} '
    f'FROM {branch_type_table} '
    f') AS Branch_Types  '
    f'RIGHT JOIN {branch_table} '
    f'ON branch.branch_type = Branch_Types.branchTypeID '
    f') AS Branches '
    f'ON branch_ID = BranchID '
    f'LEFT JOIN shecodes_monster_2_0.tracks '
    f'ON tracks.track_id_connect = lessonDateTable.trackID '
    f'LEFT JOIN (SELECT {track_name_columns} '
    f'FROM {track_name_table} '
    f') AS '
    f'track ON track.ID = tracks.track_name '
    f'WHERE {where_clause} AND '
    f"UNIX_TIMESTAMP(lessonDate) BETWEEN UNIX_TIMESTAMP(\'{date_four_months_ago}\') AND UNIX_TIMESTAMP(\'{date_now}\') "
    f'ORDER BY {order_clause} DESC '
    f') AS t '
    f'GROUP BY {group_clause} '
    f')AS t3 '
    f')AS user_lessons_branch_table '
    f'LEFT JOIN (SELECT {user_max_type_no_assignment_date_select} '
    f'FROM (SELECT * '
    f'FROM (SELECT {user_max_type_select} '
    f'FROM (SELECT {user_type_select} '
    f'CASE {cases_clause} '
    f'END AS replaced_role_ids '
    f'FROM {roles_table} '
    f') AS userRoleSubset '
    f'GROUP BY {group_clause2} '
    f') AS data_table '
    f'LEFT JOIN mdl_role '
    f'ON data_table.maxRoleID=mdl_role.id '
    f'WHERE {where_clause2} '
    f') AS role_table '
    f') AS highest_roles '
    f'ON user_lessons_branch_table.userID=highest_roles.user_ID '
)

print(query_text)