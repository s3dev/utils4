#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``srccheck`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

# pylint: disable=import-error
# pylint: disable=wrong-import-order
"""
# pylint: disable=invalid-name

try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
import io
import os
from contextlib import redirect_stdout
from glob import glob
# The imports for utils4 must be after TestBase.
from utils4.srccheck import srccheck


class TestSourceCheck(TestBase):
    """Testing class used to test the ``module`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='srccheck')

    @classmethod
    def tearDownClass(cls):
        """Run this logic at the end of all test cases.

        :Tasks:
            - Remove all ``srccheck.*`` files from the user's desktop.

        """
        files = glob(os.path.join(cls._DIR_DSK, 'srccheck*'))
        for f in files:
            os.remove(f)

    def test01a__generate_plaintext(self):
        """Test the ``generate`` method for a plaintext reference file.

        :Test:
            - Collect the lorem* files from the resources directory.
            - Generate a plaintext reference file for these files.
            - Verify the terminal output is as expected.

        """
        files = sorted(glob(os.path.join(self._DIR_RESRC, 'lorem*')))
        buff = io.StringIO()
        with redirect_stdout(buff):
            srccheck.generate(files, encrypt=False)
        exp = '\nComplete.\nThe reference file is available on your desktop.\n'
        tst = buff.getvalue()
        buff.close()
        utilities.assert_true(expected=exp, test=tst, msg=self._MSG1)

    def test01b__reference_file_exists(self):
        """Verify ``test01a`` generated a reference file on the desktop.

        :Test:
            - Verify the ``srccheck.ref`` file exists on the user's desktop.

        """
        path = os.path.join(self._DIR_DSK, 'srccheck.ref')
        utilities.assert_true(expected=True, test=os.path.exists(path), msg=self._MSG1)

    def test01c__check_plaintext_pass(self):
        """Test the ``check`` method for a plaintext reference file.

        :Test:
            - Verify the check passes for the plaintext reference file.

        """
        tst = srccheck.check(os.path.join(self._DIR_DSK, 'srccheck.ref'))
        utilities.assert_true(expected=True, test=tst, msg=self._MSG1)

    def test01d__check_plaintext_fail(self):
        """Test the ``check`` method for a plaintext reference file.

        :Test:
            - Read the reference file and change the last character of the
              first hash string to enforce a failure. Write the change back to
              the reference file.
            - Run the ``check`` and capture the output.
            - Verify the test failed and the terminal output is as expected.

        """
        refpath = os.path.join(self._DIR_DSK, 'srccheck.ref')
        # Change the last character of the first hash string and write back to the file.
        with open(refpath, 'r+', encoding='utf-8') as f:
            line1 = next(f)
            f.write(f'{line1[:-2]}x\n')
        buff = io.StringIO()
        with redirect_stdout(buff):
            tst1 = srccheck.check(os.path.join(self._DIR_DSK, 'srccheck.ref'))
        exp = '\nChecksum verification has failed for the following:\n- lorem.txt\n\n'
        tst2 = buff.getvalue()
        utilities.assert_true(expected=[False, exp], test=[tst1, tst2], msg=self._MSG1)

    def test02a__generate_encrypted(self):
        """Test the ``generate`` method for an encrypted reference file.

        :Test:
            - Collect the lorem* files from the resources directory.
            - Generate an encrypted reference file for these files.
            - Verify the terminal output is as expected.

        """
        files = glob(os.path.join(self._DIR_RESRC, 'lorem*'))
        buff = io.StringIO()
        with redirect_stdout(buff):
            srccheck.generate(files, encrypt=True)
        exp = '\nComplete.\nThe reference and key files are available on your desktop.\n'
        tst = buff.getvalue()
        buff.close()
        utilities.assert_true(expected=exp, test=tst, msg=self._MSG1)

    def test02b__reference_file_exists(self):
        """Verify ``test02a`` generated reference and key files on the desktop.

        :Test:
            - Verify the ``srccheck.ref`` file exists on the user's desktop.
            - Verify the ``srccheck.key`` file exists on the user's desktop.

        """
        tests = []
        for f in ['srccheck.ref', 'srccheck.key']:
            tests.append(os.path.exists(os.path.join(self._DIR_DSK, f)))
        utilities.assert_true(expected=[True, True], test=tests, msg=self._MSG1)

    def test02c__check_encrypted_pass(self):
        """Test the ``check`` method for an encrypted reference file.

        :Test:
            - Verify the check passes for the encrypted reference file.

        """
        tst = srccheck.check(ref_file=os.path.join(self._DIR_DSK, 'srccheck.ref'),
                             key_file=os.path.join(self._DIR_DSK, 'srccheck.key'))
        utilities.assert_true(expected=True, test=tst, msg=self._MSG1)

    def test03__generate__file_not_exist(self):
        """Verify a FileNotFoundError is raised for a non-existant source file.

        :Test:
            - Verify a FileNotFoundError is raised for a source file which
              does not exist.

        """
        with redirect_stdout(None):
            with self.assertRaises(FileNotFoundError):
                srccheck.generate(['path/does/not/exist.txt'])

    def test03__check__ref_not_exist(self):
        """Verify a FileNotFoundError is raised for a non-existant reference file.

        :Test:
            - Verify a FileNotFoundError is raised for a reference file which
              does not exist.

        """
        with redirect_stdout(None):
            with self.assertRaises(FileNotFoundError):
                srccheck.check(ref_file='path/does/not/exist.ref')

    def test03__check__key_not_exist(self):
        """Verify a FileNotFoundError is raised for a non-existant key file.

        :Test:
            - Verify a FileNotFoundError is raised for a key file which
              does not exist.

        """
        with redirect_stdout(None):
            with self.assertRaises(FileNotFoundError):
                srccheck.check(ref_file=os.path.join(self._DIR_DSK, 'srccheck.ref'),
                               key_file='path/does/not/exist.ref')
