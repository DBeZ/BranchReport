################################################
# Performs the analysis required for each graph
################################################
# Calander functions which transform dates into
# A) Track openings
# B) Week ranges

import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime as dt
import pandas as pd
from user_specific_extractor import track_openings

## Get registration dates from when track open once each quarter
# Users registered in three weeks before the track opened
def quarterly_reg_dates(start_limit, end_monthly_opening):
    quarterly_track_opening=track_openings("track_openings.txt")
    registration_quarterly_ending_list = [quarterly_track_opening[key] for key in quarterly_track_opening]
    registration_quarterly_ending_series = pd.Series(registration_quarterly_ending_list)
    mask = (start_limit <= registration_quarterly_ending_series ) & (registration_quarterly_ending_series <= end_monthly_opening)

    # If track opening last year was not in the same month
    if not mask.any(): # look for a track opening one month back
        mask1 = (start_limit- relativedelta.relativedelta(months=1) <= registration_quarterly_ending_series) & (
                    registration_quarterly_ending_series <= end_monthly_opening-relativedelta.relativedelta(months=1))
        if not mask1.any(): # look for a track opening one month forward
            mask = (start_limit+ relativedelta.relativedelta(months=1)<= registration_quarterly_ending_series) & (
                    registration_quarterly_ending_series <= end_monthly_opening+relativedelta.relativedelta(months=1))
        else:
            mask=mask1

    registration_quarterly_ending_series=registration_quarterly_ending_series[mask]
    registration_quarterly_beginning_list=[]
    for k in registration_quarterly_ending_series:
        registration_quarterly_beginning_list.append(k-dt.timedelta(days=21))
    # registration_quarterly_beginning_list = registration_quarterly_ending - dt.timedelta(days=14)
    # registration_quarterly_beginning_list = [d - dt.timedelta(days=14) for d in registration_quarterly_ending]
    return registration_quarterly_beginning_list, pd.Series.tolist(registration_quarterly_ending_series)

## Generate registration dates from when track opened each month
# User registered within first two weeks of the month
def monthly_reg_dates(start_limit, end_limit):
    registration_monthly_beginning_list=[dt.datetime(d.year, d.month, 1) for d in rrule.rrule(rrule.MONTHLY, dtstart=start_limit, until=end_limit)]
    regitration_monthly_ending_list=[d+dt.timedelta(days = 13) for d in registration_monthly_beginning_list]
    return registration_monthly_beginning_list, regitration_monthly_ending_list

# Get registration dates relevant for given date range
def track_opening_start_end(start_limit, end_limit):
    # First user was created in sheconnect on 2016-07-19
    # Track opening every month occurred since then until August 2018
    # Quarterly track openings (every 3 months) from then until now
    if not isinstance(start_limit, list) and not isinstance(start_limit, pd.Series):
        if not isinstance(start_limit, dt.datetime):
            start_limit=dt.datetime.combine(start_limit, dt.datetime.min.time())
    else:
        start_limit_new=[]
        for entry1 in start_limit:
            if not isinstance(entry1, dt.datetime):
                start_limit_new.append(dt.datetime.combine(entry1,dt.datetime.min.time()))
        start_limit= pd.Series(start_limit_new)

    if not isinstance(end_limit, list) and not isinstance(end_limit, pd.Series):
        if not isinstance(end_limit, dt.datetime):
            end_limit=dt.datetime.combine(end_limit, dt.datetime.min.time())
    else:
        end_limit_new=[]
        for entry2 in end_limit:
            if not isinstance(entry2, dt.datetime):
                end_limit_new.append(dt.datetime.combine(entry2,dt.datetime.min.time()))
        end_limit= pd.Series(end_limit_new)

    sheconnect_opening=dt.datetime(2016,7,1)
    end_monthly_opening=dt.datetime(2016,8,1)
    end_quarterly_opening=dt.datetime.now()
    if start_limit < sheconnect_opening: # Dates before system opened
        print("Please note earliest date in system is 19/7/2016")
        start_limit=sheconnect_opening
    if end_quarterly_opening < end_limit: # Dates after current date
        print("Please note latest date possible is current date")
        end_limit=end_quarterly_opening
    if sheconnect_opening <= start_limit and end_limit <= end_monthly_opening : # Dates when track opening was each month
        [reg_start_dates, reg_end_dates] = monthly_reg_dates(start_limit, end_limit)
    elif end_monthly_opening <= start_limit and end_limit <= end_quarterly_opening: # Dates when track openings are once in a quarter
        [reg_start_dates, reg_end_dates] = quarterly_reg_dates(start_limit, end_limit)
    elif end_monthly_opening <= start_limit and end_monthly_opening <= end_limit and end_limit <= end_quarterly_opening: #Dates spaning transition from each month to quarterly track openings
        [reg_start_monthly, reg_end_monthly] = monthly_reg_dates(start_limit, end_monthly_opening)
        [reg_start_quarterly, reg_end_quarterly] = quarterly_reg_dates(end_monthly_opening, end_quarterly_opening)
        reg_start_dates=reg_start_monthly.append(reg_start_quarterly)
        reg_end_dates= reg_end_monthly.append(reg_end_quarterly)
    return reg_start_dates, reg_end_dates


## Get start and end dates for each week in date range
# Input - any date range. Output - all week start and week ends in this range.
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
    if not isinstance(end_limit, dt.datetime) and not isinstance(start_limit, dt.date):
        end_limit=dt.datetime(end_limit,12,31)

    start_limit = start_limit - dt.timedelta(days=5) # To account for track openings which happen in the middle of a week
    rule_sunday = rrule.rrule(rrule.WEEKLY,byweekday=relativedelta.SU,dtstart=start_limit)
    sundays=rule_sunday.between(start_limit,end_limit,inc=True)
    saturdays=[d+dt.timedelta(days = 6) for d in sundays]
    start_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in sundays]
    end_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in saturdays]
    return start_week_dates, end_week_dates
