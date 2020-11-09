## TODO:
# Convert starting date to track opening
# Connect to sql
# Find way to devide into branches
branch_code=10

#imports
import pandas as pd
import numpy as np
import datetime as dt
import dateutil.rrule as rrule
import dateutil.relativedelta as relativedelta
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter, MultipleLocator
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
from connect_to_database import connect_to_database
from user_specific_extractor import login_sql

#Setting notebook options
#Display all columns in dtatable:
pd.set_option('display.max_columns', 999)
#Display all rows in dtatable:
pd.set_option('display.max_rows', 999)

# SQL query to receive all user lesson and branch data
def users_lesson_branch_query(connection):
    all_columns ='''
        userID,
        firstname_eng,
        lastname_eng,
        email,
        dateJoined,
        track,
        lessonDate,
        serial_number
        AS
        lessonNo,
        branchID,
        branchName
        '''
    lesson_followup_columns ='''
        userid_connect,
        track_id_connect AS trackID,
        FROM_UNIXTIME(TIMESTAMP, '%Y-%m-%d') AS lessonDate,
        lesson_id_connect
        '''
    lesson_followup_table = "shecodes_monster_2_0.lessons_followup"
    new_users_columns ='''
    userid_connect AS userID,
    firstname_eng,
    lastname_eng,
    email,
    FROM_UNIXTIME(date_joined_lms, '%Y-%m-%d') AS dateJoined,
    branch_ID AS BranchID
    '''
    New_users_table = "shecodes_monster_2_0.users_new"
    Lesson_mapping_table = "shecodes_monster_2_0.lessons_mapping"
    D ='''
    id AS branch_ID,
    short_name AS branchName,
    branchTypeID,
    branchTypes AS branchType,
    active
    '''
    Branch_type_columns = '''
    id AS branchTypeID,
    branch_type AS branchTypes
    '''
    Branch_type_table = "shecodes_monster_2_0.branch_types"
    Branch_table = "shecodes_monster_2_0.branch"
    Track_name_columns ='''
    ID,
    track_name AS track
    '''
    Track_name_table ="shecodes_monster_2_0.track_name"
    where_clause ='''
    track_category NOT IN(0, 8) AND
    track_type NOT IN(0, 3) AND
    branchTypeID NOT IN(1, 9) AND
    track_id_connect NOT IN(14) AND
    active IS NOT NULL AND
    UNIX_TIMESTAMP(lessonDate) BETWEEN UNIX_TIMESTAMP('{date_two_weeks_ago}') AND UNIX_TIMESTAMP('{date_now}') AND 
    serial_number IS NOT NULL
    '''
    Order_clause ="lessonNo"
    Group_clause = '''
    userID,
    lessondate
    '''

    query = (
        f'SELECT * '
        f'FROM(SELECT {all_columns} '
        f'FROM(SELECT {lesson_followup_columns} '
        f'FROM {lesson_followup_table} '
        f') AS lessonDateTable'
        f'LEFT JOIN (SELECT {new_users_columns} '
        f'FROM {new_users_table} '
        f') AS usersSubset '
        f'ON userid_connect = userID '
        f'LEFT JOIN {lesson_mapping_table} '
        f'ON lessons_mapping.lesson_id_connect = lessonDateTable.lesson_id_connect '
        f'LEFT JOIN (SELECT {d} '
        f'FROM(SELECT {Branch_type_columns} '
        f'FROM {branch_type_table} '
        f') AS Branch_Types  '
        f'RIGHT JOIN {branch_table} '
        f'ON branch.branch_type = Branch_Types.branchTypeID '
        f') AS Branches '
        f'ON branch_ID = BranchID '
        f'LEFT JOIN shecodes_monster_2_0.tracks '
        f'ON tracks.track_id_connect = lessonDateTable.trackID '
        f'LEFT JOIN (SELECT {track_name_columns} '
        f'FROM(track_name_table) '
        f') AS '
        f'track ON track.ID = tracks.track_name '
        f'WHERE {where_clause} '
        f'ORDER BY {order_clause} DESC '
        f') AS t '
        f'GROUP BY {group_clause} '
     )

    cursor = connection.cursor()
    cursor.execute(query)
    columns = cursor.column_names
    query_res_df = pd.DataFrame(cursor.fetchall())
    query_res_df.columns = list(columns)

    connection.close()
    cursor.close()

    fields_dict = {  # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
        "user_id": "userID",
        "user_first_name": "firstname_eng",
        "user_last_name": "lastname_eng",
        "email": "email",
        "enroll": "dateJoined",
        "track": "track",
        "lesson_date": "lessonDate",
        "lesson": "lessonNo",
        "branch_id": "branchID",
        "branch": "branchName",
    }

    field_data_types_dict = {
        "user_id": "int",
        "user_first_name": "string",
        "user_last_name": "string",
        "email": "string",
        "enroll": "datetime",
        "track": "string",
        "lesson_date": "datetime",
        "lesson": "int",
        "branch_id": "int",
        "branch": "string",
    }
    return query_res_df, fields_dict, field_data_types_dict




## Login to database and query to recive all activity enteries in a given date range
# TODO: replace with how to login on server
def retrieve_users_with_roles(sql_details_file_name, user_specific_dir):
    sql_login_dict = login_sql(sql_details_file_name, user_specific_dir)
    connection = connect_to_database(sql_login_dict["User"], sql_login_dict["Pass"], sql_login_dict["Database"], sql_login_dict["Host"], sql_login_dict["Port"])
    print("User role data being retrieved")
    data_df, fields_dict, field_data_types_dict=users_with_all_roles_query(connection)
    print("Data retrieval done!")
    return data_df,fields_dict, field_data_types_dict

# Get date 15 weeks ago
def last_15_weeks_range():
  today_date = dt.date.today()
  date_15_weeks_ago = today_date - dt.timedelta(weeks=15)
  return date_15_weeks_ago, today_date

[date_two_weeks_ago, date_now] = last_15_weeks_range()

# Query db
sql_query=sql_query.format(date_two_weeks_ago=str(date_two_weeks_ago), date_now=str(date_now))
## TODO: Complete query of db query (login and data retrieval)


# Add wheteher staff of not
def add_role(role_data, data_df):
    data_df.set_index('userID',  inplace=True)
    role_data = role_data.drop(['roleID'], axis=1)
    roles_data = pd.concat([role_data, pd.get_dummies(role_data["role"])], 1).groupby("user_ID").sum().reset_index()  # Turn role categiry into binary attribute colume and combine so only one entry for each user.
    fields = roles_data.columns

    for column in roles_data.columns: # Convert to yes/no team-member
        if column != fields[0]:
            roles_data[column] = roles_data[column].astype('bool').astype('str')
            roles_data =roles_data.replace({column: {'True': "Yes", 'False': "No"}})

    for col in roles_data: # Drop non required role categories
        if col == fields[0]:
            roles_data.rename(columns={col:"user"})
        elif col == "team_member":
            continue
        else:
            roles_data=roles_data.drop(col, axis=1)

    data_with_roles=data_df.join(roles_data.set_index('user_ID'))
    data_with_roles = data_with_roles.reset_index(drop=False)
    data_with_roles.rename(columns={"index":"userID"},inplace=True)
    return data_with_roles

activity_df=add_role(role_data=df_roles, data_df=activity_df)


## Get start and end dates for each week in date range
# Input - any two dates. Output - all week start and week ends in this range.
# Week begins on Sunday
def week_date_start_end(start_limit, end_limit):
    # convert to a single value
    if isinstance(start_limit, list) or isinstance(start_limit, pd.Series):
        start_limit=start_limit[0]
    if isinstance(end_limit, list) or isinstance(end_limit, pd.Series):
        end_limit=end_limit[0]
    # convert to datetime
    if not isinstance(start_limit, dt.datetime) and not isinstance(start_limit, dt.date):
        start_limit=dt.datetime(start_limit,1,1)
    if not isinstance(end_limit, dt.datetime) and not isinstance(end_limit, dt.date):
        end_limit=dt.datetime(end_limit,12,31)
    if isinstance(start_limit, dt.date):
        start_limit=dt.datetime(start_limit.year, start_limit.month, start_limit.day)
    if isinstance(end_limit, dt.date):
        end_limit=dt.datetime(end_limit.year, end_limit.month, end_limit.day)
    rule_sunday = rrule.rrule(rrule.WEEKLY,byweekday=relativedelta.SU,dtstart=start_limit)
    sundays=rule_sunday.between(start_limit,end_limit,inc=True)
    saturdays=[d+dt.timedelta(days = 6) for d in sundays]
    # start_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in sundays]
    # end_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in saturdays]
    return sundays, saturdays

[start_week_dates, end_week_dates]=week_date_start_end(date_two_weeks_ago, date_now)



# Select Data from this branch only
mask=(activity_df["branchID"]==branch_code)
df_branch=activity_df.loc[mask,:].copy(deep=True)

def convert_track_opening(df, registered_col):
  registered_series_datetime=pd.to_datetime(df[registered_col])
  month= registered_series_datetime.dt.strftime("%b %y")
  df[registered_col]=month
  return df

df_branch=convert_track_opening(df=df_branch, registered_col="dateJoined")

## Count active users in the given date range
def activity_total(data, activity_col, userid_col, week_start_list, week_end_list, result_name):
    data[activity_col] = data[activity_col].apply(pd.to_datetime)
    result_df = pd.DataFrame()
    cols=[]
    results = []
    for i in range(len(week_start_list)):
        mask= (week_start_list[i] <= data[activity_col]) & (data[activity_col] <= week_end_list[i])
        active_in_range = data[userid_col][mask]
        col_name = str(dt.datetime.strftime(week_start_list[i], '%d/%m/%Y'))+"-"+str(dt.datetime.strftime(week_end_list[i], '%d/%m/%Y'))
        results.append(active_in_range.unique().size)
        cols.append(col_name)
    result_df=pd.DataFrame(results)
    result_df.index=cols
    result_df.rename(columns={0:result_name}, inplace=True)
    result_df=result_df.transpose()
    return result_df

## Count active users by track in the given date range
def activity_by_track(data, track_col, activity_col, userid_col, week_start_list, week_end_list):
    result_df = pd.DataFrame()
    cols=[]
    results = []
    tracks=data[track_col].unique()
    tracks=np.sort(tracks)
    for track in tracks:
      data[track_col]
      mask1= (data[track_col]==track)
      track_data=data.loc[mask1].copy(deep=True)
      result_name=track
      df=activity_total(data=track_data, activity_col=activity_col, week_start_list=week_start_list, userid_col=userid_col, week_end_list=week_end_list, result_name=result_name)
      result_df=pd.concat([result_df, df.transpose()], axis=1)
    return result_df.transpose()


all_participants_df=activity_total(data=df_branch, activity_col="lessonDate", userid_col="userID" ,week_start_list=start_week_dates, week_end_list=end_week_dates, result_name="Total participants+staff")
by_track_all_participants_df=activity_by_track(data=df_branch, track_col="track", activity_col="lessonDate", userid_col="userID", week_start_list=start_week_dates, week_end_list=end_week_dates)
table_totals=pd.concat([all_participants_df,by_track_all_participants_df], axis=0)
#table_totals is one of the tables required to display

# Convert activity date to week
# Adds week lable as date range in new column
def activity_by_user(data, activity_col, userid_col, week_start_list, week_end_list):
    data[activity_col] = data[activity_col].apply(pd.to_datetime)
    data["lesson_week"]=""
    all_week_names=[]
    for i in range(len(week_start_list)):
      mask= (week_start_list[i] <= data[activity_col]) & (data[activity_col] <= week_end_list[i])
      date_range_name= str(dt.datetime.strftime(week_start_list[i], '%d/%m/%Y'))+"-"+str(dt.datetime.strftime(week_end_list[i], '%d/%m/%Y'))
      all_week_names.append(date_range_name)
      data["lesson_week"][mask]=date_range_name
    return data, all_week_names

[df_branch_user, all_week_names ]=activity_by_user(data=df_branch, activity_col="lessonDate", userid_col="userID", week_start_list=start_week_dates, week_end_list=end_week_dates)

# concat values for pivot
df_branch_user["full_details"]=df_branch_user["firstname_eng"].str.title()+" "+df_branch_user["lastname_eng"].str.title() +"__"+df_branch_user["team_member"].astype(str)+"__"+df_branch_user["email"]+"__"+df_branch_user["dateJoined"]
# Pivot
progress_table=pd.pivot_table(df_branch_user, values='lessonNo', index=["userID","track","full_details"],
                    columns=['lesson_week'], aggfunc=np.max)

# Editing for display
progress_table.reset_index(inplace=True)
progress_table=progress_table.drop(columns=[""], axis=1) #If sql date range in query is larger then week range if report is not run on sunday. This removes attendance out of the date range.
# Create summation columes based on pivot
attendance=progress_table.iloc[:,3:].count(axis=1)
maxLesson=progress_table.iloc[:,3:].max(axis=1).astype('str')
progress_table.fillna('', inplace=True)
# separate concatenated values for final display
details = progress_table["full_details"].str.split("__", expand = True)
progress_table.insert(1, "full name", details[0], allow_duplicates = False)
progress_table.insert(2, "staff", details[1], allow_duplicates = False)
progress_table.insert(3, "email", details[2], allow_duplicates = False)
progress_table.insert(4, "joined", details[3], allow_duplicates = False)
progress_table.insert(6, "attendance in last 15 weeks", attendance, allow_duplicates = False)
progress_table.insert(7, "Max lesson entered", maxLesson, allow_duplicates = False)
progress_table=progress_table.drop(columns=["userID","full_details"], axis=1)
cols=progress_table.columns[0:7].values.tolist()+all_week_names # sort week ranges by order
progress_table = progress_table[cols]

#Display branch summary table
print("Branch report for "+str(df_branch["branchName"].iloc[0]))

#Display branch summary graph
# Generate graph
table_totals.iloc[1:-1,:].transpose().plot(kind='bar', figsize=(40,10))
current_ax=plt.gca()

x=table_totals.transpose().reset_index().reset_index()["level_0"]
y= table_totals.transpose().reset_index().reset_index()["Total participants+staff"]

table_totals.iloc[0,:].transpose().plot(ax=current_ax, color='r')
for i,j in zip(x,y):
    current_ax.annotate(str(j),xy=(i,j))


plt.grid(True, which='both', axis='y')
plt.xticks(rotation=90)
plt.rcParams.update({'font.size': 16})

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x,p(x),"r--")
current_ax.legend([table_totals.index.values.tolist()[0],"Trendline (Total P+S)"]+table_totals.index.values.tolist()[1:-1])

#Display branch member activity table
print(progress_table)