import pandas as pd
import calendar
import datetime as dt

## Clean data so only one entery exists for each uniqe user
def remove_user_duplicates(data, user_col):
    data.drop_duplicates(subset=user_col, keep=False, inplace=True)
    return data

## Count staff and non staff in data
def populus_counter(data, staff_col):
    total=data.shape[0]
    staff=int(data[staff_col].sum())
    non_staff=int(total-staff)
    return total, staff, non_staff

## Count active users by when they began
def activity_by_track_opening_counter(data, registration_col, activity_col, reg_start_date_list, reg_end_date_series, week_start, week_end):
    temp_dict = {}
    activity_by_track_opening_count=pd.DataFrame()
    for k in range(len(reg_start_date_list)):
        registered_in_range=[]
        mask = (reg_start_date_list[k] <= data[registration_col]) & (data[registration_col] <= reg_end_date_series[k])
        registered_in_range=data[activity_col].mask(mask)
        temp_dataframe = pd.DataFrame()
        for i in range(len(week_start)):
            mask = (week_start[i] <= registered_in_range) & (registered_in_range <= week_end[i])
            start=dt.datetime.strptime(week_start[i],'%Y-%m-%d')
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
                data[fields[key]] = pd.to_datetime(data[fields[key]], format='%d/%m/%Y')
            except:
                print("%s column cannot be converted to d/m/Y" % key)
        else:
            continue
    return data
