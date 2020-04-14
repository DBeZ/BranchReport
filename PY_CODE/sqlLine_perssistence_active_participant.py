# perssistence data active participant
#  TAB :  perssistence data active participant
#  line 4 : '2 - weekly users by branch by track.sql'
# line 5 : '1.6 - Active participants by meetings.sql'


def getSQL_active_participant_line_5(d1, d2):
    str = '  '
    str += ' SELECT count(*) FROM '
    str += ' (    '
    str += ' SELECT student_name, userid, email, COUNT(lesson) as meeting, track,  branch, team FROM   '
    str += ' (SELECT CONCAT_WS(\' \', firstname_eng, lastname_eng) AS student_name, lf.userid_connect as userid, track_name.track_name as track,    '
    str += '  branch.branch_name as branch, lesson_id_connect as lesson,   '
    str += ' from_unixtime(timestamp, \'%Y-%m-%d\') as ltime , email, max(roleid) as team   '
    str += ' FROM lessons_followup as lf   '
    str += ' LEFT JOIN tracks on tracks.track_id_connect = lf.track_id_connect   '
    str += ' LEFT JOIN track_name on track_name.id = tracks.track_name   '
    str += ' LEFT JOIN users_new on users_new.userid_connect = lf.userid_connect  '
    str += ' LEFT JOIN branch on branch.id = users_new.branch_id   '
    str += ' LEFT JOIN shecodes_shecodes.mdl_role_assignments as ra on ra.userid = lf.userid_connect  '
    str += ' WHERE from_unixtime(timestamp, \'%Y-%m-%d\') >= ( CURDATE() - INTERVAL 60 DAY )  '
    str += ' AND tracks.track_name not in(0,6,8)   '
    str += ' AND branch_type != 1   '
    str += ' GROUP by userid, ltime  '
    str += ' ) as x group by userid,student_name '
    str += ' ) as r WHERE meeting > 2 and team not in(22,23,21)   '
    return str

