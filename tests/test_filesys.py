#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``filesys`` module.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order
"""

try:
    import os
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    import os
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4 import filesys


class TestFileSys(TestBase):
    """Testing class used to test the ``fileyss`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='filesys')

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
