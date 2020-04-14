



def getSQL_line9(d1, d2):
    # unixtime1 = time.mktime(d1.timetuple())
    # unixtime2 = time.mktime(d2.timetuple())
    # return unixtime1, '  ', unixtime2
    str = '  '
    str += ' SELECT count(*) from '
    str += ' (    '
    str += ' SELECT DISTINCT   '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect,   '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng, max(roleid) as role FROM lessons_followup   '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect  '
    str += ' left join tracks on tracks.track_id_connect = lessons_followup.track_id_connect  '
    str += ' left join branch on branch.id = users_new.branch_id  '
    str += ' left join shecodes_shecodes.mdl_role_assignments as ra on ra.userid = lessons_followup .userid_connect '
    str += ' WHERE  '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') and track_name != 0 and track_name != 8  '
    str += ' group by email  '
    str += ' ) as x  '
    str += ' WHERE role not in(21,22,23)  '
    return str


def getSQL_line10(d1, d2):
    str = ' '
    str += ' SELECT count(*) from '
    str += ' (    '
    str += ' SELECT DISTINCT '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect,  '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng, from_unixtime(users_new.date_joined_lms, \'%Y-%m-%d\') as ddate, roleid  '
    str += ' FROM lessons_followup  '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect  '
    str += ' left join `shecodes_shecodes`.mdl_role_assignments as ra on ra.userid = lessons_followup.userid_connect '
    str += ' LEFT JOIN tracks ON tracks.track_id_connect = lessons_followup.track_id_connect '
    str += ' WHERE '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') and track_name != 0 and track_name != 8  '
    str += ' and roleid in (1,21,22) '
    str += ' group by email '
    str += ' ) as x  '
    return str


def getSQL_line11(d1, d2):
    str = '  '
    str += ' SELECT count(*) FROM '
    str += ' (    '
    str += ' SELECT DISTINCT '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect, '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng  '
    str += ' FROM lessons_followup '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect '
    str += ' LEFT JOIN tracks on tracks.track_id_connect = lessons_followup.track_id_connect '
    str += ' LEFT JOIN branch on branch.id = users_new.branch_id '
    str += ' WHERE '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') AND track_name != 0 and track_name != 8  '
    str += ' GROUP BY email '
    str += ' ) as x  '
    return str


def getSQL_line13_19(d1, d2):
    str = '  '
    str += ' SELECT '
    str += ' CASE '
    str += ' WHEN ddate < "2018-07-01" THEN \'a BA\' '
    str += ' WHEN ddate BETWEEN "2018-07-02" and "2018-09-01" THEN \'b AUG 18\' '
    str += ' WHEN ddate BETWEEN "2018-10-01" and "2018-11-30" THEN \'c NOV 18\' '
    str += ' WHEN ddate BETWEEN "2019-01-15" and "2019-02-14" THEN \'d FEB 19\' '
    str += ' WHEN ddate Between "2019-04-20" and "2019-05-16" THEN \'e MAY 19\' '
    str += ' WHEN ddate Between "2019-07-15" and "2019-08-15" THEN \'f AUG 19\' '
    str += ' WHEN ddate Between "2019-10-15" and "2019-11-15" THEN \'g NOV 19\' '
    str += ' WHEN ddate Between "2020-03-08" and "2020-03-20" THEN \'h MAR 20\' '
    str += ' ELSE \'h UN\' '
    str += ' END as countusers_new, count(email)  FROM '
    str += ' ( '
    str += ' SELECT DISTINCT '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect, '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng,  from_unixtime(users_new.date_joined_lms, \'%Y-%m-%d\') as ddate '
    str += ' FROM lessons_followup '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect '
    str += ' left join tracks on tracks.track_id_connect = lessons_followup.track_id_connect '
    str += ' WHERE  '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') and track_name != 0 and track_name != 8  '
    str += '  group by email '
    str += ' order by lesson_day '
    str += ' ) AS attendance_table '
    str += ' group by countusers_new  '
    return str


def getSQL_line_20_branch(d1, d2):
    str = '  '
    str += ' SELECT COUNT(email) as users_new, branch_name FROM '
    str += ' ( '
    str += ' SELECT DISTINCT '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect, track_name, branch_id, branch.branch_name, '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng '
    str += ' FROM lessons_followup '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect '
    str += ' LEFT JOIN tracks ON tracks.track_id_connect = lessons_followup.track_id_connect '
    str += ' LEFT JOIN branch ON branch.id = users_new.branch_id '
    str += ' WHERE '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') and track_name != 0 and track_name != 8  '
    str += ' group by email '
    str += ' order by lesson_day '
    str += ' ) AS attendance_table '
    str += ' group by branch_name '
    return str


