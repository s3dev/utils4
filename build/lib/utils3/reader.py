#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains purpose-built data readers.

:Platform:  Linux/Windows | Python 3.8
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments: n/a

:Example:
    Example code use::

        from utils3.reader import reader
        df = reader.read_xls('/path/to/file.xls')

"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import io
import os
import pandas as pd
import xlrd
from datetime import datetime as dt


class Reader():
    """Class wrapper for various data reading methods.

    For details on each reader, refer to the docstring for that reader.

    """

    @staticmethod
    def read_xls(filepath: str,
                 encoding: str='utf-8',
                 sheet_index: int=0,
                 skiprows: int=0,
                 skipcols: int=0,
                 chopcols: int=0,
                 date_formats: dict=None,
                 errors: str='coerce',
                 fill_date_errors: bool=False) -> pd.DataFrame:
        """Read an XLS file into a DataFrame.

        This function is designed to deal with *old* XLS files which
        the ``pandas.read_excel`` function does not support.

        Args:
            filepath (str): Full path to the file to be read.
            encoding (str, optional): Encoding used to read the XLS file.
                Defaults to 'utf-8'.
            sheet_index (int, optional): Index of the sheet to be read.
                Defaults to 0.
            skiprows (int, optional): Number of rows to skip (from the
                beginning of the file). Defaults to 0.
            skipcols (int, optional): Number of columns to skip (from the left).
                Defaults to 0.
            chopcols (int, optional): Number of columns to skip/chop (from the
               right). Defaults to 0.
            date_formats (dict, optional): Dictionary of
                ``{col_name: strftime_mask}``. Defaults to None.
            errors (str, optional): Method used by ``pandas.read_csv`` to
                resolve date parsing errors. Defaults to 'coerce'.
            fill_date_errors (bool, optional): Fill coerced NaT date errors
                with '1900-01-01'. Defaults to False.

        :Logic:
            The passed XLS file is opened and parsed by ``xlrd``,
            then read into an in-memory stream buffer, which is
            passed into ``pandas.read_csv`` for conversion to a
            DataFrame.

        Raises:
            ValueError: If the file extension is not 'xls'.
            IOError: If the workbook does not contain any rows of data.

        Returns:
            df (pd.DataFrame): A DataFrame containing the contents of
            the XLS file.

        """
        if os.path.splitext(filepath)[1].lower() != '.xls':
            raise ValueError('The file *must* be an XLS file.')
        chopcols = -chopcols if chopcols else None
        stream = io.StringIO(newline='\n')
        wb = xlrd.open_workbook(filepath, encoding_override=encoding)
        ws = wb.sheet_by_index(sheet_index)
        if not ws.nrows:
            raise IOError('This workbook does not contain any rows of data.')
        rows = ws.get_rows()
        if skiprows:
            for i in range(skiprows):
                next(rows)
        for i in rows:
            stream.write(','.join(j.value for j in i[skipcols:chopcols]) + '\n')
        _ = stream.seek(0)
        df = pd.read_csv(stream)
        if date_formats:
            for col, fmt in date_formats.items():
                df[col] = pd.to_datetime(df[col], format=fmt, errors=errors)
                if fill_date_errors:
                    df[col].fillna(dt(1900,1,1), inplace=True)
        stream.close()
        return df


reader = Reader()
