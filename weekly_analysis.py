################################################
# Performs the analysis required for each graph
################################################

import pandas as pd
import datetime as dt
from retriev_users_with_roles import retrieve_users_with_roles
import numpy as np
import itertools

## Add role type to data
def add_role(data, sql_filename, user_specific_dir):
    role_data, fields=roles_as_dummy(sql_filename, user_specific_dir)
    for col in role_data:
        if col == fields[0]:
            role_data.rename(columns={col:"user"})
        elif col == "team_member" or col=="participant":
            continue
        else:
            role_data=role_data.drop(col, axis=1)

    data_with_roles=data.set_index('userID').join(role_data.set_index('user_ID'))
    ## If File is used in place of sql, replace previous line which this line
    # data_with_roles = data.set_index('userID').join(role_data.set_index('user'))
    data_with_roles = data_with_roles.reset_index(drop=False)
    data_with_roles.rename(columns={"index":"userID"})
    role_dict={"team":"team_member", "particip":"participant"}
    role_type_dict={"team":"binary", "particip":"binary"}
    return data_with_roles, role_dict, role_type_dict


## Create role table. This is required because is user has several definitions.
## Returns table where each user is either participant of staff member
def roles_as_dummy(sql_filename, user_specific_dir):
    # # To use pre-dowloaded CSV file in place of SQL query uncomment these
    # roles_data = pd.read_csv("userRoleSubset.csv")
    # roles_data=roles_data.rename(columns={"user_ID":"user"})
    # roles_data=roles_data.rename(columns={"role":"role_name"})
    # roles_data=roles_data.rename(columns={"roleID":"role_id"})
    # roles_data = pd.concat([roles_data, pd.get_dummies(roles_data.role_name)], 1).groupby(["user"]).sum().reset_index()  # Turn role categiry into binary attribute colume and combine so only one entry for each user.
    # End of sql replacment

    role_data, fields_dict, _ =retrieve_users_with_roles(sql_filename, user_specific_dir)
    role_data = role_data.drop(['roleID'], axis=1)
    roles_data = pd.concat([role_data, pd.get_dummies(role_data[fields_dict["role_name"]])], 1).groupby(fields_dict["user"]).sum().reset_index()  # Turn role categiry into binary attribute colume and combine so only one entry for each user.
    fields = roles_data.columns
    # TODO: Remove NG users in sql query level

    # #Remove team members from appearing as participants
    roles_data['participant'] = np.where(roles_data['team_member'] == 1, 0, roles_data['participant'])

    for column in roles_data.columns:
        if column != fields[0]:
            roles_data[column] = roles_data[column].astype('bool')

    return roles_data, fields


## Cleans data so only one entery exists for each unique user on each distinct day
def remove_user_duplicates(data, user_col, lesson_date_col):
    data["userLessonDate"] = data[user_col].astype(str) + " " + data[lesson_date_col]
    data.drop_duplicates(subset="userLessonDate", keep='first', inplace=True)
    data=data.drop(columns=["userLessonDate"])
    return data


## Counts active users by branch
## Returns this count for each week in date range
def activity_by_branch_counter(data, branch_col, activity_col, week_start, week_end):
    for i in range(len(week_start)):
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


## Count staff, non staff and tot in a given series
def populus_counter(data, staff_col, particip_col, week_mask):
    total = week_mask.sum()
    staff = data[staff_col][week_mask].sum()
    particip_col = data[particip_col][week_mask].sum()
    total = staff + particip_col
    return total, staff, particip_col


## Count staff, non staff and tot in series
## returns this count for each week in date range
def populus_counter_by_weeks(data, staff_col, particip_col, activity_col, week_start, week_end):
    for i in range(len(week_start)):
        temp_dict = {}
        mask = (week_start[i] <= data[activity_col]) & (data[activity_col] <= week_end[i])
        [total, staff, non_staff] = populus_counter(data, staff_col, particip_col, mask)
        start = dt.datetime.strptime(week_start[i], '%Y-%m-%d')
        end = dt.datetime.strptime(week_end[i], '%Y-%m-%d')
        col_name = str(start.strftime('%d')) + "/" + str(start.strftime('%m')) + "/" + str(
            start.strftime('%y')) + "-" + str(end.strftime('%d')) + "/" + str(end.strftime('%m')) + "/" + str(
            end.strftime('%y'))
        temp_dict[col_name] = [non_staff, staff, total]
        temp_dataframe = pd.DataFrame(temp_dict)
        temp_dataframe = temp_dataframe.set_index(
            [["Participants Only", "Team Only", "Team + Participants"]])
        # temp_dataframe = temp_dataframe.set_index([["participents","staff","tot"]])
        if i == 0:
            populus_by_weeks = pd.DataFrame(temp_dataframe)
        else:
            populus_by_weeks = pd.concat([populus_by_weeks, temp_dataframe],
                                         ignore_index=False, axis='columns')
    return populus_by_weeks

## Count active users by selected track opening vs. other track openings by branch
## Returns this count for each week in date range
def activity_this_track_opening_by_branch(data, registration_col, activity_col, branch_col, reg_start, reg_end,
                                week_start_list, week_end_list):
    results = [" "]
    # Convert list entries  from string to datetime
    week_end_list=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_end_list]
    week_start_list=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_start_list]
    reg_end = dt.datetime.combine(reg_end[0].to_pydatetime().date(), dt.datetime.min.time())
    reg_start = dt.datetime.combine(reg_start[0].to_pydatetime().date(), dt.datetime.min.time())
    # Set names to be used throughout
    reg_name=str(reg_end.month) + "/" + str(reg_end.year)

    # Loop on each week
    for i in range(len(week_start_list)):
        # Set names to be used later
        col_name = str(week_start_list[i].day) + "/" + str(week_start_list[i].month) + "/" + str(
             week_start_list[i].year) + "-" + str(week_end_list[i].day) + "/" + str(week_end_list[i].month)+ "/" + str(week_end_list[i].year)

        mask1 = (week_start_list[i] <= data[activity_col]) & (data[activity_col] <= week_end_list[i])
        # Get registration dates for all those who were active in that week and count them
        active_in_range = data[registration_col][mask1]
        results.append(mask1.sum())

        branch_in_range1 = data[branch_col][mask1].reset_index(drop=True)

        temp_dataframe1=branch_in_range1.value_counts().to_frame()
        temp_dataframe1.columns = [col_name+" Total"]

        # Get those who were active in that week and registred in selected range
        reg_start_list= pd.Series(itertools.repeat(reg_start, len(active_in_range)))
        reg_end_list = pd.Series(itertools.repeat(reg_end, len(active_in_range)))
        mask2 = (reg_start_list.reset_index(drop=True)<= active_in_range.reset_index(drop=True) ) & (active_in_range.reset_index(drop=True)  <= reg_end_list.reset_index(drop=True))
        results.append(mask2.sum())
        # Get branches those who were active in that week and count them
        branch_in_ranges2 = branch_in_range1[mask2]
        temp_dataframe2=branch_in_ranges2.value_counts().to_frame()
        temp_dataframe2.columns = [col_name+" From "+reg_name+" track opening"]

        # Get those who were active in that week and did not registred in selected range
        mask3 = ~mask2
        results.append(mask3.sum())
        branch_in_ranges3 = branch_in_range1[mask3]
        temp_dataframe3=branch_in_ranges3.value_counts().to_frame()
        temp_dataframe3.columns = [col_name+" Pre-existing"]

        if i == 0:
            activity_by_branch_all = pd.DataFrame(temp_dataframe1)
            activity_by_branch_from_track_opening = pd.DataFrame(temp_dataframe2)
            activity_by_branch_not_from_track_opening = pd.DataFrame(temp_dataframe3)
        else:
            activity_by_branch_all = pd.concat([activity_by_branch_all, temp_dataframe1],
                                           ignore_index=False, axis='columns')
            activity_by_branch_from_track_opening = pd.concat([activity_by_branch_from_track_opening, temp_dataframe2],
                                           ignore_index=False, axis='columns')
            activity_by_branch_not_from_track_opening = pd.concat([activity_by_branch_not_from_track_opening, temp_dataframe3],
                                           ignore_index=False, axis='columns')

    #Create final dataframe
    ind_list1=list(activity_by_branch_all.index)
    ind_list2=list(activity_by_branch_from_track_opening.index)
    ind_list3=list(activity_by_branch_not_from_track_opening.index)
    all_ind=np.unique(ind_list1+ind_list2+ind_list3)
    final_df = pd.DataFrame(index=all_ind)

    empty_series = pd.DataFrame([" "]*len(all_ind),index=all_ind)
    empty_series=empty_series.rename(columns={0: "Accepted to "+reg_name+" track opening"})

    final_df = pd.concat([final_df, empty_series],
                         ignore_index=False, axis='columns')

    for k in range(activity_by_branch_all.shape[1]):
        final_df = pd.concat([final_df, activity_by_branch_all.iloc[:,k]],
                                           ignore_index=False, axis='columns')
        final_df = pd.concat([final_df, activity_by_branch_from_track_opening.iloc[:,k]],
                                           ignore_index=False, axis='columns')
        final_df = pd.concat([final_df, activity_by_branch_not_from_track_opening.iloc[:,k]],
                                           ignore_index=False, axis='columns')

    # Formating branch names
    for ind_name in final_df.index:
        old_ind_name = ind_name
        new_ind_name = ind_name[0].upper()
        new_ind_name = new_ind_name + ind_name[1:]
        final_df = final_df.rename(index={old_ind_name: new_ind_name})
    final_df = final_df.sort_index(ascending=True)
    final_df = final_df.fillna(0)

    added_name="All Branches"
    results_df = pd.DataFrame(results)
    results_df = results_df.rename(columns={0: added_name})
    results_df.index=list(final_df.columns)

    final_df=results_df.transpose().append(final_df)

    final_df.iloc[:,1:]=final_df.iloc[:,1:].astype(int)

    return final_df, reg_name


## Count active users by selected track opening vs. other track openings
## Returns this count for each week since the track opening
def activity_this_track_opening(data, registration_col, activity_col, reg_start, reg_end,
                                week_start_list, week_end_list):
    week_end_list=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_end_list]
    week_start_list=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_start_list]
    reg_name=str(reg_end[0].month) + "/" + str(reg_end[0].year)
    cols = ['Total (new + existing)', 'New from ' + reg_name,
               'Pre-existing participants']
    result_df = pd.DataFrame(columns=cols)
    reg_end = dt.datetime.combine(reg_end[0].to_pydatetime().date(), dt.datetime.min.time())
    reg_start = dt.datetime.combine(reg_start[0].to_pydatetime().date(), dt.datetime.min.time())
    # data[activity_col]=[dt.datetime.strptime(date, '%Y-%m-%d') for date in data[activity_col]]
    for i in range(len(week_start_list)):
        results = []
        mask1= (week_start_list[i] <= data[activity_col]) & (data[activity_col] <= week_end_list[i])
        active_in_range = data[registration_col][mask1]
        # week_end_list = [dt.strptime(date, '%Y-%m-%d') for date in active_in_range]

        # All active in week count
        results.append(mask1.sum())
        # All active who registered in registration selected for comparison
        reg_start_list= pd.Series(itertools.repeat(reg_start, len(active_in_range)))
        reg_end_list = pd.Series(itertools.repeat(reg_end, len(active_in_range)))
        mask2 = (reg_start_list.reset_index(drop=True)<= active_in_range.reset_index(drop=True) ) & (active_in_range.reset_index(drop=True)  <= reg_end_list.reset_index(drop=True))
        results.append(mask2.sum())
        results.append(mask1.sum() - mask2.sum())
        df=pd.Series(results,index=cols).to_frame()
        result_df=pd.concat([result_df, df.transpose()], axis=0)
        result_df=result_df.reset_index(drop=True)
    return result_df, reg_name


## Count active users by when they began
## Returns this count for each week in date range
def activity_by_track_opening_counter(data, registration_col, activity_col, reg_start_date_list, reg_end_date_list,
                                      week_start, week_end):
    week_start=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_start]
    week_end=[dt.datetime.strptime(date, '%Y-%m-%d') for date in week_end]
    temp_dict = {}
    activity_by_track_opening_count = pd.DataFrame()
    for k in range(len(reg_start_date_list)):
        registered_in_range = []
        mask = (reg_start_date_list[k] <= pd.to_datetime(data[registration_col])) & (pd.to_datetime(data[registration_col]) <= reg_end_date_list[k])
        registered_in_range = data[activity_col][mask]
        temp_dataframe = pd.DataFrame()
        for i in range(len(week_start)):
            mask = (week_start[i] <= registered_in_range) & (registered_in_range <= week_end[i])
            start = week_start[i]
            end = week_end[i]
            if not isinstance(week_start[i], pd.Timestamp) and not isinstance(week_start[i], dt.datetime):
                start = dt.datetime.strptime(week_start[i], '%Y-%m-%d')
            if not isinstance(week_end[i], pd.Timestamp) and not isinstance(week_end[i], dt.datetime):
                end = dt.datetime.strptime(week_end[i], '%Y-%m-%d')
            col_name=str(start.strftime('%d'))+"/"+ str(start.strftime('%m'))+"/"+ str(start.strftime('%y')) +"-"+str(end.strftime('%d'))+"/"+str(end.strftime('%m'))+"/"+str(end.strftime('%y'))
            temp_dict[col_name]=[mask.sum()]
        temp_dataframe=pd.DataFrame(temp_dict)
        track_opening_name= str(reg_end_date_list[k].strftime('%B')) + " " + str(reg_end_date_list[k].strftime('%y'))
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
                temp_list=[]
                data[fields[key]] = pd.to_datetime(data[fields[key]], format='%Y-%m-%d')
            except:
                print("%s column cannot be converted to from Y-m-d" % key)
        else:
            continue
    return data
