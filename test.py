import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime as dt
import pandas as pd

def quarterly_reg_dates():
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
    registration_quarterly_ending = [quarterly_track_opening[key] for key in quarterly_track_opening]
    registration_quarterly_ending = pd.Series(registration_quarterly_ending)
    mask = (dt.datetime(2019, 5, 12) <= registration_quarterly_ending ) & (registration_quarterly_ending <= dt.datetime(2020, 3, 18))
    registration_quarterly_ending=registration_quarterly_ending[mask]
    print("end test")

quarterly_reg_dates()