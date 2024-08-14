#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides DataFrame differencing logic.

            The caller creates an instance which accepts the two DataFrames
            to be compared as the arguments. When the
            :meth:`~DataFrameDiff.diff` method is called, a list of columns
            containing value mismatches is compiled. Then, the list of column
            mismatches is iterated with each value in the column being
            compared. All value mismatches are reported to the terminal.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Note:      It's worth noting that current functionality **does not
            check data types**, unlike the pandas ``pd.DataFrame.equals()``
            method. This functionality may be added in a future release.

:Example:

    Short example for differencing two DataFrames::

        >>> from utils4 import dfdiff

        >>> d = dfdiff.DataFrameDiff(df_source, df_test)
        >>> d.diff()

"""
# pylint: disable=wrong-import-order

import pandas as pd
from itertools import zip_longest
try:
    from .user_interface import ui
except ImportError:  # pragma: nocover
    from user_interface import ui


class _Messages:
    """This private class handles the messaging for DataFrame differencing."""

    _FMT = '{:<10}\t{:<10}\t{:<25}\t{:<25}'

    @staticmethod
    def column_mismatches(columns: list):
        """List columns with mismatches.

        Args:
            columns (list): A list of columns containing mismatches.

        """
        # pylint: disable=consider-using-f-string
        ui.print_('\nColumn mismatches:', fore='cyan', style='normal')
        print(*map('- {}'.format, columns), sep='\n')

    @staticmethod
    def column_mismatches_none():
        """Print message for no column mismatches."""
        ui.print_('\nNo mismatches for this set.', fore='green')

    def data_mismatches(self, column: str, mismatches: list):
        """Print the data mismatches.

        Args:
            column (str): Name of the column being analysed.
            mismatches (list): A list of tuples containing data mismatches,
                as::

                    [(0, 0, 1, 2), (1, 1, 3, 4)]

        """
        ui.print_(f'Data mismatches for column: {column}', fore='yellow')
        print(self._FMT.format('SrcRow', 'TstRow', 'SrcValue', 'TstValue'))
        print('-'*92)
        print(*(self._FMT.format(*m) for m in mismatches), sep='\n')
        print()

    @staticmethod
    def data_mismatches_none(column: str):
        """Print message for no data mismatches.

        Args:
            column (str): Name of the column being analysed.

        """
        ui.print_(f'\nNo data mismatches for {column}', fore='green')


class DataFrameDiff:
    """Test and report differences in two pandas DataFrames.

    Args:
        df_source (pd.DataFrame): DataFrame containing **source** data.
            This dataset holds the **expected** results.
        df_test (pd.DataFrame): DataFrame containing the **test** data.
            This dataset is compared against the 'expected' dataset.

    """

    def __init__(self, df_source: pd.DataFrame, df_test: pd.DataFrame):
        """DataFrame difference class initialiser."""
        self._df_s = df_source
        self._df_t = df_test
        self._col_mismatches = []
        self._msg = _Messages()

    def diff(self):
        """Compare DataFrames and report the differences."""
        self._get_mismatches()
        self._report()

    def _get_mismatches(self):
        """Build a list of columns with mismatches."""
        # Add column to list if it contains a mismatch.
        mis = [col for col in self._df_s.columns
               if not self._df_t[col].equals(self._df_s[col])]
        if mis:
            self._msg.column_mismatches(columns=self._col_mismatches)
        else:
            self._msg.column_mismatches_none()
        self._col_mismatches = mis

    def _report(self) -> None:
        """Compare values in mismatched columns and report."""
        for col in self._col_mismatches:
            mismatches = []
            # Zip source and test datasets.
            for (idx1, row1), (idx2, row2) in zip_longest(self._df_s.iterrows(),
                                                          self._df_t.iterrows(),
                                                          fillvalue=(None, None)):
                # Catch if a row exists in one dataset and not the other.
                if any([row1 is None, row2 is None]):
                    idx1 = idx1 if idx1 is not None else idx2
                    idx2 = idx2 if idx2 is not None else idx1
                    val1 = str(row1[col]) if row1 is not None else 'no value (source)'
                    val2 = str(row2[col]) if row2 is not None else 'no value (test)'
                # Convert datetimes to string for compare.
                elif isinstance(row2[col], pd.Timestamp):
                    val1 = str(row1[col])
                    val2 = str(row2[col])
                # Enable compare of nan types.
                elif any([pd.isna(row1[col]), pd.isna(row2[col])]):
                    # Convert mismatched nan/NaT types to 'NaT' string.
                    if all([pd.isna(row1[col]), row2[col] is pd.NaT]):
                        val1 = 'NaT'
                        val2 = 'NaT'
                    else:
                        val1 = str(row1[col])
                        val2 = str(row2[col])
                # Reformat floats to align.
                elif any([isinstance(row1[col], float), isinstance(row2[col], float)]):
                    val1 = round(float(row1[col]), 5)
                    val2 = round(float(row2[col]), 5)
                else:
                    # Convert to string for each compare.
                    val1 = str(row1[col])
                    val2 = str(row2[col])
                # Do the compare.
                if val1 != val2:
                    # Add any mismatches to a list for reporting.
                    mismatches.append((idx1, idx2, val1, val2))
            if mismatches:
                self._msg.data_mismatches(column=col, mismatches=mismatches)
            else:
                self._msg.data_mismatches_none(column=col)
