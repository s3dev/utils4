# -*- coding: utf-8 -*-
"""
:Purpose:   This is a small class module designed as a central log file
            creator.

            The calling program is responsible for passing the proper
            arguments to create the log file header.
            (i.e.: printheader=True, headertext='some,header,text,here')

            It is suggested to initialise the :class:`~log.Log` class
            at program startup, with the ``printheader`` parameter
            set to ``True``.  This is safe because if the log file
            already exists, the header will not be re-created.  However,
            if the log file does not exist, it will be created with a
            header, using the value of the ``headertext`` parameter.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
    To use the :class:`~log.Log` class in your project::

        from utils3.log import Log

        header = 'COMMENT,TYPE,VAL,UNIT'
        logger = Log(filepath='path/to/file.log', printheader=True, headertext=header)

        logger.write(text='Most cows can jump over the moon,Fact,94.2,pct')

"""

import os
import socket
import getpass
from datetime import datetime as dt

import utils3.reporterror as reporterror


class Log():
    """This is a small and simple log file creator/writer class.

    The calling program is responsible for passing the proper arguments
    to create the log file header.
    (i.e.: printheader=True, headertext='some,header,text,here')

    On class instantiation, validation is performed to determine if the
    log file exists.  If the log file does not exist, a header is
    required before writing to the log file.  These parameters can be
    passed to the class on instantiation, and will be ignored if the
    log file already exists.

    Args:
        filepath (str): Full path to the log file.
        autofill (bool): Automatically populate ``datetime(now)``, host
            and username values, to each log entry.
        printheader (bool): Print a log file header using the text
            passed into the ``headertext`` parameter.
            **Note: The header will only be written if the log file
            does not exist.**
        headertext (str): String of delimited column labels to be
            written as the header.
        sep (str): Separator to be used in the log file.  This separator
            is used when writing the autofill values.

    :File Validation:
        On class instantiation, tests are performed to ensure the log
        file is being populated in a logical way.

            * If ``printheader`` is ``False``, and the log file does not
              exist, the user is notified
            * If ``printheader`` is ``True``, yet ``headertext`` is
              blank, the user is instructed to pass header text
            * If ``printheader`` is ``True``, yet the log file already
              exists, the header will not be written

    :Example:
        To use the :class:`~log.Log` class in your project::

            from utils3.log import Log

            header = 'COMMENT,TYPE,VAL,UNIT'
            logger = Log(filepath='path/to/file.log', printheader=True,
                         headertext=header)

            logger.write(text='Most cows can jump over the moon,Fact,94.2,pct')

    """

    def __init__(self, filepath, autofill=True, printheader=False, headertext='', sep=','):
        """Class initialiser."""
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


    def write(self, text):
        """Write text to the log file defined at instantiation.

        Args:
            text (str): Delimited text string to be written to the log.

        Note:
            If ``autofill`` is ``True``, the datetime, host and username
            values **will be populated automatically**, and *do not*
            need to be passed into the ``text`` argument.

        :Design:
            If the ``autofill`` argument is ``True``, the current
            datetime, host and username values are written (in that
            order), ahead of the text string provided to the ``text``
            argument.  The ``sep`` parameter (defined at instantiation),
            is used to separate these auto-populated fields.

        :Example:
            To write to the log file::

                from utils3.log import Log

                logger = Log(filepath='path/to/file.log', autofill=True)
                logger.write(text='Just adding some random text to my log')

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


    def write_blank_line(self):
        r"""Write a blank line to the log file.

        Note:
            The ``autofill`` information **is not** written.  This is a
            true blank line, created by writing a '\\n' value to the
            log.

        :Example:
            To write a blank line to the log file::

                from utils3.log import Log

                logger = Log(filepath='path/to/file.log', autofill=True)
                logger.write_blank_line()

        """
        try:
            # APPEND BLANK LINE TO LOG FILE
            with open(self._filepath, 'a') as f: f.write('\n')
        except Exception as err:
            # NOTIFICATION
            reporterror.reporterror(err)
