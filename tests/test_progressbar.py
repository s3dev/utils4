#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``progressbar`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name

from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4.progressbar import ProgressBar


class TestProgressBar(TestBase):
    """Testing class used to test the ``progressbar`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='progressbar')

    def test01__get_color(self):
        """Test the ``_get_color`` method.

        :Test:
            - Verify the method returns the expected escape sequence.

        """
        # pylint: disable=protected-access
        clrs = {'r': 31, 'g': 32, 'y': 33, 'b': 34, 'm': 35, 'c': 36, 'w': 37}
        for k, v in clrs.items():
            with self.subTest(msg=f'k={k}, v={v}'):
                pb = ProgressBar(color=k)
                test = pb._getcolor()
                exp = f'\033[{clrs.get(k)};40m'
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)
