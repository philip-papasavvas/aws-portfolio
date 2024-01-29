"""
Created on: 14 Dec 2023
Script for cleaning data
"""
import datetime


def increment_date_by_day(
        date_in: str,
        is_reverse: bool = True
) -> str:
    """
    Helper function to increment (back or forward) a date in time, expected format YYYY-MM-DD.
    By default, it will go back in time one increment
    """
    date_dt = datetime.datetime.strptime(date_in, '%Y-%m-%d')
    sign = -1 if is_reverse else 1
    date_out = date_dt + datetime.timedelta(days=sign * 1)

    return str(date_out)


if __name__ == '__main__':
    pass
