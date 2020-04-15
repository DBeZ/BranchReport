import pandas as pd
import calendar
import datetime as dt


## Clean data so only one entery exists for each uniqe user on each distinct day
def remove_user_duplicates(data, user_col, lesson_date_col):
    data["userLessonDate"] = data[user_col].astype(str) + " " + data[lesson_date_col]
    data.drop_duplicates(subset="userLessonDate", keep='first', inplace=True)
    data.drop(columns=["userLessonDate"])
    return data


## Counts active users by branch
## returns this count for each week in date range
def activity_by_branch_counter(data, branch_col, activity_col, week_start, week_end):
    for i in range(len(week_start)):
        temp_dataframe = pd.DataFrame()
        activity_count_by_branch = pd.Series()
        mask = (week_start[i] <= data[activity_col]) & (data[activity_col] <= week_end[i])
        activity_count_by_branch = data[branch_col][mask].value_counts()
        start = dt.datetime.strptime(week_start[i], '%Y-%m-%d')
        end = dt.datetime.strptime(week_end[i], '%Y-%m-%d')
        col_name = str(start.strftime('%d')) + "/" + str(start.strftime('%m')) + "/" + str(
            start.strftime('%y')) + "-" + str(end.strftime('%d')) + "/" + str(end.strftime('%m')) + "/" + str(
            end.strftime('%y'))
        temp_dataframe = pd.DataFrame(activity_count_by_branch)
        temp_dataframe.columns = [col_name]
        if i == 0:
            activity_by_branch = pd.DataFrame(temp_dataframe)
        else:
            activity_by_branch = pd.concat([activity_by_branch, temp_dataframe],
                                           ignore_index=False, axis='columns')
    # Formating branch names
    for ind_name in activity_by_branch.index:
        old_ind_name = ind_name
        new_ind_name = ind_name[0].upper()
        new_ind_name = new_ind_name + ind_name[1:]
        activity_by_branch = activity_by_branch.rename(index={old_ind_name: new_ind_name})
    activity_by_branch = activity_by_branch.sort_index(ascending=True)
    # Formating values
    activity_by_branch = activity_by_branch.fillna(0)
    activity_by_branch = activity_by_branch.astype(int)
    return activity_by_branch


## Count staff, non staff and tot in series
def populus_counter(data, staff_col, week_mask):
    total = week_mask.sum()
    staff = data[staff_col][week_mask].sum()
    non_staff = int(total - staff)
    return total, staff, non_staff


## Count staff, non staff and tot in series
## returns this count for each week in date range
def populus_counter_by_weeks(data, staff_col, activity_col, week_start, week_end):
    for i in range(len(week_start)):
        temp_dict = {}
        mask = (week_start[i] <= data[activity_col]) & (data[activity_col] <= week_end[i])
        [total, staff, non_staff] = populus_counter(data, staff_col, mask)
        start = dt.datetime.strptime(week_start[i], '%Y-%m-%d')
        end = dt.datetime.strptime(week_end[i], '%Y-%m-%d')
        col_name = str(start.strftime('%d')) + "/" + str(start.strftime('%m')) + "/" + str(
            start.strftime('%y')) + "-" + str(end.strftime('%d')) + "/" + str(end.strftime('%m')) + "/" + str(
            end.strftime('%y'))
        temp_dict[col_name] = [non_staff, staff, total]
        temp_dataframe = pd.DataFrame(temp_dict)
        temp_dataframe = temp_dataframe.set_index(
            [["משתתפות בלבד", "חברות צוות בלבד", "חברות צוות" + " + " + "משתתפות"]])
        # temp_dataframe = temp_dataframe.set_index([["participents","staff","tot"]])
        if i == 0:
            populus_by_weeks = pd.DataFrame(temp_dataframe)
        else:
            populus_by_weeks = pd.concat([populus_by_weeks, temp_dataframe],
                                         ignore_index=False, axis='columns')
    return populus_by_weeks


## Count active users by when they began
## returns this count for each week in date range
def activity_by_track_opening_counter(data, registration_col, activity_col, reg_start_date_list, reg_end_date_series,
                                      week_start, week_end):
    temp_dict = {}
    activity_by_track_opening_count = pd.DataFrame()
    for k in range(len(reg_start_date_list)):
        registered_in_range = []
        mask = (reg_start_date_list[k] <= data[registration_col]) & (data[registration_col] <= reg_end_date_series[k])
        registered_in_range = data[activity_col][mask]
        temp_dataframe = pd.DataFrame()
        for i in range(len(week_start)):
            mask = (week_start[i] <= registered_in_range) & (registered_in_range <= week_end[i])
            start = dt.datetime.strptime(week_start[i], '%Y-%m-%d')
            end = dt.datetime.strptime(week_end[i], '%Y-%m-%d')
            col_name=str(start.strftime('%d'))+"/"+ str(start.strftime('%m'))+"/"+ str(start.strftime('%y')) +"-"+str(end.strftime('%d'))+"/"+str(end.strftime('%m'))+"/"+str(end.strftime('%y'))
            temp_dict[col_name]=[mask.sum()]
        temp_dataframe=pd.DataFrame(temp_dict)
        track_opening_name=str(reg_end_date_series[k].strftime('%B'))+" "+str(reg_end_date_series[k].strftime('%y'))
        temp_dataframe = temp_dataframe.set_index([[track_opening_name]])
        if k==0:
            activity_by_track_opening_count = pd.DataFrame(temp_dataframe)
        else:
            activity_by_track_opening_count=pd.concat([activity_by_track_opening_count,temp_dataframe], ignore_index=False)
    return activity_by_track_opening_count

# Convert values in each column to the right datatype
def column_converter(data, fields, datatpypes):
    for key in fields:
        if datatpypes[key]=="binary":
            try:
                data[fields[key]] = data[fields[key]].astype('bool')
            except:
                print("%s column cannot be converted to boolean" % key)
        elif datatpypes[key] == "int":
            try:
                data[fields[key]]= pd.to_numeric(data[fields[key]])
            except:
                print("%s column cannot be converted to int" % key)
        elif datatpypes[key] == "datetime":
            try:
                data[fields[key]] = pd.to_datetime(data[fields[key]], format='%Y/%m/%d')
            except:
                print("%s column cannot be converted to d/m/Y" % key)
        else:
            continue
    return data
