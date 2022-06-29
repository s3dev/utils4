#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains tests and utilities relating to files and the
            filesystem.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

    Example for comparing two files::

        >>> from utils4 import filesys

        >>> filesys.compare_files(file1='/path/to/file1.txt',
                                  file2='/path/to/file2.txt')
        True


    If the files are expected to have *different* line endings, yet the
    contents are otherwise expected to be the same, pass the ``contents_only``
    argument as ``True``; as this will skip the file signature test::

        >>> from utils4 import filesys

        >>> filesys.compare_files(file1='/path/to/file1.txt',
                                  file2='/path/to/file2.txt',
                                  contents_only=True)
        True

"""
# pylint: disable=invalid-name

import os
import stat

_SIZE = 16*1024  # 16 KiB


def compare_files(file1: str,
                  file2: str,
                  encoding: str='utf-8',
                  contents_only: bool=False,
                  sig_only: bool=False) -> bool:
    """Test if two files are the same.

    This method is *modelled* after the built-in :func:`~filecmp.cmp` function,
    yet has been modified to *ignore* line endings. Meaning, if two files have
    the same signature and the contents are the same, except for the line
    endings, a result of True is returned.

    Args:
        file1 (str): Full path to a file to be tested.
        file2 (str): Full path to a file to be tested.
        encoding (str, optional): Encoding to be used when reading the files.
            Defaults to 'utf-8'.
        contents_only (bool, optional): Only compare the file contents, do not
            test the signatures. This is useful if the line endings are
            expected to be different, as a file with DOS line endings will be
            marginally larger than a file with UNIX line endings; meaning
            the file signature test will *fail*. Defaults to False.
        sig_only (bool, optional): Only compare the file signatures. The files'
            contents are *not* compared. Defaults to False.

    :Tests:
        If any of the following tests fail, a value of False is returned
        immediately, and no further tests are conducted.

        The following tests are conducted, given default function parameters:

        - Test both files are 'regular' files.
        - Test the files have the same size (in bytes), they are both regular
          files and their inode mode is the same.
        - Test the contents are the same; ignoring line endings.

    Returns:
        bool: True if *all* tests pass, indicating the files are the same;
        otherwise False.

    """
    if contents_only:
        return _compare_content(file1=file1, file2=file2, encoding=encoding)
    sig1 = _sig(file1)
    sig2 = _sig(file2)
    if sig1[1] != stat.S_IFREG | sig2[1] != stat.S_IFREG:
        return False
    if sig_only:
        # Only compare signatures.
        return sig1 == sig2
    if sig1 != sig2:
        # Shortcut to bypass file content compare.
        return False
    return _compare_content(file1=file1, file2=file2, encoding=encoding)

def _compare_content(file1: str, file2: str, encoding: str='utf-8') -> bool:
    """Compare the content of each file.

    Args:
        file1 (str): Full path to a file to be tested.
        file2 (str): Full path to a file to be tested.
        encoding (str, optional): Encoding to be used when reading the files.
            Defaults to 'utf-8'.

    This function short-circuits once a difference is found and immediately
    returns False.

    Returns:
        bool: True if the file contents are the same, otherwise False.

    """
    with open(file1, 'r', encoding=encoding) as f1, open(file2, 'r', encoding=encoding) as f2:
        while True:
            data1 = f1.read(_SIZE)
            data2 = f2.read(_SIZE)
            if data1 != data2:
                return False
            # Both files have reached EOF and are the same.
            if not data1 and not data2:
                return True

def _sig(file: str) -> tuple:
    """Build a tuple containing elements of a file's signature.

    Args:
        file (str): Full path to the file to be tested.

    Returns:
        tuple: A tuple containing elements of the file's signature, as::

            (file size, file type, inode mode)

    """
    st = os.stat(file)
    return (st.st_size, stat.S_IFMT(st.st_mode), st.st_mode)
