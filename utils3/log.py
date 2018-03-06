"""------------------------------------------------------------------------------------------------
Program:    log
Purpose:    This is a small class module designed as a central log file creator.

            The calling program is responsible for passing the proper arguments to create the
            log file header.  (i.e.: printheader=True, headertext='some,header,text,here')

            It is suggested to call Log at program startup, with the printheader parameter
            set to True.  This is safe because if the log file already exists, the header will
            not be re-written.  However if the log file does not exist, it will be created with a
            header.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > from utils3.log import Log
            > header = 'COMMENT,TYPE,VAL,UNIT'
            > logger = Log(filepath='path/to/file.log', printheader=True, headertext=header)
            >
            > logger.write(text='most cows can just over the moon,Fact,94.2,pct')

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
06.03.18    J. Berendt      1.0.1       Minor docstring and use case edits.  pylint (10/10)
------------------------------------------------------------------------------------------------"""

import os
import socket
import getpass
from datetime import datetime as dt

import utils3.reporterror as reporterror


class Log(object):
    """
    DESIGN:
    This is a small and simple log file writer class.

    The calling program is responsible for passing the proper arguments
    to create the log file header.
    (i.e.: printheader=True, headertext='some,header,text,here')

    On class instantiation, validation is performed to determine if the
    log file exists.  If the log file does not exist, a header is
    required before writing to the log file.  These parameters can be
    passed to the class on instantiation, and will be ignored if the
    log file already exists.

    PARAMETERS:
    - filepath
    Full path to the log file.
    - autofill (default=True)
    Auto-fill the log entry with datetime(now), host and username values.
    - printheader (default=False)
    Flag to print the text passed to the headertext parameter asthe log
    file header.
    - headertext (default='')
    Values to be written as the log file header.
    - sep (default=',')
    Separator to be used in the log file.  This separator is used when
    writing the autofill values.

    FILE VALIDATION:
    On class instantiation, tests are performed to ensure the log file
    is being populated in a logical way.
    1) If printheader is False, and the log file does not yet exist,
    the user is notified.
    2) If printheader is True, yet headertext is blank, the user is
    instructed to pass header text.
    3) If printheader is True, yet the log file already exists,
    the header will not be written.

    USE:
    > from utils3.log import Log
    > header = 'COMMENT,TYPE,VAL,UNIT'
    > logger = Log(filepath='path/to/file.log', printheader=True,
                   headertext=header)
    >
    > logger.write(text='most cows can just over the moon,Fact,94.2,pct')
    """

    # ------------------------------------------------------------------
    # INITIALISATION METHOD
    def __init__(self, filepath, autofill=True, printheader=False, headertext='', sep=','):

        # INITIALISE CLASS VARIABLES
        self._filepath  = filepath
        self._autofill  = autofill
        self._sep       = sep
        self._host      = socket.gethostname()
        self._user      = getpass.getuser()
        self._autotext  = ('%s%s%s%s' % (self._host, self._sep, self._user, self._sep)
                           if self._autofill is True else '')

        # VALIDATION
        # TEST THE LOG FILE EXISTS (IF HEADER IS NOT REQUESTED)
        if printheader is False and os.path.exists(self._filepath) is False:
            # NOTIFY USER
            raise UserWarning('The log file does not exist, however a header was not requested. '
                              'A header must be written at the time of log file creation.\n')

        # VALIDATION
        # TEST PRINTHEADER ARGUMENT, TO ENSURE A HEADER STRING IS BEING PASSED >> RAISE ERROR
        if printheader is True and headertext == '':
            # NOTIFY USER
            raise UserWarning('The printheader argument is True, however the headertext string is '
                              'blank. A headertext string must also be supplied.\n')

        # WRITE HEADER
        # TEST TO BE SURE A HEADER SHOULD BE WRITTEN >> PRINT HEADER
        if printheader is True and headertext != '' and os.path.exists(self._filepath) is False:
            # CREATE FILE
            with open(self._filepath, 'a') as f:
                # WRITE HEADER
                f.write(headertext)
                # ADD NEW LING CHARACTER
                f.write('\n')


    # ------------------------------------------------------------------
    # METHOD FOR WRITING TO THE LOG FILE
    def write(self, text):
        """
        Write text to the log file defined at instantiation.

        DESIGN:
        If the autofill argument is True, the current datetime, host
        and username values are written (in that order), ahead of the
        text string provided to the text argument.  The sep parameter
        defined at instantiation, is used to separate these
        auto-populated fields.

        PARAMETERS:
        - text
        Text string to be written to the log.
        Note: If autofill is True - the datetime, host and username
        values will be populated, and *do not* need to be passed in this
        string.

        USE:
        > from utils3.log import Log
        >
        > logger = Log(filepath='path/to/file.log', autofill=True)
        > logger.write(text='just adding some random text to my log')
        """

        try:

            # TEST THAT TEXT IS PASSED >> WRITE TEXT TO LOG
            if text != '':

                # TEST FOR AUTOFILL >> GET / POPULATE TIMESTAMP
                auto_text = '%s%s%s' % (dt.now(),
                                        self._sep,
                                        self._autotext) if self._autofill is True else ''

                # APPEND TEXT TO LOG FILE
                with open(self._filepath, 'a') as f:
                    # WRITE TEXT
                    f.write(auto_text)
                    f.write(text)
                    # ADD NEW LINE CHARACTER
                    f.write('\n')

        except Exception as err:
            # NOTIFICATION
            reporterror.reporterror(err)


    # ------------------------------------------------------------------
    # METHOD FOR WRITING A SINGLE BLANK LINE TO THE LOG FILE
    def write_blank_line(self):
        r"""
        Write a blank line to the log file.

        Note, that the autofill information *is not* written.  This is
        a true blank line, created by writing a '\n' value to the log.

        USE:
        > from utils3.log import Log
        >
        > logger = Log(filepath='path/to/file.log', autofill=True)
        > logger.write_blank_line()
        """

        try:
            # APPEND BLANK LINE TO LOG FILE
            with open(self._filepath, 'a') as f: f.write('\n')

        except Exception as err:
            # NOTIFICATION
            reporterror.reporterror(err)
