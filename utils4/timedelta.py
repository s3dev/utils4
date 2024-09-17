# -*- coding: utf-8 -*-
r"""
:Purpose:   This module handles the time delta calculations.

            Essentially, this module is a soft wrapper around the
            :func:`pandas.DateOffset` class, which handles the time delta
            calculations.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:

    Calculate five months into the future::

        >>> from datetime import datetime as dt  # Imported for demonstration only
        >>> from utils4.timedelta import timedelta

        >>> origin = dt.now()
        >>> result = timedelta(origin=origin, unit='m', value=5)

        >>> print(f'Origin: {origin}', f'Result: {result}', sep='\n')
        Origin: 2022-03-23 14:45:58.974822
        Result: 2022-08-23 14:45:58.974822


    Calculate 55 minutes into the past::

        >>> from datetime import datetime as dt  # Imported for demonstration only
        >>> from utils4.timedelta import timedelta

        >>> origin = dt.now()
        >>> result = timedelta(origin=origin, unit='M', value=-55)

        >>> print(f'Origin: {origin}', f'Result: {result}', sep='\n')
        Origin: 2022-03-23 14:48:43.566826
        Result: 2022-03-23 13:53:43.566826


    Calculate 15 months into the past::

        >>> from datetime import datetime as dt  # Imported for demonstration only
        >>> from utils4.timedelta import timedelta

        >>> origin = dt.now()
        >>> result = timedelta(origin=origin, unit='m', value=-15)

        >>> print(f'Origin: {origin}', f'Result: {result}', sep='\n')
        Origin: 2022-03-23 14:48:59.531170
        Result: 2020-12-23 14:48:59.531170

"""

import pandas as pd
try:
    from .reporterror import reporterror
except ImportError:
    from utils4.reporterror import reporterror


def timedelta(origin, unit, value):
    """Calculate the time delta, of a given unit, from the original value.

    Args:
        origin (datetime.datetime): Original datetime on which the
            time delta is to be calculated.
        unit (str): Time unit to be used. Valid options are:

            - ``'S'``: seconds
            - ``'M'``: minutes
            - ``'H'``: hours
            - ``'d'``: days
            - ``'w'``: weeks
            - ``'m'``: months
            - ``'y'``: years

        value (int): Value of the delta. Can be either a positive or negative
            integer.

    Raises:
        ValueError: If the unit provided is invalid.

    Returns:
        datetime.datetime: A ``datetime.datetime`` object of the calculated
        result.

    """
    units = ['S', 'M', 'H', 'd', 'w', 'm', 'y']
    if not unit in units:
        raise ValueError(f'Invalid unit. Valid units are: {", ".join(units)}\n'
                         'Seconds through years, respectively.')
    try:
        new = None
        if unit == 'S':
            new = origin + pd.DateOffset(seconds=value)
        elif unit == 'M':
            new = origin + pd.DateOffset(minutes=value)
        elif unit == 'H':
            new = origin + pd.DateOffset(hours=value)
        elif unit == 'd':
            new = origin + pd.DateOffset(days=value)
        elif unit == 'w':
            new = origin + pd.DateOffset(weeks=value)
        elif unit == 'm':
            new = origin + pd.DateOffset(months=value)
        elif unit == 'y':
            new = origin + pd.DateOffset(years=value)
    except Exception as err:
        reporterror(err)
    return new
