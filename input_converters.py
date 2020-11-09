####################################################################################
# Converts inputs into python types, checks dates are legal to sheconnect timeframe
####################################################################################

import datetime as dt
from calendar import month_abbr, monthrange
from re import split
from collections import Counter

## Get compelete number (such as months, years) from user
def ask_num():
    user_input = input()
    while not user_input.isnumeric():
        user_input = input()
    return int(user_input)

## Check years in range are consecutive
def year_range_check(yearRange):
    today = dt.datetime.now()
    if len(yearRange)>2:
        print("Year range should contain start year and end year")
        ask_date_range_year()
    if min(yearRange) < 2016:
        print("Year should be between 2016 and present")
        ask_date_range_year()
    if max(yearRange) > today.year:
        print("Year should be between 2016 and present")
        ask_date_range_year()
    else:
        return yearRange

## Validation that input is yyyy
def year_check(input_val, input_converted, flag):
    if len(input_val) != 1 and len(input_val) != 2:
        print('Year range should be in formate "xxxx-xxxx"')
    else:
        for year in input_val:
            if len(year.split(".")) > 1:
                print("Year should be a whole number")
                break
            else:
                try:
                    int(year)
                except:
                    print("Year should be a whole number")
                    break
                if len(year) == 4:
                    try:
                        input_converted.append(int(year))
                        flag = 1
                    except ValueError:
                        print("Year should be a whole number1")
                        break
                else:
                    print("Year should be 4 digits")
    return input_converted, flag

## Convert month from name to number
def month_to_num_converet(months):
    converted_months=[]
    for month in months:
        month=month.lower()
        monthAbbrivDict = {v: k for k, v in enumerate(month_abbr)}
        c = Counter()
        for k, v in monthAbbrivDict.items():
            c.update({k.lower(): v})
        monthAbbrivDict = c
        month = int(monthAbbrivDict[month])
        if month ==0:
            ask_date_range_month_year()
        converted_months.append(month)
    return converted_months

## Convert month from number to name
def month_to_name_converet(months):
    converted_months=[]
    for month in months:
        month=month_abbr[month]
        if month ==0:
            ask_date_range_month_year()
        converted_months.append(month)
    return converted_months

## Validation input is month short name
def month_check(months, months_converted, flagMonth):
    month_correct=0
    if len(months) != 1 and len(months) != 2:
        print('Range should contain one or two months only')
    else:
        for month in months:
            if month in month_abbr:
                month_correct += 1
        if month_correct==len(months):
            flagMonth=1
        return flagMonth

# Get user input in mmm yyyy or mmm yyyy- mmm yyyy and validate format
def ask_date_range_month_year():
    flagMonth = 0
    flagYear = 0
    input_val = []
    while flagMonth == 0 or flagYear == 0:
        print("Enter time span (Format: Aug 2018 or Aug 2018 - Nov 2019):\n")
        user_input = input()
        input_val = split('\W+', user_input)
        input_converted = []
        if len(input_val) != 2 and len(input_val) != 4:
            print('Range should be in the format "Aug 2018" or "Aug 2018 - Nov 2019"')
        else:
            months=input_val[::2]
            years=input_val[1::2]
            months_converted = []
            years_converted = []
            [years_converted, flagYear] = year_check(years, years_converted, flagYear)
            years_converted = year_range_check(years_converted)
            flagMonth=month_check(months, months_converted, flagMonth)
            months_converted=month_to_num_converet(months)
            min_date = dt.date(years_converted[0], months_converted[0], 1)
            days_in_max_month = monthrange(years_converted[-1], months_converted[-1])
            max_date = dt.date(years_converted[-1], months_converted[-1], days_in_max_month[1])
            return min_date, max_date

# Get user input in yyyy or yyyy-yyyy and validate format
def ask_date_range_year():
    flag = 0
    while flag == 0:
        print("Enter time span (2018 or 2018-2019):\n")
        input_converted = []
        input_val = input()
        input_val = input_val.split("-")
        [input_converted, flag] = year_check(input_val, input_converted, flag)
    [min_date, max_date] =year_range_check(input_converted)
    return min_date, max_date