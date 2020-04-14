

# Persistence Data - by Tracks Openings
def getSQL_Persistence_Data_By_Tracks_Openings(d1, d2, r1, r2):
    str = '  '
    str += ' SELECT count(*)  FROM '
    str += ' ( '
    str += ' SELECT x.email, x.firstname_eng, x.lastname_eng, max(roleid) as role, ddate, userid,  '
    str += ' CASE  '
    str += ' WHEN ddate BETWEEN (\''
    str += r1.date().isoformat()   
    str += '\') and (\''
    str += r2.date().isoformat() 
    str += '\') THEN \'MONTH19\' '
    str += ' ELSE \'Other\' '
    str += ' END as \'opening_time\'  '
    str += ' from '
    str += ' ( '
    str += ' SELECT  '
    str += ' from_unixtime(lessons_followup.timestamp, \'%Y-%m-%d\') as lesson_day, lessons_followup.track_id_connect, lesson_id_connect, from_unixtime(users_new.date_joined_lms, \'%Y-%m-%d\') as ddate, '
    str += ' users_new.email, users_new.firstname_eng, users_new.lastname_eng, roleid, users_new.userid_connect as userid FROM lessons_followup  '
    str += ' LEFT JOIN users_new ON lessons_followup.userid_connect = users_new.userid_connect '
    str += ' left join tracks on tracks.track_id_connect = lessons_followup.track_id_connect '
    str += ' left join branch on branch.id = users_new.branch_id '
    str += ' left join shecodes_shecodes.mdl_role_assignments as ra on ra.userid = lessons_followup .userid_connect '
    str += ' WHERE '
    str += ' lessons_followup.timestamp between unix_timestamp(\''
    str += d1.date().isoformat()  # '2019-06-02'
    str += '\') and unix_timestamp(\''
    str += d2.date().isoformat()  # '2019-06-06'
    str += '\') and track_name != 0 and track_name != 8  '
    str += ' group by userid, roleid '
    str += '  ) as x '
    str += ' group by userid '
    str += ' ) as y  '
    str += ' WHERE role not in (1,22,23,21) and opening_time = \'MONTH19\'  '
    return str

