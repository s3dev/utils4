#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``dfdiff`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=wrong-import-order

import numpy as np
import pandas as pd
from datetime import datetime as dt
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4 import dfdiff


class TestDfDiff(TestBase):
    """Testing class used to test the ``dfdiff`` module."""

    _MSG1 = msgs.templates.not_as_expected.general
    _DFBASE = pd.DataFrame({'col1': [0, 1, 2, 3],
                            'col2': ['a', 'b', 'c', 'd'],
                            'col3': [0.0, 1.0, 2.0, 3.0]})
    _DFBASE2 = pd.DataFrame({'col1': [0, 1, 2, 3],
                             'col2': ['a', 'b', 'c', 'd'],
                             'col3': [0.0, 1.0, np.nan, 3.0]})

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='dfdiff')

    def setUp(self):
        """Run this logic *before* each test case."""
        self.disable_terminal_output()

    def tearDown(self):
        """Run this logic *after* each test case."""
        self.enable_terminal_output()

    def test01__diff__matching(self):
        """Test the ``diff`` method for two matching DataFrames.

        :Test:
            - The local DataFrame is compared against the class' base
              DataFrame.
            - The expected columns to return differences are passed into the
              assertion method. In this case, it's an empty list.

        """
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=self._DFBASE)
        d.diff()
        utilities.assert_true(expected=[], test=d._col_mismatches, msg=self._MSG1)

    def test02__diff__non_matching_01(self):
        """Test the ``diff`` method for two non-matching DataFrames.

        :Test:
            - The local DataFrame (containing different values) is compared
              against the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 1, 2, 4],  # The 4 is different.
                            'col2': ['a', 'b', 'c', 'd'],
                            'col3': [0.0, 1.0, 2.0, 3.0]})
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1'], test=d._col_mismatches, msg=self._MSG1)

    def test02__diff__non_matching_02(self):
        """Test the ``diff`` method for two non-matching DataFrames.

        :Test:
            - The local DataFrame (containing different values) is compared
              against the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 1, 2, 3],
                            'col2': ['a', 'b', 'c', 'e'],  # The 'e' is different.
                            'col3': [0.0, 1.0, 2.0, 3.0]})
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col2'], test=d._col_mismatches, msg=self._MSG1)

    def test02__diff__non_matching_03(self):
        """Test the ``diff`` method for two non-matching DataFrames.

        :Test:
            - The local DataFrame is compared against the class' base
              DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 0, 2, 3],           # The second 0 is different.
                            'col2': ['a', 'b', 'c', 'e'],   # The 'e' is different.
                            'col3': [0.0, 1.0, 2.0, 3.0]})
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1', 'col2'], test=d._col_mismatches, msg=self._MSG1)

    def test02__diff__non_matching_04(self):
        """Test the ``diff`` method for two non-matching DataFrames.

        :Test:
            - The local DataFrame (containing different values) is compared
              against the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 0, 2, 3],           # The second 0 is different.
                            'col2': ['a', 'b', 'c', 'e'],   # The 'e' is different.
                            'col3': [0.0, 1.0, 2.0, 4.0]})  # The 4.0 is different.
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1', 'col2', 'col3'],
                              test=d._col_mismatches,
                              msg=self._MSG1)

    def test02__diff__non_matching_05(self):
        """Test the ``diff`` method for two non-matching DataFrames.

        :Test:
            - The local DataFrame (which has an extra row) is compared against
              the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 0, 2, 3, 4],             # There is an extra row of data in this set.
                            'col2': ['a', 'b', 'c', 'e', 'f'],   # Same
                            'col3': [0.0, 1.0, 2.0, 4.0, 5.0]})  # Same
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1', 'col2', 'col3'],
                              test=d._col_mismatches,
                              msg=self._MSG1)

    def test02__diff__non_matching_06(self):
        """Test the ``diff`` method for two non-matching DataFrames with datetime.

        :Test:
            - The local DataFrame (which contains datetime values) is compared
              against the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [0, 1, 2, pd.to_datetime('1900-01-01')],  # Column contains a pandas datetime value.
                            'col2': ['a', 'b', 'c', dt(2022,1,1)],            # Column contains a datetime value.
                            'col3': [0.0, 1.0, 2.0, 4.0]})
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1', 'col2', 'col3'],
                              test=d._col_mismatches,
                              msg=self._MSG1)

    def test02__diff__non_matching_07(self):
        """Test the ``diff`` method for two non-matching DataFrames with NaN,
        and NaT.

        :Test:
            - The local DataFrame (which contains NaN/NaT values) is compared
              against the class' base DataFrame.
            - The expected columns to return differences are passed into the
              assertion method.

        """
        df1 = pd.DataFrame({'col1': [np.nan, 1, 2, 3],             # Column contains NaN.
                            'col2': ['a', float('nan'), 'c', 'd'], # Column contains NaN.
                            'col3': [0.0, 1.0, pd.NaT, 3.0]})      # Column contains NaT.
        d = dfdiff.DataFrameDiff(df_source=self._DFBASE2, df_test=df1)
        d.diff()
        utilities.assert_true(expected=['col1', 'col2', 'col3'],
                              test=d._col_mismatches,
                              msg=self._MSG1)
