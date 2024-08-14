#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains purpose-built data readers for formats
            which are no longer supported, namely:

            - **.xls:** pre-Excel 5.0/95 Workbook

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments: n/a

:Example:

    Example for reading an old-style .xls (pre-Excel 5.0/95) Workbook into a
    DataFrame::

        >>> from utils4.reader import reader
        >>> df = reader.read_xls('/path/to/file.xls')

"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import io
import os
import pandas as pd
import xlrd
from datetime import datetime as dt


class Reader:
    """Class wrapper for various data reading methods.

    For details on each reader, refer to the docstring for that reader.

    """

    def read_xls(self,
                 filepath: str,
                 encoding: str=None,
                 sheet_index: int=0,
                 skiprows: int=0,
                 skipcols: int=0,
                 chopcols: int=0,
                 date_formats: dict=None,
                 errors: str='coerce',
                 fill_date_errors: bool=False) -> pd.DataFrame:
        """Read a pre-Excel 5.0/95 .XLS file into a DataFrame.

        This function is designed to deal with *old* XLS files which
        the ``pandas.read_excel`` function *does not support*.

        Args:
            filepath (str): Full path to the file to be read.
            encoding (str, optional): Encoding used to read the XLS file.
                Defaults to None.
            sheet_index (int, optional): Index of the sheet to be read,
                zero-based. Defaults to 0.
            skiprows (int, optional): Number of rows to skip (from the
                beginning of the file). Defaults to 0.
            skipcols (int, optional): Number of columns to skip (from the left).
                Defaults to 0.
            chopcols (int, optional): Number of columns to skip/chop (from the
               right). Defaults to 0.
            date_formats (dict, optional): Dictionary of
                ``{col_name: strftime_mask}``. Defaults to None.
            errors (str, optional): Method used by :func:`~pandas.read_csv` to
                resolve date parsing errors. Defaults to 'coerce'.
            fill_date_errors (bool, optional): Fill coerced NaT date errors
                with '1900-01-01'. Defaults to False.

        :Logic:
            The passed XLS file is opened and parsed by the ``xlrd`` library,
            then read into an in-memory stream buffer, which is
            passed into ``pandas.read_csv`` function for conversion to a
            DataFrame.

        Raises:
            ValueError: If the file extension is not ``.xls``.
            IOError: If the workbook does not contain any rows of data.

        Returns:
            df (pd.DataFrame): A DataFrame containing the contents of
            the XLS file.

        """
        if os.path.splitext(filepath)[1].lower() != '.xls':
            raise ValueError('The file *must* be an XLS file.')
        chopcols = -chopcols if chopcols else None
        stream = io.StringIO(newline='\n')
        wb = xlrd.open_workbook(filepath, encoding_override=encoding, formatting_info=True)
        ws = wb.sheet_by_index(sheet_index)
        if not ws.nrows:
            raise IOError('This workbook does not contain any rows of data.')
        rows = ws.get_rows()
        if skiprows:
            for _ in range(skiprows):
                next(rows)
        for r in rows:
            row = r[skipcols:chopcols]
            # Ensure xldate formats are parsed correctly.
            data = self._extract_row(row=row)
            stream.write(data + '\n')
        _ = stream.seek(0)
        df = pd.read_csv(stream)
        if date_formats:
            for col, fmt in date_formats.items():
                df[col] = pd.to_datetime(df[col], format=fmt, errors=errors)
                if fill_date_errors:
                    # Changed to remove inplace=True due to pandas v3.0 deprecation warnings.
                    df[col] = df[col].fillna(dt(1900,1,1))
        stream.close()
        return df

    @staticmethod
    def _extract_row(row: iter) -> str:
        """Extract and parse each row.

        Args:
            row (iter): Iterable object which is converted into a string,
                separated by the separator specified by the ``sep`` argument.
            sep (str, optional): Separator character. Defaults to ``','``.

        Returns:
            str: A string containing all row values, separated by the ``sep``
            character.

        """
        def _value_generator(row: iter) -> str:
            """Parse each row value based on its ``xf_index`` value.

            Args:
                row (iter): Iterable object.

            Yields:
                str: Each parsed value from the iterable.

            """
            for i in row:
                if i.xf_index == 62:
                    val = xlrd.xldate.xldate_as_datetime(i.value, 0)
                else:
                    val = i.value
                yield str(val)
        return ','.join(_value_generator(row=row))


reader = Reader()
