import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime as dt
import pandas as pd

## Get registration dates from when track open once each quarter
def quarterly_reg_dates(start_limit, end_monthly_opening):
    quarterly_track_opening = {
        "May18": dt.datetime(2018, 5, 6),
        "Aug18": dt.datetime(2018, 8, 5),
        "Nov18": dt.datetime(2018, 11, 4),
        "Feb19": dt.datetime(2019, 2, 3),
        "May19": dt.datetime(2019, 5, 12),
        "Aug19": dt.datetime(2019, 8, 4),
        "Nov19": dt.datetime(2019, 11, 3),
        "Mar19": dt.datetime(2020, 3, 18)
    }
    registration_quarterly_ending_list = [quarterly_track_opening[key] for key in quarterly_track_opening]
    registration_quarterly_ending_series = pd.Series(registration_quarterly_ending_list)
    mask = (start_limit <= registration_quarterly_ending_series ) & (registration_quarterly_ending_series <= end_monthly_opening)
    registration_quarterly_ending_list=registration_quarterly_ending_series[mask]
    registration_quarterly_beginning_list=[]
    for k in registration_quarterly_ending_series:
        registration_quarterly_beginning_list.append(k-dt.timedelta(days=14))
    # registration_quarterly_beginning_list = registration_quarterly_ending - dt.timedelta(days=14)
    # registration_quarterly_beginning_list = [d - dt.timedelta(days=14) for d in registration_quarterly_ending]
    return registration_quarterly_beginning_list, registration_quarterly_ending_series

## Generate registration dates from when track opened each month
def monthly_reg_dates(start_limit, end_limit):
    registration_monthly_beginning_list=[dt.datetime(d.year, d.month, 1) for d in rrule.rrule(rrule.MONTHLY, dtstart=start_limit, until=end_limit)]
    regitration_monthly_ending_list=[d+dt.timedelta(days = 13) for d in registration_monthly_beginning_list]
    return registration_monthly_beginning_list, regitration_monthly_ending_list

#3 Get registration dates relevant for given date range
def track_opening_start_end(start_limit, end_limit):
    # First user was created in sheconnect on 2016-07-19
    # Track opening every month occurred since then until August 2018
    # Quarterly track openings (every 3 months) from then until now
    sheconnect_opening=dt.datetime(2016,7,1)
    end_monthly_opening=dt.datetime(2016,8,1)
    end_quarterly_opening=dt.datetime.now()
    if start_limit < sheconnect_opening:
        print("Please note earliest date in system is 19/7/2016")
        start_limit=sheconnect_opening
    if end_quarterly_opening < end_limit:
        print("Please note latest date possible is current date")
        end_limit=end_quarterly_opening
    if sheconnect_opening <= start_limit and end_limit <= end_monthly_opening:
        [reg_start_dates, reg_end_dates] = monthly_reg_dates(start_limit, end_limit)
    elif end_monthly_opening <= start_limit and end_limit <= end_quarterly_opening:
        [reg_start_dates, reg_end_dates] = quarterly_reg_dates(start_limit, end_limit)
    elif end_monthly_opening <= start_limit and  end_monthly_opening <= end_limit and end_limit <= end_quarterly_opening:
        [reg_start_monthly, reg_end_monthly] = monthly_reg_dates(start_limit, end_monthly_opening)
        [reg_start_quarterly, reg_end_quarterly] = quarterly_reg_dates(end_monthly_opening, end_quarterly_opening)
        reg_start_dates=reg_start_monthly.append(reg_start_quarterly)
        reg_end_dates= reg_end_monthly.append(reg_end_quarterly)
    return reg_start_dates, reg_end_dates


## Get start and end dates for each week in date range
def week_date_start_end(start_limit, end_limit):
    if not isinstance(start_limit, dt.datetime):
        start_limit=dt.datetime(start_limit,1,1)
    if not isinstance(end_limit, dt.datetime):
        end_limit=dt.datetime(end_limit,12,31)
    rule_sunday = rrule.rrule(rrule.WEEKLY,byweekday=relativedelta.SU,dtstart=start_limit)
    sundays=rule_sunday.between(start_limit,end_limit,inc=True)
    saturdays=[d+dt.timedelta(days = 6) for d in sundays]
    start_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in sundays]
    end_week_dates=[dt.datetime.strftime(d, '%Y-%m-%d') for d in saturdays]
    return start_week_dates, end_week_dates
