#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``filesys`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=ungrouped-imports
# pylint: disable=unspecified-encoding

try:
    import contextlib
    import os
    import shutil
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    import contextlib
    import os
    import shutil
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4 import filesys


class TestFileSys(TestBase):
    """Testing class used to test the ``fileyss`` module."""

    _MSG1 = msgs.templates.not_as_expected.general
    _DIR = ''

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='filesys')

    def tearDown(self):
        """Run this logic at the end of each test case."""
        if os.path.exists(self._DIR):
            shutil.rmtree(self._DIR)

    def test01__compare_files__diff1(self):
        """Test the ``compare_files`` method, for different files.

        :Test:
            - Test two text files and verify the contents are different.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__diff1.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__diff1.txt')
        test = filesys.compare_files(file1=f1, file2=f2)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test01__compare_files__diff2(self):
        """Test the ``compare_files`` method, for different files.

        :Test:
            - Test two text files and verify the contents are different,
              although the file signatures are the same.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__diff2.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__diff2.txt')
        test = filesys.compare_files(file1=f1, file2=f2)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test01__compare_files__file_dir(self):
        """Test the ``compare_files`` method, for a file and a directory.

        :Test:
            - Pass a file and a directory into the testing method and verify
              the regular file signature test returns False.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__same.txt')
        f2 = self._DIR_RESRC
        test = filesys.compare_files(file1=f1, file2=f2)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test01__compare_files__line_endings(self):
        """Test the ``compare_files`` method, for the same file with different
        line engines.

        :Test:
            - Test two text files and verify the contents are same, although
              having different line endings.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__dos.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__unix.txt')
        test = filesys.compare_files(file1=f1, file2=f2, contents_only=True)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test01__compare_files__same(self):
        """Test the ``compare_files`` method, for the same files.

        :Test:
            - Test two text files and verify the contents are the same.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__same.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__same.txt')
        test = filesys.compare_files(file1=f1, file2=f2)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test01__compare_files__sig_only__true(self):
        """Test the ``compare_files`` method, testing the signature only, for
        a True result.

        :Test:
            - Test the signature only for two files, expecting a True response.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__same.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__same.txt')
        test = filesys.compare_files(file1=f1, file2=f2, sig_only=True)
        utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test01__compare_files__sig_only__false(self):
        """Test the ``compare_files`` method, testing the signature only, for
        a False result.

        :Test:
            - Test the signature only for two files, expecting a False response.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__diff1.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file2__diff1.txt')
        test = filesys.compare_files(file1=f1, file2=f2, sig_only=True)
        utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test02__sig(self):
        """Test the ``_sig`` method, to verify the returned file signature.

        :Test:
            - Test a series of files, and verify the returned signatures are
              as expected.

        """
        f1 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__same.txt')
        f2 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__diff1.txt')
        f3 = os.path.join(self._DIR_RESRC, 'test_filesys__file1__dos.txt')
        files = [f1, f2, f3]
        exp = ((734, 32768, 33204), (734, 32768, 33204), (744, 32768, 33204))
        for f, e in zip(files, exp):
            with self.subTest(msg=f'{f=} {e=}'):
                tst = filesys._sig(file=f)
                utilities.assert_true(expected=e, test=tst, msg=self._MSG1)

    def test03__dirsplit(self):
        """Test the ``dirsplit`` function to verify the directory is split as
        expected.

        :Test:
            - Create a temp/<hash> directory and create 50 empty testing files.
            - Split the directory.
            - Perform tests to ensure the test files have been distributed
              between the split directories.

        """
        exp = (50, True, 5, [10, 10, 10, 10, 10])
        path = self._create_temp_files()
        tst1 = len(os.listdir(path))
        with contextlib.redirect_stdout(None):  # Suppress stdout.
            tst2 = filesys.dirsplit(path=path, nfiles=10)
        tst3 = len(os.listdir(path))
        tst4 = []
        for dir_ in os.listdir(path):
            tst4.append(len(os.listdir(os.path.join(path, dir_))))
        utilities.assert_true_pyiter(expected=exp,
                                     test=(tst1, tst2, tst3, tst4),
                                     msg=self._MSG1)

    def test03__dirsplit__file_pairs(self):
        """Test the ``dirsplit`` function with file pairs.

        :Test:
            - Create a temp/<hash> directory and create 50 paired empty testing
              files.
            - Split the directory.
            - Perform tests to ensure the test files have been distributed
              between the split directories.

        """
        exp = (100, True, 5, [20, 20, 20, 20, 20])
        path = self._create_temp_files(pairs=True)
        tst1 = len(os.listdir(path))
        with contextlib.redirect_stdout(None):  # Suppress stdout.
            tst2 = filesys.dirsplit(path=path,
                                    nfiles=10,
                                    pattern='*.csv',
                                    pairs=True,
                                    repl=('_thing1.csv', '_thing2.txt'))
        tst3 = len(os.listdir(path))
        tst4 = []
        for dir_ in os.listdir(path):
            tst4.append(len(os.listdir(os.path.join(path, dir_))))
        utilities.assert_true_pyiter(expected=exp,
                                     test=(tst1, tst2, tst3, tst4),
                                     msg=self._MSG1)

    def test04__dirsplit__path_not_exist(self):
        """Test the ``dirsplit`` function with a path which does not exist.

        :Test:
            - Run the ``dirsplit`` function with an invalid path and catch
              the FileNotFoundError error.

        """
        path = os.path.join(self._DIR_DSK, os.urandom(8).hex())
        with self.assertRaises(FileNotFoundError):
            filesys.dirsplit(path=path, nfiles=10)

    def test05__file_move_test(self):
        """Test the ``_file_move_test`` function.

        :Test:
            - Verify the function raises a FileNotFoundError.

        """
        with self.assertRaises(FileNotFoundError):
            filesys._file_move_test('/not/a/real/path')

    def _create_temp_files(self, nfiles: int=50, pairs: bool=False) -> str:
        """Create a /temp/<hash> directory and populate with testing files.

        Returns:
            str: Full path to the created directory.

        """
        # pylint: disable=multiple-statements
        path = os.path.join(self._DIR_TMP, os.urandom(8).hex())
        self._DIR = path
        if not os.path.exists(path):
            os.mkdir(path)
        for i in range(nfiles):
            if pairs:
                with open(os.path.join(path, f'file_{i}_thing1.csv'), 'w'): pass
                with open(os.path.join(path, f'file_{i}_thing2.txt'), 'w'): pass
            else:
                with open(os.path.join(path, f'file_{i}'), 'w'): pass
        return path
