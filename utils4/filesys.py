#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains tests and utilities relating to files and the
            filesystem.

:Platform:  Linux/Windows | Python 3.7+
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
import shutil
import stat
from glob import glob
from utils4.reporterror import reporterror
try:
    from natsort import natsorted
    _IMP_NATSORT = True
except ImportError:
    # Built-in sorting will be used instead.
    _IMP_NATSORT = False

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

def dirsplit(path: str,
             nfiles: int,
             pattern: str='*',
             pairs: bool=False,
             repl: tuple=(None,)) -> bool:
    """Move all files from a single directory into (n) sub-directories.

    Args:
        path (str): Full path to the source files. Additionally, all files
            will be moved into sub-directories in this path.
        nfiles (int): Number of source files to be moved into each directory.
        pattern (str, optional): A shell-style wildcard pattern used for
            collecting the source files. For example: ``*.csv``.
            Defaults to '*'.
        pairs (bool, optional): Are the files in pairs?. If True, the ``repl``
            argument is used to replace a sub-string of the source file with
            that of the paired file, so each file pair is moved into the same
            directory. Defaults to False.
        repl (tuple, optional): A tuple containing the old and new replacement
            strings. This argument is only in effect if the ``pairs`` argument
            is True. Defaults to (None,).

            For example::

                ('_input.csv', '_output.txt')

    Raises:
        FileNotFoundError: If the input file path does not exist.

    Returns:
        bool: True if the operation completes, otherwise False.

    """
    if not os.path.exists(path):
        raise FileNotFoundError('The requested path does not exist.')
    success = False
    try:
        # Setup.
        files = [f for f in glob(os.path.join(path, pattern)) if os.path.isfile(f)]
        files = natsorted(files) if _IMP_NATSORT else sorted(files)
        total = len(files)
        i = nfiles
        dirnum = 0
        # File iterator.
        for idx, file in enumerate(files, 1):
            # Define the (next) copy-to directory and create it.
            if i >= nfiles:
                i = 0
                dirnum += 1
                dirnam = str(dirnum).zfill(2)
                dirpath = os.path.join(path, dirnam)
                if not os.path.exists(dirpath):
                    os.mkdir(path=dirpath)
            # Copy source file.
            base = os.path.basename(file)
            dst = os.path.join(path, dirnam, base)
            print(f'Moving {idx} of {total}: {base} -> {dirnam}')
            shutil.move(src=file, dst=dst)
            _file_move_test(fpath=dst)
            if pairs:
                # Copy paired file.
                base2 = base.replace(*repl)
                dst2 = os.path.join(path, dirnam, base2)
                print(rf'\t\-- {base2} -> {dirnam}')
                shutil.move(src=os.path.join(path, base2), dst=dst2)
                _file_move_test(fpath=dst2)
            i += 1
        success = True
    except FileNotFoundError as ferr:  # progma nocover (cannot test)
        # Designed to catch / print file move errors from _file_move_test().
        print(ferr)
    except Exception as err:
        reporterror(err)
    return success

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

def _file_move_test(fpath: str) -> bool:
    """Test a file exists.

    This method is used to verify the subject file was moved successfully.

    Args:
        fpath (str): File path to be tested.

    Raises:
        FileNotFoundError: If the subject file does not exist.

    Returns:
        bool: True if the file was moved successfully, otherwise False.

    """
    if not os.path.exists(fpath):
        msg = ('\nThe following file was not copied successfully. Processing aborted.\n'
               f'-- {fpath}\n')
        raise FileNotFoundError(msg)
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
