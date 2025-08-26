#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``futils`` module.

:Note:
            This test module tests the **installed** ``utils4.futils``
            module, as this is a C implementation and therefore cannot be
            tested directly. Preferably, there should be an
            *dev release* of utils4 which can be installed locally where
            this module can be tested.

:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  Because this test module fiddles with (**destroys**)
            ``sys.path`` and ``sys.modules``, it's best to ensure this
            test runs **last**. Hence the ``_x_`` in the test module
            name.

"""
# pylint: disable=global-statement
# pylint: disable=import-error
# pylint: disable=import-outside-toplevel

import os
import sys
from glob import glob
from pip._internal.utils.appdirs import user_cache_dir
# locals
from base import TestBase
from testlibs import msgs
# from testlibs.utilities import utilities
utils = None  # Global placeholder for import


class TestFutils(TestBase):
    """Testing class used to test the ``futils`` module."""

    _MSG1 = msgs.templates.not_as_expected.general
    _DIR_DATA = os.path.join(TestBase._DIR_RESRC, __name__)

    @classmethod
    def setUpClass(cls):
        """Tasks to be run at the testing startup.

        :Tasks:
            - Print the start of test message.
            - Hack ``sys.modules`` and ``sys.path`` to allow import from
              *installed* ``utils4`` for C library testing.

        """
        msgs.startoftest.startoftest(module_name='futils')
        # Clear utils4 from imports to allow re-import from installed.
        keys = [k for k in sys.modules if 'utils4' in k]
        for k in keys:
            del sys.modules[k]
        # Force import from *installed* library.
        sys.path = [i for i in map(str.lower, sys.path) if 'python' in i or 'site-packages' in i]
        from utils4 import utils as utils_
        # Export the import to global namespace.
        global utils
        utils = utils_

    def test01a__isascii__plaintext(self):
        """Test the ``isascii`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertTrue(utils.isascii(f))

    def test01b__isascii__binary(self):
        """Test the ``isascii`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.isascii(f))

    def test02a__isbinary__plaintext(self):
        """Test the ``isbinary`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.isbinary(f))

    def test02b__isbinary__binary(self):
        """Test the ``isbinary`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertTrue(utils.isbinary(f))

    def test03a__iszip__plaintext(self):
        """Test the ``iszip`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.iszip(f))

    def test03b__iszip__binary(self):
        """Test the ``iszip`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertFalse(utils.iszip(f))

    def test03c__iszip__zip(self):
        """Test the ``iszip`` method with Python wheels.

        :Test:
            - Collect Python wheels from pip's cache directory.
            - Verify each file is a ZIP archive file as expected.

        """
        files = glob(os.path.join(user_cache_dir('pip'), '**', '*.whl'), recursive=True)
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertTrue(utils.iszip(f))

    def test04a__ispdf__plaintext(self):
        """Test the ``ispdf`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.ispdf(f))

    def test04b__ispdf__binary(self):
        """Test the ``ispdf`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertFalse(utils.ispdf(f))

    def test04c__ispdf__pdf(self):
        """Test the ``ispdf`` method with true PDF files.

        :Test:
            - For each true PDF file in the resources directory, verify
              the function under test returns True.

        """
        files = glob(os.path.join(self._DIR_DATA, '*.pdf'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertTrue(utils.ispdf(f))

    def test05a__is7zip__plaintext(self):
        """Test the ``is7zip`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.is7zip(f))

    def test05b__is7zip__binary(self):
        """Test the ``is7zip`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertFalse(utils.is7zip(f))

    def test05c__is7zip__7zip(self):
        """Test the ``is7zip`` method with true 7-zip files.

        :Test:
            - For each true 7-zip file in the resources directory, verify
              the function under test returns True.

        """
        files = glob(os.path.join(self._DIR_DATA, '*.7z'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertTrue(utils.is7zip(f))

    def test06a__isgzip__plaintext(self):
        """Test the ``isgzip`` method with plain-text files.

        :Test:
            - Collect all Python modules from the ``utils4`` directory.
            - Verify each file (except utils.py) is a plain-text ASCII
              file.

        Note:
            The ``utils.py`` module is excluded as it contains Polish,
            Greek and Chinese characters in docstring for ``unidecode``.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '*.py'))
        for f in files:
            if 'utils.py' not in f:
                with self.subTest(msg=f'File: {f}'):
                    self.assertFalse(utils.isgzip(f))

    def test06b__isgzip__binary(self):
        """Test the ``isgzip`` method with binary files.

        :Test:
            - Collect known binary files from the ``utils4/__pycache__``
              directory.
            - Verify each file is a binary file as expected.

        """
        files = glob(os.path.join(self._DIR_ROOT, 'utils4', '__pycache__', '*.pyc'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertFalse(utils.isgzip(f))

    def test06c__isgzip__gzip(self):
        """Test the ``isgzip`` method with true GZIP compressed files.

        This test also includes ``.tar.gz`` archives.

        :Test:
            - For each true GZIP compressed file in the resources
              directory, verify the function under test returns True.

        """
        files = glob(os.path.join(self._DIR_DATA, '*.gz'))
        for f in files:
            with self.subTest(msg=f'File: {f}'):
                self.assertTrue(utils.isgzip(f))
