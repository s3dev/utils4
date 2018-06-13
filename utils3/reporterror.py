# -*- coding: utf-8 -*-
"""
:Purpose:   This module is designed to report program errors to the
            console and/or a log file, using the :class:`~log.Log`
            class.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

"""

def reporterror(error, logevent=False, logfilepath='c:/temp/reporterror.log'):
    """Report an error, derived from the built-in Exception object.

    Args:
        error (Exception): Python Exception object from the built-in
            try/except error handler.  Refer to the use example below.
        logevent (bool): Send the error to a log file.
        logfilename (str): Full path to the log file.

    Note:
        The ``logevent`` parameter assumes the log file exists and the
        header is already written.

        For general logging help, you can use the :class:`~log.Log`
        class which is built into ``utils3``.

    :Example:
        Here is an example of how to use the error reporter::

            from utils3 import reporterror

            try:
                # SOMETHING BAD HAPPENS HERE ...
                1/0
            except Exception as err:
                # SEND ERROR TO REPORTERROR METHOD
                reporterror.reporterror(err)

        And the output looks like this::

            ERROR:  division by zero
            TYPE:   <class 'ZeroDivisionError'>
            FUNC:   <module>
            LINE:   2
            CMD:    1/0

    """
    # BUILT-IN IMPORTS
    import sys
    import traceback
    # SELF-DEPENDENT IMPORTS
    from utils3.log import Log

    # GET TRACEBACK OBJECTS
    exc_type, _, exc_tb = sys.exc_info()
    _, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]

    # USER NOTIFICATION
    print('')
    print('ERROR:\t%s'  % error)
    print('TYPE:\t%s'   % exc_type)
    print('FUNC:\t%s'   % func_name)
    print('LINE:\t%s'   % line_num)
    print('CMD:\t%s'    % text)
    print('')

    # LOG THE ERROR
    if logevent:
        # SETUP THE LOGGER
        logger = Log(filepath=logfilepath)
        # LOG ERROR
        logger.write(text='ERROR: %s; CMD: %s; METHOD: %s; LINE: %s' %
                     (error, text, func_name, line_num))

    # CLEANUP
    del (exc_type, exc_tb)
