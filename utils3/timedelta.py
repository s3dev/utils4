# -*- coding: utf-8 -*-
"""
:Purpose:   This module handles the time delta calculations.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
    Example code use::

        from datetime import datetime as dt
        from utils3.timedelta import timedelta

        origin = dt.now()
        # Get the datetime of exactly 1 week ago.
        lastweek = timedelta(origin=origin, unit='w', value=-1)
        print('Origin:', origin)
        print('Last week:', lastweek)

"""

import pandas as pd


def timedelta(origin, unit, value):
    """Calculate a time delta, of a given unit, from the original value.

    Args:
        origin (datetime.datetime): Original datetime on which the
            time delta is to be calculated.
        unit (str): Time unit to be used.  Valid options are:

            - 's' = seconds
            - 'm' = minutes
            - 'h' = hours
            - 'd' = days
            - 'w' = weeks
            - 'M' = months
            - 'y' = years

        value (int): Value of the delta.  Can be either a positive or
            negative integer.

    Returns:
        A ``datetime.datetime`` object of the calculated result.

    """
    new = None
    units = ['s', 'm', 'h', 'd', 'w', 'M', 'y']
    try:
        if unit in units:
            if unit == 's':
                new = origin + pd.DateOffset(seconds=value)
            elif unit == 'm':
                new = origin + pd.DateOffset(minutes=value)
            elif unit == 'h':
                new = origin + pd.DateOffset(hours=value)
            elif unit == 'd':
                new = origin + pd.DateOffset(days=value)
            elif unit == 'w':
                new = origin + pd.DateOffset(weeks=value)
            elif unit == 'M':
                new = origin + pd.DateOffset(months=value)
            elif unit == 'y':
                new = origin + pd.DateOffset(years=value)
        else:
            print('\nTime delta cannot be calculated, the unit is invalid.\n'
                  'Valid units are: {units}'.format(units=units))
    except Exception as err:
        print(err)
    return new
