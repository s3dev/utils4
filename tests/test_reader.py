#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``reader`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import os
import pandas as pd
import pickle
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4.reader import Reader


class TestReader(TestBase):
    """Testing class used to test the ``reader`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='reader')

    def test01__read_xls(self):
        """Test the ``read_xls`` method.

        :Test:
            - Read the expected data from a serialised file.
            - Read an old-style XLS file using the reader.
            - Verify the contents of the expected output and the parsed data
              from the reader are the same.

        """
        fp_exp = os.path.join(self._DIR_RESRC, 'test_reader__exp.p')
        fp_test = os.path.join(self._DIR_RESRC, 'test_reader__excel95.xls')
        with open(fp_exp, 'rb') as f:
            data = pickle.load(f)
            df_exp = pd.DataFrame(data)
            df_exp[['col5', 'col6', 'col7']] = (df_exp[['col5', 'col6', 'col7']]
                                                .apply(pd.to_datetime))
        r = Reader()
        df_test = r.read_xls(filepath=fp_test,
                             skiprows=6,
                             skipcols=1,
                             chopcols=2,
                             date_formats={'col5': '%Y-%m-%d %H:%M:%S',
                                           'col6': '%Y-%m-%d %H:%M:%S',
                                           'col7': '%Y-%m-%d %H:%M:%S'})
        utilities.assert_equal_dataframe(df1=df_exp, df2=df_test)

    def test02__read_xls__date_error(self):
        """Test the ``read_xls`` method, with an invalid date.

        :Test:
            - Read the expected data from a serialised file, including an
              invalid date filled to '1900-01-01 00:00:00'.
            - Read an old-style XLS file using the reader and the
              ``fill_date_errors`` argument.
            - Verify the contents of the expected output and the parsed data
              from the reader are the same.

        """
        fp_exp = os.path.join(self._DIR_RESRC, 'test_reader__exp__date_error.p')
        fp_test = os.path.join(self._DIR_RESRC, 'test_reader__excel95_date_error.xls')
        with open(fp_exp, 'rb') as f:
            data = pickle.load(f)
            df_exp = pd.DataFrame(data)
            df_exp[['col5', 'col6', 'col7']] = (df_exp[['col5', 'col6', 'col7']]
                                                .apply(pd.to_datetime))
        r = Reader()
        df_test = r.read_xls(filepath=fp_test,
                             skiprows=6,
                             skipcols=1,
                             chopcols=2,
                             date_formats={'col5': '%Y-%m-%d %H:%M:%S',
                                           'col6': '%Y-%m-%d %H:%M:%S',
                                           'col7': '%Y-%m-%d %H:%M:%S'},
                             errors='coerce',
                             fill_date_errors=True)
        utilities.assert_equal_dataframe(df1=df_exp, df2=df_test)

    def test03__read_xls__not_xls(self):
        """Test the ``read_xls`` method with a non-XLS file.

        :Test:
            - Verify the method raises a ValueError if the passed filpath is
              not an XLS file.

        """
        with self.assertRaises(ValueError):
            r = Reader()
            _ = r.read_xls(filepath='/path/to/file.csv')

    def test04__read_xls__no_data(self):
        """Test the ``read_xls`` method with an empty XLS file.

        :Test:
            - Verify the method raises an IOError if the method receives
              an empty data file.

        """
        fp = os.path.join(self._DIR_RESRC, 'test_reader__excel95_nodata.xls')
        with self.assertRaises(IOError):
            r = Reader()
            _ = r.read_xls(filepath=fp)
