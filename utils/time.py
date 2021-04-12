from datetime import datetime, timedelta
from dateutil import tz

# Returns datetime tuple of (start_of_this_week, end_of_this_week)
# This can be used for comparisons (with other tz aware datetime structures)
def this_week():
    # Get today at midnight
    today = datetime.now(tz=tz.tzlocal()).replace(hour=0, minute=0, second=0)

    # Take today, subtract the days since monday to get monday at midnight
    week_start = today - timedelta(days=today.weekday())

    # Take monday, add 6 to get sunday at one second before midnight
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return (week_start, week_end)

# Returns datetime tuple of (start_of_last_week, end_of_last_week)
# This can be used for comparisons (with other tz aware datetime structures)
def last_week():
    # Get today at midnight
    today = datetime.now(tz=tz.tzlocal()).replace(hour=0, minute=0, second=0)

    # Take today, subtract the days since monday to get monday at midnight.
    week_start = today - timedelta(days=today.weekday())

    #Subtract a week to get last monday at midnight
    last_week_start = week_start - timedelta(days=7)

    # Take last monday, add 6 to get sunday one second before midnight
    last_week_end = last_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return (last_week_start, last_week_end)
