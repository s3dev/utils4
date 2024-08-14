#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``reporterror`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name

import contextlib
import io
import os
import sys
import traceback

try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
from utils4.log import Log
from utils4.reporterror import reporterror


class TestReportError(TestBase):
    """Testing class used to test the ``reporterror`` module."""

    _LOGPATH = os.path.join(TestBase._DIR_TMP, 'reporterror.log')
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases.

        :Tasks:
            - Notify user of the test being run.
            - Create a log file at the specified path.

        """
        msgs.startoftest.startoftest(module_name='reporterror')
        Log(filepath=cls._LOGPATH,
            autofill=True,
            printheader=True,
            headertext='datetime,host,user,message',
            sep=',')

    @classmethod
    def tearDownClass(cls):
        """Perform these tasks at the end of all tests.

        :Tasks:
            - Delete the log file created by this test.

        """
        os.remove(path=cls._LOGPATH)

    def test01__reporterror__divzero(self):
        """Test the ``reporterror`` method with a ZeroDivisionError.

        :Test:
            - Trigger a ZeroDivisionError and capture the output of
              ``reporterror``.
            - Compare the output to the expected result to confirm they match.

        """
        exp = ''
        buff = io.StringIO()
        with contextlib.redirect_stdout(buff):
            try:
                1/0
            except Exception as err:
                reporterror(error=err, logevent=False)
                exp = self._build_error_message(error=err)
            test = buff.getvalue()
        utilities.assert_true(expected=exp.strip(), test=test.strip(), msg=self._MSG1)

    def test02__reporterror__assertion(self):
        """Test the ``reporterror`` method with an AssertionError.

        :Test:
            - Trigger a AssertionError and capture the output of
              ``reporterror``.
            - Compare the output to the expected result to confirm they match.

        """
        exp = ''
        buff = io.StringIO()
        with contextlib.redirect_stdout(buff):
            try:
                assert False
            except Exception as err:
                reporterror(error=err, logevent=False)
                exp = self._build_error_message(error=err)
            test = buff.getvalue()
        utilities.assert_true(expected=exp.strip(), test=test.strip(), msg=self._MSG1)

    def test03__reporterror__assertion_logged(self):
        """Test the ``reporterror`` method with a logged AssertionError.

        :Test:
            - Trigger a AssertionError and capture the output of
              ``reporterror``, and log the error.
            - Compare the output to the expected result to confirm they match.
            - Verify the log file contains the records as expected.

        """
        exp = ''
        with contextlib.redirect_stdout(None):
            try:
                assert False
            except Exception as err:
                reporterror(error=err, logevent=True, logfilepath=self._LOGPATH)
                exp = self._build_log_entry(error=err)
        with open(self._LOGPATH, 'r', encoding='utf-8') as f:
            for line in f:
                test = line  # Capture last line of the long file.
        self.assertIn(member=exp, container=test)

    @staticmethod
    def _build_error_message(error: Exception) -> str:
        """Build the error message string for the test.

        Args:
            error (Exception): Exception raised by the try/except block.

        Returns:
            str: An error message string against which the test is conducted.

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
        return msg

    @staticmethod
    def _build_log_entry(error: Exception) -> str:
        """Build and return the expected log file entry.

        Args:
            error (Exception): Exception raised by the try/except block.

        Returns:
            str: A string containing the log entry.

        """
        _, _, exc_tb = sys.exc_info()
        fnam, line, func, text = traceback.extract_tb(exc_tb)[-1]
        msg = f'ERROR: {error}; CMD: {text}; MODULE: {fnam}; FUNC: {func}; LINE: {line}'
        return msg
