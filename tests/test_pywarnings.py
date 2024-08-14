#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``pywarnings`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name

import contextlib
import io
import warnings
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4.pywarnings import PyWarnings


class TestPyWarnings(TestBase):
    """Testing class used to test the ``pywarnings`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='pywarnings')

    def test01__ignore_warnings__single(self):
        """Test the ``ignore_warnings`` method, for a single category.

        :Test:
            - Verify the FutureWarnings are allowed, ignored and re-allowed.

        """
        buff = io.StringIO()
        pw = PyWarnings(ignore=True, categories=['FutureWarning'])
        with contextlib.redirect_stderr(buff):
            # Test 1
            warnings.warn('', FutureWarning)
            test1 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
            # Test 2
            pw.ignore_warnings()
            warnings.warn('', FutureWarning)
            test2 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
            # Test 3
            pw.reset_warnings()
            warnings.warn('', FutureWarning)
            test3 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
        self.assertIn(member='FutureWarning', container=test1)
        utilities.assert_true(expected='', test=test2, msg=self._MSG1)
        self.assertIn(member='FutureWarning', container=test3)

    def test02__ignore_warnings__multiple(self):
        """Test the ``ignore_warnings`` method, for multiple categories.

        :Test:
            - Verify the following warnings are allowed, ignored and
              re-allowed:

                  - Futurewarning
                  - ResourceWarning
                  - UserWarning

        """
        buff = io.StringIO()
        classes = [FutureWarning, ResourceWarning, UserWarning]
        strings = [c.__name__ for c in classes]
        pw = PyWarnings(ignore=True, categories=strings)
        with contextlib.redirect_stderr(buff):
            # Test 1
            for c, s  in zip(classes, strings):
                warnings.warn('', c)
                test1 = buff.getvalue()
                buff.truncate(0)
                buff.seek(0)
                # Test 2
                pw.ignore_warnings()
                warnings.warn('', c)
                test2 = buff.getvalue()
                buff.truncate(0)
                buff.seek(0)
                # Test 3
                pw.reset_warnings()
                warnings.warn('', c)
                test3 = buff.getvalue()
                buff.truncate(0)
                buff.seek(0)
                self.assertIn(member=s, container=test1)
                utilities.assert_true(expected='', test=test2, msg=self._MSG1)
                self.assertIn(member=s, container=test3)

    def test03__ignore_warnings__config(self):
        """Test the ``ignore_warnings`` method, using a dict.

        :Test:
            - Verify the FutureWarning is allowed, ignored and re-allowed.

        """
        buff = io.StringIO()
        config = {'py_warnings': {'ignore': True, 'categories': 'FutureWarning'}}
        pw = PyWarnings(config=config)
        with contextlib.redirect_stderr(buff):
            # Test 1
            warnings.warn('', FutureWarning)
            test1 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
            # Test 2
            pw.ignore_warnings()
            warnings.warn('', FutureWarning)
            test2 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
            # Test 3
            pw.reset_warnings()
            warnings.warn('', FutureWarning)
            test3 = buff.getvalue()
            buff.truncate(0)
            buff.seek(0)
            self.assertIn(member='FutureWarning', container=test1)
            utilities.assert_true(expected='', test=test2, msg=self._MSG1)
            self.assertIn(member='FutureWarning', container=test3)
