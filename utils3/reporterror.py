"""------------------------------------------------------------------------------------------------
Program:    reporterror
Platform:   Windows / Linux
Purpose:    Module designed to report program errors to the console
            and/or a log file, using the utils.log Log() class.

Dependents: log
            sys
            traceback

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > import utils3.reporterror as reporterror
            >
            > try:
            >   stuff here ...
            > except Exception as err:
            >   # SEND ERROR TO REPORTERROR METHOD
            >   reporterror.reporterror(err)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
------------------------------------------------------------------------------------------------"""


# ----------------------------------------------------------------------
def reporterror(error, logevent=False,
                logfilepath='c:/temp/reporterror.log'):
    """
    Report an error, using the Exception object.

    DESIGN:
    Module designed to handle error reporting and logging.

    PARAMETERS:
        - error
        Exception from the error handler; refer to the USE section.
        - logevent (default=False)
        Send the error to a log file.
        Note: use of this command assumes the log file is already
        created, and the header is already written.
        - logfilename (default='c:/temp/reporterror.log')
        File path to the log file.

    USE:
    > try:
    >     stuff here ...
    > except Exception as err:
    >     # REPORT / LOG ERROR
    >     reporterror.reporterror(err)
    """

    # BUILT-IN IMPORTS
    import sys
    import traceback

    # SELF-DEPENDENT IMPORTS
    import utils3.log as log

    # GET TRACEBACK OBJECTS
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]

    # USER NOTIFICATION
    print('')
    print('ERROR:\t%s'  % error)
    print('TYPE:\t%s'   % exc_type)
    print('FUNC:\t%s'   % func_name)
    print('LINE:\t%s'   % line_num)
    print('CMD:\t%s'    % text)

    # LOG ERROR
    if logevent:
        # SETUP THE LOGGER
        _log = log.Log(filepath=logfilepath)
        # LOG ERROR
        _log.write(text='ERROR: %s; CMD: %s; METHOD: %s; LINE: %s' %
                   (error, text, func_name, line_num))

    # CLEANUP
    del (exc_type, exc_obj, exc_tb)
