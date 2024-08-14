#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``stats`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
import io
import os
import numpy as np
import pandas as pd
import pickle
from contextlib import redirect_stdout
from scipy.stats import linregress
from utils4.stats import LinearRegression
from utils4.stats import stats


class TestStats(TestBase):
    """Testing class used to test the ``stats`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='stats')

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

    def test02__cusum__window_full(self):
        """Test the ``Stats.cusum`` method, with a 'full' window.

        :Test:
            - Calculate a CUSUM with a window size the length of the
              DataFrame and compare the results with a pre-calculated
              CUSUM on the same dataset to ensure the results are equal.

        :Source Data:

            The code used to generate the source dataset is::

                >>> fpath = os.path.join(self._DIR_RESRC,
                                         'test_stats__cusum_win_full.p')
                >>> np.random.seed(1)
                >>> df = pd.DataFrame({'col1': (pd.Series(np.random.randn(1000))
                                                .rolling(window=100, min_periods=100)
                                                .mean())})
                >>> stats.cusum(df, cols=['col1'],
                                window=len(df),
                                min_periods=1,
                                inplace=True,
                                show_plot=False)
                >>> df.to_pickle(fpath, protocol=4)

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_stats__cusum_win_full.p')
        df_exp = pd.read_pickle(fpath)
        df_test = stats.cusum(df_exp,
                              cols=['col1'],
                              window=len(df_exp),
                              min_periods=1,
                              inplace=False,
                              show_plot=False)
        utilities.assert_equal_dataframe(df1=df_exp, df2=df_test)

    def test02__cusum__window_5pct(self):
        """Test the ``Stats.cusum`` method, with a 5% window size.

        :Test:
            - Calculate a CUSUM with a window size of 5% (default) and
              compare the results with a pre-calculated CUSUM on the
              same dataset to ensure the results are equal.

        :Source Data:

            The code used to generate the source dataset is::

                >>> fpath = os.path.join(self._DIR_RESRC,
                                         'test_stats__cusum_win_5pct.p')
                >>> np.random.seed(1)
                >>> df = pd.DataFrame({'col1': (pd.Series(np.random.randn(1000))
                                                .rolling(window=100, min_periods=100)
                                                .mean())})
                >>> stats.cusum(df, cols=['col1'],
                                window=None,  # Use default window size.
                                min_periods=1,
                                inplace=True,
                                show_plot=False)
                >>> df.to_pickle(fpath, protocol=4)

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_stats__cusum_win_5pct.p')
        df_exp = pd.read_pickle(fpath)
        df_test = stats.cusum(df_exp,
                              cols=['col1'],
                              window=None,  # Use default window size.
                              min_periods=1,
                              inplace=False,
                              show_plot=False)
        utilities.assert_equal_dataframe(df1=df_exp, df2=df_test)

    def test03__kde__array(self):
        """Test the Gaussian KDE calculation, from an array.

        :Test:
            - Read the expected output from a serialised file and compare
              the function output to the expected results.

        :Source Data:

            The code used to generate the source dataset is::

            >>> fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
            >>> np.random.seed(73)
            >>> data = np.random.normal(size=100)*100
            >>> X, Y, max_x = stats.kde(data, n=500)
            >>> with open(fpath, 'wb') as f:
            >>>     pickle.dump((data, X, Y, max_x), f)

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
        with open(fpath, 'rb') as f:
            data, X_exp, Y_exp, max_exp = pickle.load(f)
        X_test, Y_test, max_test = stats.kde(data, n=500)
        with self.subTest(msg='Max X test'):
            utilities.assert_true(expected=max_exp, test=max_test, msg=self._MSG1)
        for exp, test in ((X_exp, X_test), (Y_exp, Y_test)):
            with self.subTest(msg='Size test'):
                test_size = exp.size == test.size
                utilities.assert_true(expected=exp.size, test=test.size, msg=self._MSG1)
            if test_size:
                # Cannot test values if the shapes are not the same.
                with self.subTest(msg='Values test'):
                    n = 15
                    utilities.assert_true_array(expected=np.round(exp, n),
                                                test=np.round(test, n),
                                                msg=self._MSG1)
            else:
                self.assertEqual(1, 0, msg='** Forced failure. **')

    def test03__kde__list(self):
        """Test the Gaussian KDE calculation, from a list.

        :Test:
            - Read the expected output from a serialised file and compare
              the function output to the expected results.

        :Source Data:

            The code used to generate the source dataset is::

            >>> fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
            >>> np.random.seed(73)
            >>> data = np.random.normal(size=100)*100
            >>> X, Y, max_x = stats.kde(data, n=500)
            >>> with open(fpath, 'wb') as f:
            >>>     pickle.dump((data, X, Y, max_x), f)

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
        with open(fpath, 'rb') as f:
            data, X_exp, Y_exp, max_exp = pickle.load(f)
        data = data.tolist()  # <-- Key point of the test.
        X_test, Y_test, max_test = stats.kde(data, n=500)
        with self.subTest(msg='Max X test'):
            utilities.assert_true(expected=max_exp, test=max_test, msg=self._MSG1)
        for exp, test in ((X_exp, X_test), (Y_exp, Y_test)):
            with self.subTest(msg='Size test'):
                test_size = exp.size == test.size
                utilities.assert_true(expected=exp.size, test=test.size, msg=self._MSG1)
            if test_size:
                with self.subTest(msg='Values test'):
                    n = 15
                    utilities.assert_true_array(expected=np.round(exp, n),
                                                test=np.round(test, n),
                                                msg=self._MSG1)

    def test03__kde__series(self):
        """Test the Gaussian KDE calculation, from a pandas Series.

        :Test:
            - Read the expected output from a serialised file and compare
              the function output to the expected results.

        :Source Data:

            The code used to generate the source dataset is::

            >>> fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
            >>> np.random.seed(73)
            >>> data = np.random.normal(size=100)*100
            >>> X, Y, max_x = stats.kde(data, n=500)
            >>> with open(fpath, 'wb') as f:
            >>>     pickle.dump((data, X, Y, max_x), f)

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_stats__kde.p')
        with open(fpath, 'rb') as f:
            data, X_exp, Y_exp, max_exp = pickle.load(f)
        data = pd.Series(data)  # <-- Key point of the test.
        X_test, Y_test, max_test = stats.kde(data, n=500)
        with self.subTest(msg='Max X test'):
            utilities.assert_true(expected=max_exp, test=max_test, msg=self._MSG1)
        for exp, test in ((X_exp, X_test), (Y_exp, Y_test)):
            with self.subTest(msg='Size test'):
                test_size = exp.size == test.size
                utilities.assert_true(expected=exp.size, test=test.size, msg=self._MSG1)
            if test_size:
                with self.subTest(msg='Values test'):
                    n = 15
                    utilities.assert_true_array(expected=np.round(exp, n),
                                                test=np.round(test, n),
                                                msg=self._MSG1)

    def test03__kde_invalid(self):
        """Test the Gaussian KDE calculation, with invalid data.

        :Test:
            - Verify the KDE function returns two empty arrays on error.

        """
        buff = io.StringIO()
        with redirect_stdout(buff):
            X, Y, max_x = stats.kde(0)
        utilities.assert_true(expected=0, test=X.size, msg=self._MSG1)
        utilities.assert_true(expected=0, test=Y.size, msg=self._MSG1)
        utilities.assert_true(expected=0, test=max_x, msg=self._MSG1)
        self.assertIn('TypeError', buff.getvalue())
