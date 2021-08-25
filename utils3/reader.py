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

import io
import os
import pandas as pd
import xlrd


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
                 chopcols: int=0) -> pd.DataFrame:
        """Read an XLS file into a DataFrame.

        This function is designed to deal with *old* XLS files which
        the ``pandas.read_excel`` function does not support.

        Args:
            filepath (str): Full path to the file to be read.
            encoding (str): Encoding used to read the XLS file.
                Defaults to 'utf-8'.
            sheet_index (int): Index of the sheet to be read.
                Defaults to 0.
            skiprows (int): Number of rows to skip (from the beginning
                of the file). Defaults to 0.
            skipcols (int): Number of columns to skip (from the left).
                Defaults to 0.
            chopcols (int): Number of columns to skip/chop (from the
               right). Defaults to 0.

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
        stream.close()
        return df


reader = Reader()
