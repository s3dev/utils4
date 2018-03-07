"""------------------------------------------------------------------------------------------------
Program:    reporterror
Platform:   Windows / Linux
Purpose:    Module designed to report program errors to the console and/or a log file, using the
            utils3.log Log() class.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > from utils3 import reporterror
            >
            > try:
            >   do bad stuff here ...
            > except Exception as err:
            >   # SEND ERROR TO REPORTERROR METHOD
            >   reporterror.reporterror(err)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
07.03.18    J. Berendt      1.0.1       Minor code cleaning.
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
    Note: Use of this command assumes the log file is already
    created, and the header is already written.
    - logfilename (default='c:/temp/reporterror.log')
    File path to the log file.

    USE:
    > from utils3 import reporterror
    > try:
    >     do bad stuff here ...
    > except Exception as err:
    >     # REPORT / LOG ERROR
    >     reporterror.reporterror(err)
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
