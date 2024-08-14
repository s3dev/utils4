#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``log`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import getpass
import os
import socket
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4.log import Log


class TestLog(TestBase):
    """Testing class used to test the ``log`` module."""

    _FPATH = os.path.join(TestBase._DIR_TMP, 'testlog.log')
    _HEAD = 'DATETIME,HOST,USER,COMMENT'
    _MSG1 = msgs.templates.not_as_expected.general

    def setUp(self):
        """Run this logic *before* each test case."""
        if os.path.exists(self._FPATH):
            os.remove(self._FPATH)
        self._user = getpass.getuser()
        self._host = socket.gethostname()

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='log')

    @classmethod
    def tearDownClass(cls):
        """Run this logic at the end of all test cases.

        :Tasks:
            - Remove the log file created by these tests.

        """
        if os.path.exists(cls._FPATH):
            os.remove(cls._FPATH)

    @property
    def log_spec_01(self):
        """Arguments to be passed into the ``Log`` constructor."""
        spec = {'filepath': self._FPATH,
                'autofill': True,
                'printheader': True,
                'headertext': self._HEAD,
                'sep': ','}
        return spec

    @property
    def log_spec_02(self):
        """Invalid arguments to be passed into the ``Log`` constructor."""
        spec = {'filepath': self._FPATH,
                'autofill': True,
                'printheader': False,
                'sep': ','}
        return spec

    @property
    def log_spec_03(self):
        """Invalid arguments to be passed into the ``Log`` constructor."""
        spec = {'filepath': self._FPATH,
                'autofill': True,
                'printheader': True,
                'headertext': '',  # Intentionally not providing header text.
                'sep': ','}
        return spec

    def test01__setup(self):
        """Test the ``_setup`` method.

        :Test:
            - Create a new log file.
            - Test the header has been written as expected.

        """
        Log(**self.log_spec_01)
        with open(self._FPATH, 'r', encoding='utf-8') as f:
            test = f.read()
        utilities.assert_true(expected=self._HEAD + '\n', test=test, msg=self._MSG1)

    def test01__write(self):
        """Test the ``write`` method.

        :Test:
            - Create a new log file.
            - Write (n) lines to the log file.
            - Test the contents are as expected.

        """
        n = 5
        exp = [f'{self._host},{self._user},line{i}' for i in range(n)]
        l = Log(**self.log_spec_01)
        for i in range(n):
            l.write(f'line{i}')
        with open(self._FPATH, 'r', encoding='utf-8') as f:
            lines = [i.strip() for i in f.readlines()]
        for idx, line in enumerate(lines):
            if idx == 0:
                self.assertEqual(first=line, second=self._HEAD)
            else:
                self.assertEqual(first=','.join(line.split(',')[1:]), second=exp[idx-1])

    def test01__write_blank_line(self):
        """Test the ``write_blank_line`` method.

        :Test:
            - Create a new log file.
            - Write (n) lines to the log file, including a blank line.
            - Test the contents are as expected.

        """
        n = 5
        exp = [f'{self._host},{self._user},line{i}' for i in range(n)]
        exp[2] = ''
        l = Log(**self.log_spec_01)
        l.write('line0')
        l.write('line1')
        l.write_blank_line()
        l.write('line3')
        l.write('line4')
        with open(self._FPATH, 'r', encoding='utf-8') as f:
            lines = [i.strip() for i in f.readlines()]
        for idx, line in enumerate(lines):
            if idx == 0:
                self.assertEqual(first=line, second=self._HEAD)
            else:
                self.assertEqual(first=','.join(line.split(',')[1:]), second=exp[idx-1])

    def test02__new_file_no_header(self):
        """Test the library detects new file creation with no header.

        :Test:
            - Create a new instance.
            - Verify the libary raises a UserWarning for no header requested.

        """
        with self.assertRaises(UserWarning):
            Log(**self.log_spec_02)

    def test03__header_no_header_text(self):
        """Test the library detects a header request but no text.

        :Test:
            - Create a new instance.
            - Verify the libary raises a UserWarning for a header request, but
              no text provided.

        """
        with self.assertRaises(UserWarning):
            Log(**self.log_spec_03)
