#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``timedelta`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name

from datetime import datetime as dt
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4.timedelta import timedelta


class TestTimeDelta(TestBase):
    """Testing class used to test the ``timedelta`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='timedelta')

    def test01__timedelta__seconds(self):
        """Test the ``timedelta`` method, for (n) seconds into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -5, dt(2022,3,22,15,5,23)), ('Future', 5, dt(2022,3,22,15,5,33))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='S', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__timedelta__minutes(self):
        """Test the ``timedelta`` method, for (n) minutes into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -5, dt(2022,3,22,15,0,28)), ('Future', 5, dt(2022,3,22,15,10,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='M', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__timedelta__hours(self):
        """Test the ``timedelta`` method, for (n) hours into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -15, dt(2022,3,22,0,5,28)), ('Future', 15, dt(2022,3,23,6,5,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='H', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__timedelta__days(self):
        """Test the ``timedelta`` method, for (n) days into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -10, dt(2022,3,12,15,5,28)), ('Future', 10, dt(2022,4,1,15,5,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='d', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test05__timedelta__weeks(self):
        """Test the ``timedelta`` method, for (n) weeks into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -10, dt(2022,1,11,15,5,28)), ('Future', 10, dt(2022,5,31,15,5,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='w', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test06__timedelta__months(self):
        """Test the ``timedelta`` method, for (n) months into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -10, dt(2021,5,22,15,5,28)), ('Future', 10, dt(2023,1,22,15,5,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='m', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test07__timedelta__years(self):
        """Test the ``timedelta`` method, for (n) years into the past/future.

        :Test:
            - Verify (n) <units> into the past matches the expected result.
            - Verify (n) <units> into the future matches the expected result.

        """
        now = dt(2022,3,22,15,5,28)
        exps = [('Past', -5, dt(2017,3,22,15,5,28)), ('Future', 5, dt(2027,3,22,15,5,28))]
        for fp, n, exp in exps:
            with self.subTest(msg=f'fp={fp}'):
                test = timedelta(origin=now, unit='y', value=n)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test08__timedelta__invalid(self):
        """Test the ``timedelta`` method, with an invalid unit.

        :Test:
            - Verify a ValueError is raised for invalid units.

        """
        now = dt(1900,1,1)
        units = ['s', 'h', 'D', 'W', 'Y']
        for unit in units:
            with self.subTest(msg=f'unit={unit}'):
                with self.assertRaises(ValueError):
                    _ = timedelta(origin=now, unit=unit, value=1)
