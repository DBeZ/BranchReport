##################################################
# This function converts a month given in shape
# "May 2019" to a date X months from it
##################################################


import datetime
import calendar
from dateutil.relativedelta import relativedelta

def week_date_range(year):
    calendar_sunday_begin_week = calendar.TextCalendar(calendar.SUNDAY)
    day_dates = datetime.date(year, 1, 1)
    for day_dates in calendar_sunday_begin_week.itermonthdays(year, month):


    for month in range(1, 13):

            if day_dates != 0:
                day = datetime.date(year, month, day_dates)
                if day.weekday() == 6:
                    start_week_date = day
                    day=start_week_date+datetime.timedelta(days=6)
                    if day.weekday() == 6:
                    end_week_date = datetime.date(year, month, 1)

week_date_range(2019)

# Converts given month in format 'may 2019' to date range,
# beginning on the first of that month
# ending on the first of the month of a following month.
# Range between them defined by monthsRangeForward
def month_to_date_range(montWithYear, monthsRangeForward=1):
    year = int(montWithYear.split()[1])
    month = montWithYear.split()[0]
    monthAbbrivDict = {v: k for k, v in enumerate(calendar.month_abbr)}
    month = int(monthAbbrivDict[month])
    mindate = datetime.date(year, month, 1)
    if monthsRangeForward == 1:
        daysInMonth = calendar.monthrange(year, month)
        daysInMonth = daysInMonth[1]
        monthsRangeForward = datetime.timedelta(days=int(daysInMonth))
        maxdate = mindate + monthsRangeForward
    else:
        maxdate = mindate + relativedelta(months=+monthsRangeForward)
    return [mindate, maxdate]

# Converts given year in format "2020" date range,
# beginning on the first of that month
# ending on the first of the month of a following year.
# Range between them defined by yearRangeForward
def year_date_range(year, yearsRangeForward=1):
    yearStart = int(year)
    yearEnd = yearStart + yearsRangeForward-1
    mindate = datetime.date(yearStart, 1, 1)
    maxdate = datetime.date(yearEnd, 12, 31)
    return [mindate, maxdate]


def date_converter(date_options):
    if date_options.split() == 1:
        month_to_date_range(date_options)
    elif date_options.split() == 2:
        month_to_date_range(date_options)
    else:
        print("Date range should be in the format May2019 or 2018")
