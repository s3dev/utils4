#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``utils`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=wrong-import-order
# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods

import contextlib
import io
import os
import pandas as pd
import pickle
import platform
import shutil
import site
import sys
from datetime import datetime as dt
from glob import glob
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4 import utils
from utils4.crypto import crypto


class TestUtils(TestBase):
    """Testing class used to test the ``utils`` module."""

    _DIR1 = os.path.join(TestBase._DIR_TMP, 'path/to/create')
    _DIR2 = os.path.join(TestBase._DIR_TMP, 'path/to/create/file.csv')
    _FP10_1 = os.path.join(TestBase._DIR_TMP, 'rand.txt')
    _FP10_2 = f'{_FP10_1}.gz'
    _FP10_3 = f'{_FP10_1}.bak'
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases.

        :Tasks:
            - Notify user of the module being tested.
            - Remove the directories created by the ``direxists`` method.

        """
        msgs.startoftest.startoftest(module_name='utils')
        cls._test02__rmdir()
        cls._test10__rm_files()

    @classmethod
    def tearDownClass(cls):
        """Run this logic at the end of all test cases.

        :Tasks:
            - Remove the files created by the ``gzip_*`` tests.

        """
        cls._test10__rm_files()

    def tearDown(self):
        """Run this logic *after* each test case."""
        self._test02__rmdir()

    def test01__clean_dataframe(self):
        """Test the ``clean_dataframe`` method.

        :Test:
            - Read the testing (dirty) and expected (clean) DataFrames from
              the serialised file.
            - Verify the in-place cleaned copy of the dirty DataFrame matches
              the expected result.

        """
        with open(os.path.join(self._DIR_RESRC, 'test_utils__clean_dataframe_01.p'), 'rb') as f:
            dictE, dictT = pickle.load(f)  # Read a list of dicts as [dictE, dictT] from the file.
        dfE = pd.DataFrame(dictE)
        dfT = pd.DataFrame(dictT)
        dfC = dfT.copy()
        utils.clean_dataframe(df=dfC)
        utilities.assert_equal_dataframe(df1=dfE, df2=dfC)

    def test02__direxists(self):
        """Test the ``direxists`` method.

        :Test:
            - Verify the testing path does not exist, using built-in.
            - Verify the testing path does not exist, using utils.
            - Verify the testing path does not exist, using utils, and create
              the directory.
            - Verify the testing path does exist, using built-in.
            - Compare the expected results with the test results.

        """
        exp = [False, False, True, True]
        test = []
        test.append(os.path.exists(self._DIR1))
        test.append(utils.direxists(path=self._DIR1, create_path=False))
        test.append(utils.direxists(path=self._DIR1, create_path=True))
        test.append(os.path.exists(self._DIR1))
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test02__direxists__with_file(self):
        """Test the ``direxists`` method, with a filename in the path.

        :Test:
            - Verify the testing path does not exist, using built-in.
            - Verify the testing path does not exist, using utils; exercising
              the filename removal logic.
            - Verify the testing path does not exist, using utils, and create
              the directory, exercising the filename removal logic.
            - Verify the testing path does exist, using built-in.
            - Compare the expected results with the test results.

        """
        exp = [False, False, True, True]
        test = []
        test.append(os.path.exists(self._DIR2))
        test.append(utils.direxists(path=self._DIR2, create_path=False))
        test.append(utils.direxists(path=self._DIR2, create_path=True))
        test.append(os.path.exists(os.path.dirname(self._DIR2)))
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test03__fileexists(self):
        """Test the ``fileexists`` method, with an existant file.

        :Test:
            - Verify the method returns True, using this module's filepath.

        """
        fp = os.path.realpath(__file__)
        test = utils.fileexists(filepath=fp)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test03__fileexists__ignore(self):
        """Test the ``fileexists`` method, using errors='ignore'.

        :Test:
            - Verify the method returns False and shows no output to the
              terminal.

        """
        exp = (False, '')
        buff = io.StringIO()
        with contextlib.redirect_stdout(buff):
            test1 = utils.fileexists(filepath=self._DIR2, error='ignore')
            test2 = buff.getvalue()
        utilities.assert_true(expected=exp, test=(test1, test2), msg=self._MSG1)

    def test03__fileexists__alert(self):
        """Test the ``fileexists`` method, using errors='alert'.

        :Test:
            - Verify the method returns False and notifies the user the file
              does not exist.

        """
        exp = (False, True)
        msg = f'File not found: {self._DIR2}'
        buff = io.StringIO()
        with contextlib.redirect_stdout(buff):
            test1 = utils.fileexists(filepath=self._DIR2, error='alert')
            test2 = buff.getvalue()
        utilities.assert_true(expected=exp, test=(test1, msg in test2), msg=self._MSG1)

    def test03__fileexists__raise(self):
        """Test the ``fileexists`` method, using errors='raise'.

        :Test:
            - Verify the method raises a FileNotFoundError.

        """
        with self.assertRaises(FileNotFoundError):
            utils.fileexists(filepath=self._DIR2, error='raise')

    def test04__format_exif_date__str(self):
        """Test the ``format_exif_date`` method, returning a string.

        :Test:
            - Verify the *default* values of the method return the expected
              results.

        """
        inp = '2022:03:28 20:50:00'
        exp = '20220328205000'
        test = utils.format_exif_date(datestring=inp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__format_exif_date__datetime(self):
        """Test the ``format_exif_date`` method, returning a datetime object.

        :Test:
            - Verify the *default* values of the method return the expected
              results.

        """
        inp = '2022:03:28 20:50:00'
        exp = dt(2022,3,28,20,50)
        test = utils.format_exif_date(datestring=inp, return_datetime=True)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test05__get_os(self):
        """Test the ``get_os`` method.

        :Test:
            - Verify the method returns the platform's system, in lower
              case.

        """
        exp = platform.system().lower()
        test = utils.get_os()
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test06__getsitepackages(self):
        """Test the ``getsitepackages`` method.

        :Test:
            - Verify the method returns the platform-expected site-packages
              directory.
              - On Windows this is index 1, and on Linux this is index 0.

        """
        _os = platform.system().lower()
        if 'lin' in _os:
            exp = site.getsitepackages()[0]
        elif 'win' in _os:
            exp = site.getsitepackages()[1]
        else:
            exp = None
        test = utils.getsitepackages()
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test10__0__setup(self):
        """Create the testing files used by test10."""
        self._test10__create_file()

    def test10__1__gzip_compress(self):
        """Test the ``gzip_compress`` method.

        :Test:
            - Verify the gzip file does *not* exist.
            - Create the compressed gzip file.
            - Verify the gzip file does exist.
            - Verify the filename returned by the method is as expected.

        """
        exp = [False, True, True]
        test1 = os.path.exists(self._FP10_2)
        fp = utils.gzip_compress(in_path=self._FP10_1)
        test2 = os.path.exists(fp)
        test3 = fp == self._FP10_2
        utilities.assert_true_pyiter(expected=exp, test=[test1, test2, test3], msg=self._MSG1)

    def test10__2__gzip_decompress(self):
        """Test the ``gzip_decompress`` method.

        :Test:
            - Decompress the test file, compressed by the previous test.
            - Compare the MD5 hash of the decompressed file with the backup
              of the original file, and verify the hashes are the same.

        """
        exp = [True, True]
        test1 = utils.gzip_decompress(path=self._FP10_2)
        md5_1 = crypto.checksum_md5(path=self._FP10_1)
        md5_2 = crypto.checksum_md5(path=self._FP10_3)
        test2 = md5_1 == md5_2
        utilities.assert_true_pyiter(expected=exp, test=[test1, test2], msg=self._MSG1)

    def test07__ping__127001(self):
        """Test the ``ping`` method, on 127.0.0.1.

        :Test:
            - Verify a ping of 127.0.0.1 returns True.

        """
        test = utils.ping(server='127.0.0.1', count=1, verbose=False)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test07__ping__localhost(self):
        """Test the ``ping`` method, on 'localhost'.

        :Test:
            - Verify a ping of 'localhost' returns True.

        """
        test = utils.ping(server='localhost', count=1, verbose=False)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test07__ping__utilss3d(self):
        """Test the ``ping`` method, on utils.s3d.

        :Test:
            - Verify a ping of 'utils.s3d' returns False.

        """
        test = utils.ping(server='utils.s3d', count=1, timeout=2, verbose=False)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test07__ping__utilss3d__verbose(self):
        """Test the ``ping`` method, on utils.s3d with verbose output.

        :Test:
            - Verify a ping of 'utils.s3d' returns False and produces a
              verbose output to stdout.

        """
        buff = io.StringIO()
        exp1 = '[PingError]:'
        if 'win' in sys.platform.lower():
            exp2a = ('Ping request could not find host utils.s3d. '
                    'Please check the name and try again.')
            exp2b = 'UNUSED'
        else:
            exp2a = 'ping: utils.s3d: Name or service not known'
            exp2b = 'Temporary failure'
        with contextlib.redirect_stdout(buff):
            test1 = utils.ping(server='utils.s3d', count=1, timeout=2, verbose=True)
            test2 = buff.getvalue()
        utilities.assert_true(expected=True,
                              test=all([test1 is False,
                                        exp1 in test2,
                                        exp2a in test2 or exp2b in test2]),
                              msg=self._MSG1)

    def test07__ping__192168099__verbose(self):
        """Test the ``ping`` method, on 192.168.0.99 with verbose output.

        :Test:
            - Verify a ping of '192.168.0.99' returns False and produces a
              verbose output to stdout.

        """
        buff = io.StringIO()
        # All strings generalised for Win/Lin compatibility.
        exp1 = '[pingerror]:'
        exp2a = 'bytes of data'
        exp2b = 'unreachable'
        # exp3 = 'destination host unreachable'
        exp4 = 'statistics'
        exp5 = 'packets'
        with contextlib.redirect_stdout(buff):
            test1 = utils.ping(server='192.168.0.99', count=1, timeout=2, verbose=True)
            test2 = buff.getvalue().lower()
        utilities.assert_true(expected=True,
                              test=all([test1 is False,
                                        exp1 in test2,
                                        exp2a in test2 or exp2b in test2,
                                        # exp3 in test2,
                                        exp4 in test2 or exp2b in test2,
                                        exp5 in test2 or exp2b in test2]),
                              msg=self._MSG1)

    def test08__testimport__os(self):
        """Test the ``testimport`` method, on the ``os`` library.

        :Test:
            - Verify the method returns True for the ``os`` library.

        """
        test = utils.testimport(module_name='os', verbose=False)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test08__testimport__bob(self):
        """Test the ``testimport`` method, on the ``bob`` library.

        :Test:
            - Verify the method returns False for the ``bob`` library.

        """
        test = utils.testimport(module_name='bob', verbose=False)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test08__testimport__bob__verbose(self):
        """Test the ``testimport`` method, on the ``bob``, with verbose output.

        :Test:
            - Verify the method returns False for the ``bob`` library and
              notifies the user the library is not installed.

        """
        msg = 'Library/module not installed: bob'
        buff = io.StringIO()
        with contextlib.redirect_stdout(buff):
            test1 = utils.testimport(module_name='bob', verbose=True)
            test2 = buff.getvalue()
        utilities.assert_true(expected=(False, True),
                              test=(test1, msg in test2),
                              msg=self._MSG1)

    def test09__unidecode__ascii(self):
        """Test the ``unidecode`` method, with an ASCII string.

        :Test:
            - Verify the same ASCII string is returned.

        """
        exp = 'An ASCII string.'
        string = 'An ASCII string.'
        test = utils.unidecode(string=string)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test09__unidecode__list_of_bytes(self):
        """Test the ``unidecode`` method, with a list of bytes.

        :Test:
            - Verify the same list of bytes is returned.

        """
        exp = [os.urandom(8)]
        test = utils.unidecode(string=exp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test09__unidecode__poland(self):
        """Test the ``unidecode`` method, with a Polish address.

        :Test:
            - Verify the Polish address is returned in ASCII characters.

        """
        exp = 'ul. Baltow 8a 27-423 Baltow, woj. swietokrzyskie'
        string = 'ul. Bałtów 8a 27-423 Bałtów, woj. świętokrzyskie'
        test = utils.unidecode(string=string)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    @classmethod
    def _test02__rmdir(cls):
        """Remove the directories created by test02."""
        path = os.path.join(cls._DIR_TMP, 'path')
        if os.path.exists(path):
            shutil.rmtree(path=path)

    def _test10__create_file(self):
        """Create a large file to be tested by test10."""
        # print('\nTesting gzip.\nCreating large testing file ...')
        with open(self._FP10_1, 'w', encoding='utf-8') as f:
            s = '\n'.join('a, b, c, d, e, f, g' for _ in range(10**7))
            f.write(s)
        shutil.copy(src=self._FP10_1, dst=self._FP10_3)
        # print('Done.')

    @classmethod
    def _test10__rm_files(cls):
        """Remove the files created by test10."""
        files = glob(os.path.join(cls._DIR_TMP, 'rand*'))
        for f in files:
            os.remove(f)
