# -*- coding: utf-8 -*-
"""
:Purpose:   Central library for general utility-based methods.

            This ``utils`` module was the starting place of the original
            ``utils`` library. Therefore, it's historically been a
            'dumping-ground' for general S3DEV utilities and function
            wrappers specialised to the needs of S3DEV projects, which
            did not seem to fit in anywhere else. So we'll be honest,
            it's a bit of a melting pot of functions.

            With the overhaul of the ``utils3`` library into ``utils4``,
            *many* of the original functions, which were no longer being
            used, have been removed in an effort to clean the module's
            code base.

            If you are looking for a function which used to be here,
            please refer to the last ``utils3`` release, which is
            v0.15.1.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

Note:
            Any libraries which are not built-in, are imported *only*
            if/when the function which uses them is called.

            This helps to reduce the packages required by ``utils4``.

:Example:

    For usage examples, please refer to the docstring for each method.

"""
# pylint: disable=import-error
# pylint: disable=import-outside-toplevel  # Keep required dependencies to a minimum.
# pylint: disable=wrong-import-order

from __future__ import annotations

import importlib
import io
import os
import platform
import re
import site
import string
import subprocess
from datetime import datetime
from typing import Generator, Union
# locals
from utils4.reporterror import reporterror
from utils4.user_interface import ui
try:
    # The C library is only available if installed.
    from . import futils  # pylint: disable=no-name-in-module
except ImportError:
    pass

# OS-dependent imports
try:  # pragma: nocover
    import win32api
    import win32file
except ImportError:
    pass


def clean_dataframe(df: pd.DataFrame):  # noqa  # pylint: disable=undefined-variable
    """Clean a ``pandas.DataFrame`` data structure.

    Args:
        df (pd.DataFrame): DataFrame to be cleaned.

    :Design:
        The DataFrame is cleaned *in-place*. An object is *not* returned by
        this function.

        The following cleaning tasks are performed:

            - Column names:

                - All punctuation characters are removed, with the exception
                  of three characters. See next bullet point.
                - The ``-``, ``[space]`` and ``_`` characters are replaced
                  with an underscore.
                - All column names are converted to lower case.

            - Data:

                - All ``object`` (string) fields, are stripped of leading and
                  trailing whitespace.

    :Example:

        Example for cleaning a DataFrame::

            >>> import pandas as pd  # For demonstration only.
            >>> from utils4 import utils

            >>> # Define a dirty testing dataset.
            >>> df = pd.DataFrame({'Column #1': [' Text field 1.',
                                                 '   Text field 2.',
                                                 ' Text field 3.    ',
                                                 '  Text field 4.  ',
                                                 '  Text field 5. '],
                                   '  COLUmn (2)': [1.0,
                                                    2.0,
                                                    3.0,
                                                    '4',
                                                    '5.0'],
                                   'COLUMN 3  ': [1,
                                                  2,
                                                  3.0,
                                                  4,
                                                  5.0]})
            >>> utils.clean_dataframe(df)
            >>> df
                    column_1 column_2  column_3
            0  Text field 1.      1.0       1.0
            1  Text field 2.      2.0       2.0
            2  Text field 3.      3.0       3.0
            3  Text field 4.        4       4.0
            4  Text field 5.      5.0       5.0

    """
    # Define replacement/translation characters.
    repls = {k: '' for k in string.punctuation}
    repls.update({'-':'_', '_': '_', ' ': '_'})
    trans = str.maketrans(repls)
    # Clean column names.
    df.columns = [c.strip().lower().translate(trans) for c in df.columns]
    # Strip whitespace from text values.
    for col in df:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

def direxists(path: str, create_path: bool=False) -> bool:
    """Test if a directory exists. If not, create it, if instructed.

    Args:
        path (str): The directory path to be tested.
        create_path (bool, optional): Create the path if it doesn't exist.
            Defaults to False.

    :Design:
        Function designed to test if a directory path exists. If the
        path does *not* exist, the path can be created; as determined by
        the ``create_path`` parameter.

        This function extends the built-in :func:`os.path.exists()` function
        in that the path can be created if it doesn't already exist, by
        passing the ``create_path`` parameter as ``True``.

        If the path is created by this function, the function is recursively
        called to test if the path exists, and will return ``True``.

        If a filename is passed with the path, the filename is automatically
        stripped from the path before the test begins.

    :Example:

        Test if a directory exists, and create it if it does not exist::

            >>> from utils4 import utils

            >>> utils.direxists(path='/tmp/path/to_create/file.csv',
                                create_path=True)

    Returns:
        bool: True if the directory exists (or was created), otherwise False.

    """
    found = False
    if os.path.splitext(path)[1]:
        path, _ = os.path.split(path)  # Remove file if passed with the path.
    if os.path.exists(path):
        found = True
    else:
        if create_path:
            os.makedirs(name=path)
            found = direxists(path=path, create_path=False)
    return found

def excludedirs(source: list[str], exclude: list[str]) -> list[str]:
    """Exclude the listed directories from the source.

    Args:
        source (list[str]): List of source paths.
        exclude (list[str]): List of directories to be excluded from
            ``source``.

    :Design:
        The paths in ``exclude`` are expanded to their realpath, with
        a trailing path separator explicitly added to ensure only
        directory paths are matched.

        For example, if the trailing path separator was not added,
        ``.gitignore`` would be excluded if ``./.git`` was in
        ``exclude`` paths. Adding the trailing path separator
        prevents this.

    Returns:
        list[str]: A new list of paths where any ``source`` path
        sharing a common base path with any ``exclude`` path has
        been removed.

    """
    # Cannot be a generator as it's iterated multiple times.
    exclude = tuple(map(lambda x: f'{os.path.realpath(x)}/', exclude))
    return [s for s in source if all(e not in s for e in exclude)]

def fileexists(filepath: str, error: str='ignore') -> bool:
    """Test if a file exists. If not, notify the user or raise an error.

    Args:
        filepath (str): Full file path to test.
        error (bool, optional): Action to be taken if the file does not exist.
            Defaults to 'ignore'. Options:

                - ``'ignore'``: Take no action.
                - ``'alert'``: Alert the user the filepath does not exist via
                  a simple message to the terminal.
                - ``'raise'``: Raise a ``FileNotFoundError``. This will abort
                  all subsequent processing.

    :Design:
        Function designed check if a file exists.  A boolean value is
        returned to the calling program.

        This function extends the built-in :func:`os.path.isfile` function
        in that the user can be notified if the path does not exist, or an
        error can be raised.

    :Example:

        Test if a file exists, using ``'ignore'``, the default action::

            >>> from utils4 import utils

            >>> if utils.fileexists(filepath='/tmp/path/to/file.csv'):
            >>>     ...
            >>> else:
            >>>     ...


        Test if a file exists, using ``'alert'``::

            >>> from utils4 import utils

            >>> if utils.fileexists(filepath='/tmp/path/to/file.csv',
                                    error='alert'):
            >>>     ...
            >>> else:
            >>>     ...

            File not found: /tmp/path/to/file.csv


        Test if a file exists, using ``'raise'``::

            >>> from utils4 import utils

            >>> if utils.fileexists(filepath='/tmp/path/to/file.csv',
                                    error='raise'):
            >>>     ...
            >>> else:
            >>>     ...

            FileNotFoundError: File not found: /tmp/path/to/file.csv

    Raises:
        FileNotFoundError: If the filepath does not exist and the ``error``
            parameter is ``'raise'``.

    Returns:
        bool: True if the file exists, otherwise False.

    """
    found = False
    if os.path.isfile(filepath):
        found = True
    else:
        if error == 'alert':
            ui.print_warning(f'\nFile not found: {filepath}')
        elif error == 'raise':
            raise FileNotFoundError(f'File not found: {filepath}')
    return found


def format_exif_date(datestring: str,
                     input_format: str='%Y:%m:%d %H:%M:%S',
                     output_format: str='%Y%m%d%H%M%S',
                     return_datetime: bool=False) -> Union[datetime, str]:
    """Format an exif timestamp.

        This function is useful for storing an exif date as a datetime string.
        For example, extracting the exif data from an image to be stored into
        a database.

    Args:
        datestring (str): The datetime string to be formatted.
            A typical exif date format is: yyyy:mm:dd hh:mi:ss
        input_format (str, optional): Format mask for the input datetime value.
            Defaults to '%Y:%m:%d %H:%M:%S'.
        output_format (str, optional): Format mask for the output datetime,
            if returned as a string. Defaults to '%Y%m%d%H%M%S'.
        return_datetime (bool, optional): Return a ``datetime`` object, rather
            than a formatted string.

    :Design:
        Function designed to convert the exif date/timestamp from
        '2010:01:31 12:31:18' (or a caller specified format) to a format
        specified by the caller.

        The default input mask is the standard exif capture datetime format.

    :Example:

            Convert the exif datetime to the default output string format::

                >>> from utils4 import utils

                >>> formatted = utils.format_exif_date('2010:01:31 12:31:18')
                >>> formatted
                '20100131123118'


            Convert the exif datetime to a datetime object::

                >>> from utils4 import utils

                >>> formatted = utils.format_exif_date('2010:01:31 12:31:18',
                                                       return_datetime=True)
                >>> formatted
                datetime.datetime(2010, 1, 31, 12, 31, 18)


    Returns:
        Union[str, datetime.datetime]: A formatted datetime string, if the
        ``return_datetime`` parameter is ``False``, otherwise a
        ``datetime.datetime`` object.

    """
    # pylint: disable=no-else-return
    _dt = datetime.strptime(datestring, input_format)
    if return_datetime:
        return _dt
    else:
        return _dt.strftime(output_format)

def get_os() -> str:
    """Get the platform's OS.

    This method is a very thin wrapper around the :func:`platform.system()`
    function.

    :Example:
        ::

            >>> from utils4 import utils

            >>> utils.get_os()
            'linux'

    Returns:
        str: A string of the platform's operating system, in lower case.

    """
    return platform.system().lower()

def get_removable_drives() -> Generator[str, str, str]:
    """Return a generator of removable drives.

    .. important::

        This is a Windows-only function.

    Note:
        A removable drive is identified by the constant 2, which is the
        value of the enum ``win32con.DRIVE_REMOVABLE``.

        This code uses the integer 2 to:

            1) Save the extra import.
            2) Help keep the code compact, concise and clear.

    :Example:

        To obtain a list of removable drives from a Windows system::

            >>> from utils4 import utils

            >>> list(utils.get_removable_drives())
            ['E:', 'H:']

    Raises:
        NotImplementedError: Raised if the OS is not Windows.

    Yields:
        Generator[str]: Each removable drive letter as a
        string. For example: ``'E:'``

    """
    if get_os() == 'windows':  # pragma: nocover
        yield from filter(lambda x: win32file.GetDriveType(x) == 2,
                          win32api.GetLogicalDriveStrings().split('\\\x00'))
    else:
        raise NotImplementedError('This function is Windows-only.')

def getdrivername(driver: str, return_all: bool=False) -> list:  # pragma: nocover
    """Return a list of ODBC driver names, matching the regex pattern.

    Args:
        driver (str): A **regex pattern** for the ODBC driver you're searching.
        return_all (bool, optional): If True, *all* drivers matching the
            pattern are returned. Defaults to False, which returns only the
            first driver name.

    :Design:
        This is a helper function designed to get and return the names
        of ODBC drivers.

        The ``driver`` parameter should be formatted as a regex
        pattern. If multiple drivers are found, by default, only the
        first driver in the list is returned. However, the
        ``return_all`` parameter adjusts this action to return all driver
        names.

        This function has a dependency on the ``pyodbc`` library. Therefore,
        the :func:`~utils.testimport()` function is called before ``pyodbc``
        is imported. If the ``pyodbc`` library is not installed, the user is
        notified.

    :Dependencies:
        - ``pyodbc`` library

    :Example:

            Get the driver name for the SQL Server ODBC driver::

            >>> from utils4 import utils
            >>> driver = utils.getdrivername(driver='SQL Server.*')

    :Troubleshooting:

        - On Unix-like systems, the following error message::

            ImportError: libodbc.so.2: cannot open shared object file: No such file or directory

          can be resolved by installing the ``unixodbc-dev`` package as::

            $ sudo apt install unixodbc-dev

    Returns:
        list: A list of ODBC drivers, if any were found.

    """
    drivers = []
    if testimport('pyodbc', verbose=True):
        import pyodbc
        drivers = [i for i in pyodbc.drivers() if re.search(driver, i)]
        if not return_all and drivers:
            drivers = drivers[0]
    return drivers

def getsitepackages() -> str:
    """Return the Python installation's site packages directory.

    :Design:
        The function first uses the local :func:`~utils.get_os()`
        function to get the system's OS. The OS is then tested and the
        site-packages location is returned using the OS-appropriate element
        from the list returned by the built-in :func:`site.getsitepackages`
        function.

        If the OS is not accounted for, or fails the test, a value of
        'unknown' is returned.

    :Rationale:
        The need for this function comes out of the observation there are many
        (many!) different ways on stackoverflow (and other sites) to get the
        location to which ``pip`` will install a package, and many of the
        answers contradict each other. Also, the :func:`site.getsitepackages`
        function returns a list of options (in all tested cases); and the
        Linux / Windows paths are in different locations in this list.

    :Example:

            Get the location of the ``site-packages`` directory::

            >>> from utils4 import utils

            >>> utils.getsitepackages()
            '/home/<username>/venvs/py38/lib/python3.8/site-packages'

    Returns:
        str: Full path to the ``site-packages`` directory.

    """
    _os = get_os()
    pkgs = 'unknown'
    if 'win' in _os:  # pragma: nocover  # utils4 will *rarely* ever be tested on Windows.
        pkgs = site.getsitepackages()[1]
    elif 'lin' in _os:
        pkgs = site.getsitepackages()[0]
    return pkgs

def gzip_compress(in_path: str, out_path: str=None, size: int=None) -> str:
    """Compress a file using ``gzip``.

    Args:
        in_path (str): Full path to the file to be compressed. If the file
            does not exist, a ``FileNotFoundError`` is raised.
        out_path (str, optional): Full path to the compressed output file.
            Defaults to None. If this value is ``None`` a ``'.gz'`` file
            extension is appended to the path provided to the ``in_path``
            parameter.
        size (int, optional): Size of the chunk to be read / written during
            compression. Defaults to 10MiB.

    :Example:

        Compress a text file::

            >>> from utils4 import utils

            >>> utils.gzip_compress(in_path='/tmp/rand.txt')
            '/tmp/rand.txt.gz'


        Compress a text file, specifying the output path::

            >>> from utils4 import utils

            >>> utils.gzip_compress(in_path='/tmp/rand.txt', out_path='/tmp/rand2.txt.gz')
            '/tmp/rand2.txt.gz'

    Returns:
        str: Full path to the output file.

    """
    import gzip
    size = 1024*1024*10 if size is None else size  # Default to 10MiB.
    if fileexists(filepath=in_path, error='raise'):
        if out_path is None:
            out_path = f'{in_path}.gz'
        with open(in_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
            chunk = f_in.read(size)
            while len(chunk) > 0:
                comp = gzip.compress(data=chunk, compresslevel=9)
                f_out.write(comp)
                chunk = f_in.read(size)
    return out_path

def gzip_decompress(path: str, encoding: str='utf-8', size: int=None) -> bool:
    """Decompress a ``.gz`` file using ``gzip``.

    Args:
        path (str): Full path to the file to be decompressed. If the file
            does not exist, a ``FileNotFoundError`` is raised.
        encoding (str, optional): Encoding to be used to decode the
            decompressed binary data. Defaults to 'utf-8'.
        size (int, optional): Size of the chunk to be read / written during
            decompression. Defaults to 1MiB.

    Note:
        The output path is simply the ``path`` value with *last* file
        extension removed.

        In general cases, a file compressed using gzip will have a ``.gz``
        extension appended onto the existing filename and extension.
        For example: ``data.txt.gz``.

    Note:
        **Newline Characters:**

        When the decompressed file is written, the ``newline`` character is
        specified as ``''``, which enables 'universal newline mode', whereby
        the system's newline character is used. However, the *original* line
        endings - those used in the compressed file - are written back to the
        decompressed file.

        This method is used to ensure the checksum hash on the original
        (unzipped) and decompressed file can be compared.

    :Example:

        Decompress a text file::

            >>> from utils4 import utils

            >>> utils.gzip_decompress(path='/tmp/rand.txt.gz')
            True

    Returns:
        bool: True if the decompression was successful, otherwise False.

    """
    # pylint: disable=line-too-long
    import gzip
    size = (1<<2)**10 if size is None else size  # Default to 1 MiB.
    success = False
    try:
        if fileexists(filepath=path, error='raise'):
            out_path = os.path.splitext(path)[0]
            with open(path, 'rb') as f_in, open(out_path, 'w', encoding='utf-8', newline='') as f_out:
                chunk = f_in.read(size)
                while len(chunk) > 1:
                    decomp = gzip.decompress(data=chunk).decode(encoding=encoding)
                    f_out.write(decomp)
                    chunk = f_in.read(size)
            success = True
    except Exception as err:
        reporterror(err)
    return success

# Tested by the test_x_futils module.
def isascii(path: str, size: int=2048) -> bool:  # pragma: nocover
    """Determine if a file is plain-text (ASCII only).

    A file is deemed non-binary if *all* of the characters in the file
    are within ASCII's printable range.

    Args:
        path (str): Full path to the file to be tested.
        size (int, optional): Number of bytes to read in a chunk.
            Defaults to 2048 (2 MiB).

    :Example:

        Test if a file is a plain-text (ASCII-only) file::

            >>> from utils4 import utils

            >>> utils.isascii('/usr/local/bin/python3.12-config')
            True

    :Design:
        This function simply inverts the return value of the
        :func:`isbinary` function. For design detail, refer to the
        :meth:`isbinary` documentation.

        This method calls the :func:`futils.isascii` function with the
        given arguments.

    Returns:
        bool: True if *all* characters in the file are plain-text
        (ASCII only), otherwise False.

    """
    return bool(futils.isascii(path, size))

# Tested by the test_x_futils module.
def isbinary(path: str, size: int=1024) -> bool:  # pragma: nocover
    """Determine if a file is binary.

    A file is deemed non-binary if *all* of the characters in the file
    are within ASCII's printable range. Refer to the **References**
    section for further definition.

    Args:
        path (str): Full path to the file to be tested.
        size (int, optional): Number of bytes to read in a chunk.
            Defaults to 1024 (1 MiB).

    :Example:

        Test if a file is a binary file or executable::

            >>> from utils4 import utils

            >>> utils.isbinary('/usr/bin/python3')
            True

    :Design:
        For each chunk of size ``size``, read each character; if the
        character is outside the ASCII printable range, True is returned
        immediately as the file is not plain-text. Otherwise, if a file
        is read to the end, with all characters being within ASCII's
        printable range, False is returned as the file is plain-text
        (ASCII only).

        This method calls the :func:`futils.isbinary` function with the
        given arguments.

    :References:

        - `How to detect if a file is binary <so_ref1_>`_
        - `ASCII printable character reference <so_ref2_>`_

        .. _so_ref1: https://stackoverflow.com/a/7392391/6340496
        .. _so_ref2: https://stackoverflow.com/a/32184831/6340496

    Returns:
        bool: True if *any* of the characters in the file are outside
        ASCII's printable range. Otherwise, False.

    """
    return bool(futils.isbinary(path, size))

# Tested by the test_x_futils module.
def iszip(path: str) -> bool:  # pragma: nocover
    r"""Determine if a file is a ``ZIP`` archive.

    Args:
        path (str): Full path to the file to be tested.

    Tip:
        As Python wheel files are `ZIP-format archives <zip-wheel_>`_
        (per PEP-491), this function can be used to test wheel files as
        well.

    :Example:

        Test if a file is a ZIP archive::

            >>> from utils4 import utils

            >>> utils.iszip('/path/to/file.zip')
            True

        Test if a file is a true Python wheel::

            >>> from utils4 import utils

            >>> utils.iszip('/path/to/sphinx-8.1.3-py3-none-any.whl')
            True

    Note:
        A file is tested to be a ``ZIP`` archive by checking the
        `first four bytes <zip-format_>`_ of the file itself, *not*
        using the file extension.

        It is up to the caller to handle empty or spanned ZIP
        archives appropriately.

    :Design:
        This method calls the :func:`futils.iszip` function with the
        given arguments.

    Returns:
        bool: True if the first four bytes of the file match any of
        the below. Otherwise, False.

        - ``\x50\x4b\x03\x04``: 'Standard' archive
        - ``\x50\x4b\x05\x06``: Empty archive
        - ``\x50\x4b\x07\x08``: Spanned archive

    .. _zip-format: https://en.wikipedia.org/wiki/ZIP_(file_format)#Local_file_header
    .. _zip-wheel: https://peps.python.org/pep-0491/#abstract

    """
    return bool(futils.iszip(path))

def ping(server: str, count: int=1, timeout: int=5, verbose: bool=False) -> bool:
    r"""Ping an IP address, server or web address.

    Args:
        server (str): IP address, server name or web address.
        count (int, optional): The number of ping attempts. Defaults to 1.
        timeout (int, optional): Number of seconds to wait for response.
            Defaults to 5.
        verbose (bool, optional): Display all stdout and/or stderr output, if
            the returned status code is non-zero. Defaults to False.

    :Design:
        Using the platform's native ``ping`` command (via a ``subprocess``
        call) the host is pinged, and a boolean value is returned to the
        caller to indicate if the ping was successful.

        A ping status:

            - 0 returns True
            - Non-zero returns False

        If the server name is preceeded by ``\\`` or ``//``, these are
        stripped out using the built-in :func:`os.path.basename()` function.

    :Example:

        Ping the local PC at 127.0.0.1::

            >>> from utils4 import utils

            >>> utils.ping(server='127.0.0.1')
            True


        Ping an unknown server::

            >>> from utils4 import utils

            >>> utils.ping(server='//S3DHOST01', verbose=True)

            [PingError]:
            ping: S3DHOST01: Temporary failure in name resolution
            False


        Ping an unreachable IP address::

            >>> from utils4 import utils

            >>> utils.ping(server='192.168.0.99', count=3, verbose=True)

            [PingError]:
            PING 192.168.0.99 (192.168.0.99) 56(84) bytes of data.
            From 192.168.0.XX icmp_seq=1 Destination Host Unreachable
            From 192.168.0.XX icmp_seq=2 Destination Host Unreachable
            From 192.168.0.XX icmp_seq=3 Destination Host Unreachable

            --- 192.168.0.99 ping statistics ---
            3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2037ms
            False

    Returns:
        bool: True if the ping was successful, otherwise False.

    """
    cmd = []
    server = os.path.basename(server)
    status = 1
    stdout = None
    stderr = None
    _os = get_os()
    if 'win' in _os:  # pragma: nocover  # utils4 will *rarely* ever be tested on Windows.
        timeout *= 1000  # Windows timeout (-w) is in milliseconds.
        cmd = ['ping', '-n', str(count), '-w', str(timeout), server]
    elif 'lin' in _os:
        cmd = ['ping', f'-c{count}', f'-W{timeout}', server]
    else:  # pragma: nocover
        ui.print_alert('\nProcess aborted, unsupported OS.\n'
                       f'- OS identified as: {_os}\n')
    if cmd:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            status = proc.returncode
    if ('win' in _os) & (b'Destination host unreachable' in stdout):  # pragma nocover
        # Hard code status if host is unreachable.
        # Generally, this will return 0, so it must be overridden.
        status = 1
    if all([verbose, cmd, status != 0]):
        ui.print_alert('\n[PingError]:')
        if stdout:
            ui.print_alert(text=stdout.decode().strip())
        if stderr:
            ui.print_alert(text=stderr.decode().strip())
    return status == 0

def strip_ansi_colour(text: str):
    r"""Strip ANSI colour sequences from a string.

    Args:
        text (str): Text string to be cleaned.

    Note:
        This method is *very* basic and only caters to colour sequences.

        It is designed to yield all characters that are not part of the
        ``\x1b`` sequence start, and the ``m`` sequence end. In other
        words, all text before and after each ``\x1b[M;Nm`` sequence.

    :Example:

        Strip the colouring sequence from terminal text and return a
        single string::

            clean = ''.join(strip_ansi_colour(text))

        Strip the colouring sequence from terminal text and return a list
        of lines, with empty lines removed::

            lines = list(filter(None, ''.join(strip_ansi_colour(text)).split('\n')))

    Yields:
        str: Each character which not part of the ANSI escape sequence
        is yielded to the caller. Essentially, this is a generator
        method.

    """
    # pylint: disable=multiple-statements
    buff = io.StringIO(text)
    while (b := buff.read(1)):
        if b == '\x1b':
            while ( b := buff.read(1) ) != 'm': continue  # Fast-forward from \x1b to m.
        else:
            yield b

def testimport(module_name: str, verbose: bool=True) -> bool:
    """Test if a Python library is installed.

    Args:
        module_name (str): Exact name of the module to be found.
        verbose (bool, optional): Notify if the library is not installed.
            Defaults to True.

    :Design:
        This is a small helper function designed to test if a library is
        installed before trying to import it.

        If the library is not intalled the user is notified, if the ``verbose``
        argument is True.

    :Internal Use:
        For example, the :meth:`~utils.getdrivername` function uses this
        function before attempting to import the ``pyodbc`` library.

    :Example:

        Execute a path only if ``mymodule`` is installed::

            >>> from utils4 import utils

            >>> if utils.testimport('mymodule', verbose=True):
            >>>     import mymodule
            >>>     ...
            >>> else:
            >>>     ...

    Returns:
        bool: True if the library is installed, otherwise False.

    """
    found = False
    if importlib.util.find_spec(module_name):
        found = True
    if (verbose) & (not found):
        ui.print_warning(f'\nLibrary/module not installed: {module_name}')
    return found

def unidecode(string: str, **kwargs) -> str:
    """Attempt to convert a Unicode string object into a 7-bit ASCII string.

    Args:
        string (str): The string to be decoded.
        **kwargs (dict): Keyword arguments passed directly into the underlying
            :func:`unidecode.unidecode` function.

    :Design:
        This function is a light wrapper around the :func:`unidecode.unidecode`
        function.

        **Per the** ``unicode`` **docstring:**

        "Transliterate an Unicode object into an ASCII string."

        Example::

            >>> unidecode(u"北亰")
            "Bei Jing "

        "This function first tries to convert the string using ASCII codec.
        If it fails (because of non-ASCII characters), it falls back to
        transliteration using the character tables."

        "This is approx. five times faster if the string only contains ASCII
        characters, but slightly slower than
        :func:`unidecode.unicode_expect_nonascii` if non-ASCII characters are
        present."

    :Dependencies:

        - ``unidecode`` library

    :Example:

        Convert a Polish address into pure ASCII::

            >>> from utils4 import utils

            >>> addr = 'ul. Bałtów 8a 27-423 Bałtów, woj. świętokrzyskie'
            >>> utils.unidecode(addr)
            'ul. Baltow 8a 27-423 Baltow, woj. swietokrzyskie'


        Convert the first line of 'The Seventh Letter', by Plato::

            >>> from utils4 import utils

            >>> text = 'Πλάτων τοῖς Δίωνος οἰκείοις τε καὶ ἑταίροις εὖ πράττειν.'
            >>> utils.unidecode(text)
            'Platon tois Dionos oikeiois te kai etairois eu prattein.'

    Returns:
        str: If the ``unidecode`` library is installed and the passed
        ``string`` value is a ``str`` data type, the decoded string is
        returned, otherwise the original value is returned.

    """
    # pylint: disable=redefined-outer-name  # No adverse effects and keeps clear variable name.
    if testimport(module_name='unidecode', verbose=True):
        import unidecode as unidecode_
        decoded = unidecode_.unidecode(string, **kwargs) if isinstance(string, str) else string
    else:  # pragma: nocover
        decoded = string
    return decoded
