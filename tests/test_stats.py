#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``stats`` module.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order
"""

try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
import numpy as np
from scipy.stats import linregress
from utils4.stats import LinearRegression


class TestStats(TestBase):
    """Testing class used to test the ``stats`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='stats')

    # def setUp(self):
    #     """Run this logic *before* each test case."""
    #     self.disable_terminal_output()

    # def tearDown(self):
    #     """Run this logic *after* each test case."""
    #     self.enable_terminal_output()

    def test01__linear_regression(self):
        """Test the ``LinearRegression`` class output.

        :Test:
            - Run the scipy.stats.linregress method alongside the
              LineaRegression.calculate() method and verify the following
              attributes are the same:

                  - intercept
                  - slope
                  - regression line

        """
        # pylint: disable=line-too-long
        np.random.seed(4)
        x = np.arange(10000)
        y = np.sort(np.random.exponential(10, size=10000))
        linreg = LinearRegression(x=x, y=y)
        scipy_lr = linregress(x=x, y=y)
        linreg.calculate()
        # Calculate the regression line from scipy. Test against stats.
        line = (scipy_lr.slope * x) + scipy_lr.intercept
        utilities.assert_true(expected=True,
                              test=all([linreg.intercept.round(10) == scipy_lr.intercept.round(10),
                                        linreg.slope.round(10) == scipy_lr.slope.round(10),
                                        (line.round(10) == linreg.regression_line.round(10)).all()]),
                              msg=self._MSG1)
