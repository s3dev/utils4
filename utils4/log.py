# -*- coding: utf-8 -*-
"""
:Purpose:   This is a small class module designed as a central log file
            creator.

            The calling program is responsible for passing the proper
            arguments to create the log file header. For example::

                (printheader=True, headertext='some,header,text,here')

            It is suggested to initialise the :class:`~Log` class
            at program startup, with the ``printheader`` parameter
            set to ``True``. This is safe because if the log file
            already exists, the header will not be re-created. However,
            if the log file does not exist, it will be created with a
            header, using the value of the ``headertext`` parameter.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:

    To use the :class:`~Log` class in your project::

        >>> from utils4.log import Log

        >> header = 'COMMENT,TYPE,VAL,UNIT'
        >> logger = Log(filepath='/tmp/testlog.log',
                        printheader=True,
                        headertext=header)
        >> logger.write(text='Most cows can jump over the moon,Fact,94.2,pct')

"""

import getpass
import os
import socket
from datetime import datetime as dt


class Log:
    """This is a small and simple log file creator/writer class.

    The calling program is responsible for passing the proper arguments
    to create the log file header. For example::

        (printheader=True, headertext='some,header,text,here')

    On class instantiation, validation is performed to determine if the
    log file exists.  If the log file does not exist, a header is
    required before writing to the log file. These parameters can be passed to
    the class on instantiation, and will be ignored if the log file already
    exists.

    Args:
        filepath (str): Full path to the log file.
        autofill (bool, optional): Automatically populate ``datetime.now()``,
            host and username values, to each log entry. Defaults to True.
        printheader (bool, optional): Print a log file header using the text
            passed into the ``headertext`` parameter. Defaults to False.

            .. note:: The header will only be written if the log file does not
                      exist.

        headertext (str, optional): String of delimited column labels to be
            written as the header. Defaults to ''.
        sep (str, optional): Separator to be used in the log file. This
            separator is used when writing the autofill values.
            Defaults to ','.

    :File Validation:
        On class instantiation, tests are performed to ensure the log
        file is being populated in a logical way.

            * If ``printheader`` is ``False``, and the log file does not
              exist, the user is notified.
            * If ``printheader`` is ``True``, yet ``headertext`` is
              blank, the user is instructed to pass header text.
            * If ``printheader`` is ``True``, yet the log file already
              exists, the header will not be written.

    :Example:

        To use the :class:`~Log` class in your project::

            >>> from utils4.log import Log

            >>> header = 'COMMENT,TYPE,VAL,UNIT'
            >>> logger = Log(filepath='/tmp/testlog.log',
                             printheader=True,
                             headertext=header)

            >>> logger.write(text='Most cows can jump over the moon,Fact,94.2,pct')

    """

    def __init__(self, filepath, autofill=True, printheader=False, headertext='', sep=','):
        """Log class initialiser."""
        self._filepath = filepath
        self._autofill = autofill
        self._printheader = printheader
        self._headertext = headertext
        self._sep = sep
        self._host = socket.gethostname()
        self._user = getpass.getuser()
        self._autotext = ''
        self._setup()

    def write(self, text: str):
        """Write text to the log file defined at instantiation.

        Args:
            text (str): Delimited text string to be written to the log.

        Note:
            If ``autofill`` is ``True``, the datetime, host and username
            values **will be populated automatically**; these do *not*
            need to be passed into the ``text`` argument.

        :Design:
            If the ``autofill`` argument is ``True``, the current
            datetime, host and username values are written (in that
            order), ahead of the text string provided to the ``text``
            argument. The ``sep`` parameter (defined at instantiation),
            is used to separate these auto-populated fields.

        :Example:
            To write to the log file::

                >>> from utils4.log import Log

                >>> logger = Log(filepath='/tmp/testlog.log, autofill=True)
                >>> logger.write(text='Just adding some random text to my log')

        """
        try:
            if text:
                auto_text = f'{dt.now()}{self._sep}{self._autotext}' if self._autofill else ''
                with open(self._filepath, 'a', encoding='utf-8') as f:
                    f.write(auto_text)
                    f.write(text)
                    f.write('\n')
        except Exception as err:  # pragma: nocover
            print(err)

    def write_blank_line(self):
        """Write a blank line to the log file.

        Note:
            The ``autofill`` information is **not** written. This is a
            true blank line, created by writing the system's native line
            separator character(s)to the log.

        :Example:
            To write a blank line to the log file::

                >>> from utils4.log import Log

                >>> logger = Log(filepath='/tmp/testlog.log', autofill=True)
                >>> logger.write_blank_line()

        """
        try:
            with open(self._filepath, 'a', encoding='utf-8') as f:
                f.write('\n')
        except Exception as err:  # pragma: nocover
            print(err)

    def _setup(self):
        """Setup tasks performed on class instantiation.

        :Tasks:

            - Create the log file.
            - Write the header.

        :Validation:

            - If the log file does not exist, ensure a header is requested.
            - If the header is requested, ensure the header text is provided.

        Raised:
            UserWarning: If either of the validation criteria are not met.

        """
        self._autotext = (f'{self._host}{self._sep}{self._user}{self._sep}'
                          if self._autofill else '')
        # Verify the logfile does not exists, ensure a header is requested.
        if (not self._printheader) & (not os.path.exists(self._filepath)):
            raise UserWarning('Header expected, log does not already exist.\n'
                              '- Log file does not exist, therefore a header must be requested,\n'
                              '  as the header is written at the time of log file creation.\n')
        # Verify header text is populated, if print header is requested.
        if self._printheader & (not self._headertext):
            raise UserWarning('Header requested, but header text not received.\n'
                              '- The printheader argument is True, however the headertext string\n'
                              '  is blank. A headertext string must also be supplied.\n')
        # Write the header if 1) requested, 2) header text provided and 3) log file does not exist.
        if all([self._printheader, self._headertext, not os.path.exists(self._filepath)]):
            with open(self._filepath, 'w', encoding='utf-8') as f:
                f.write(self._headertext)
                f.write('\n')
