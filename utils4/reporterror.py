#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module is designed to report program errors to the
            console and/or a log file, using the :class:`~log.Log`
            class.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:   For a usage example, refer to the :meth:`~reporterror` method's
            docstring.

"""
# pylint: disable=multiple-statements

import sys
import traceback
try:
    from .log import Log
except ImportError:
    from utils4.log import Log


if 'linux' in sys.platform.lower(): _PATH = '/tmp/reporterror.log'
elif 'win' in sys.platform.lower(): _PATH = 'c:/temp/reporterror.log'  # pragma: nocover
else: _PATH = None  # pragma: nocover


def reporterror(error: Exception, logevent=False, logfilepath=_PATH):
    """Report an error, derived from the passed ``Exception`` object.

    Args:
        error (Exception): Python ``Exception`` object from the built-in
            try/except error handler.  Refer to the use example below.
        logevent (bool, optional): Send the error to a log file.
            Defaults to False.
        logfilename (str, optional): Full path to the log file. Defaults to:

            - **Linux**: ``'/tmp/reporterror.log'``
            - **Windows**: ``'c:/temp/reporterror.log'``
            - **Other**: ``None``

    Note:
        The ``logevent`` parameter assumes the log file exists and the
        header is already written.

        For general logging help, you can use the :class:`~log.Log`
        class which is built into ``utils4``.

    :Example:

        Report a simple error to the terminal::

            >>> from utils4.reporterror import reporterror

            >>> try:
            >>>     1/0  # Force a known error.
            >>> except Exception as err:
            >>>     reporterror(err)

        Output::

            ERROR:  division by zero
            TYPE:   <class 'ZeroDivisionError'>
            MODU:   <./module/with/error.py>
            FUNC:   <func_name>
            LINE:   2
            CMD:    1/0


        Report a simple error to the terminal and create a log file entry::

            >>> from utils4.reporterror import reporterror

            >>> try:
            >>>     1/0  # Force a known error.
            >>> except Exception as err:
            >>>     reporterror(err, logevent=True, logfilepath='/tmp/errors.log')

        .. tip::
            **Reminder:** The log file must already exist.

            For help with the :mod:`utils4.log` module, please refer to the
            documentation here: :class:`~log.Log`.

    """
    exc_type, _, exc_tb = sys.exc_info()
    fnam, line, func, text = traceback.extract_tb(exc_tb)[-1]
    msg = (f'\n'
           f'ERROR:\t{error}\n'
           f'TYPE:\t{exc_type}\n'
           f'MODU:\t{fnam}\n'
           f'FUNC:\t{func}\n'
           f'LINE:\t{line}\n'
           f'CMD:\t{text}\n')
    print(msg)
    if all([logevent, logfilepath]):
        logger = Log(filepath=logfilepath, sep=',')
        msg = f'ERROR: {error}; CMD: {text}; MODULE: {fnam}; FUNC: {func}; LINE: {line}'
        logger.write(msg)
    del (exc_type, exc_tb)
