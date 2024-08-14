#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``cmaps`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import contextlib
import io
import numpy as np
import os
import pickle
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4 import cmaps


class TestCMaps(TestBase):
    """Testing class used to test the ``cmaps`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Print the test's startup message."""
        msgs.startoftest.startoftest(module_name='cmaps')

    def test01__get_cmap_rgba(self):
        """Test the ``get_cmap`` method for RGBA color values.

        :Test:
            - Verify the 'Blues' colour map of 15 RGBA colours is
              created as expected.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_cmaps__test1.npy')
        cmaps_ = cmaps.CMaps()
        tst = cmaps_.get_cmap('Blues', n=15, as_hex=False, preview=False)
        exp = np.load(fname)
        utilities.assert_true_array(expected=exp, test=tst, msg=self._MSG1)

    def test02__get_cmap_hex(self):
        """Test the ``get_cmap`` method for hex colour values.

        :Test:
            - Verify the 'Blues' colour map of 15 hex colours is
              created as expected.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_cmaps__test2.p')
        cmaps_ = cmaps.CMaps()
        tst = cmaps_.get_cmap('Blues', n=15, as_hex=True, preview=False)
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        utilities.assert_true_pyiter(expected=exp, test=tst, msg=self._MSG1)

    def test03__get_named_colours(self):
        """Test the ``get_named_colours`` method.

        :Test:
            - Verify the returned named colours are as expected.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_cmaps__test3.p')
        cmaps_ = cmaps.CMaps()
        tst = cmaps_.get_named_colours()
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        utilities.assert_true_pyiter(expected=exp, test=tst, msg=self._MSG1)

    def test04__view_cmaps__view_only_false(self):
        """Test the ``view_cmaps`` method, using ``view_only = False``.

        :Test:
            - Verify the returned named colour maps are as expected.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_cmaps__test4.p')
        cmaps_ = cmaps.CMaps()
        tst = cmaps_.view_cmaps(view_only=False)
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        utilities.assert_true_pyiter(expected=sorted(exp), test=sorted(tst), msg=self._MSG1)

    def test04__view_cmaps__view_only_true(self):
        """Test the ``view_cmaps`` method, using ``view_only = True``.

        :Test:
            - Verify the printed named colour maps are as expected.

        """
        buff = io.StringIO()
        cmaps_ = cmaps.CMaps()
        exp = cmaps_.view_cmaps(view_only=False)
        with contextlib.redirect_stdout(buff):
            cmaps_.view_cmaps(view_only=True)
        utilities.assert_true(expected=str(exp), test=buff.getvalue().strip(), msg=self._MSG1)

    def test05__get_cmap__invalid_n(self):
        """Test the ``get_cmap`` method, with an ``n`` value > 255.

        :Test:
            - Verify a ValueError is raised for an ``n`` value > 255.

        """
        for n in [-1, 0, 256, 500]:
            with self.subTest(msg=f'n={n}'):
                with self.assertRaises(ValueError):
                    self._test05__get_cmap__invalid_n(n=n)

    def test06__get_cmap__0_255(self):
        """Test the ``get_cmap`` method, with an ``n`` value of 0-255.

        :Test:
            - ...

        """
        cmaps_ = cmaps.CMaps()
        for i in range(1, 256):
            with self.subTest(msg=f'i={i}'):
                cmaps_.get_cmap('Blues', n=i)

    @staticmethod
    def _test05__get_cmap__invalid_n(n: int):
        """Test the ``get_cmap`` mathod and trigger a ValueError.

        Args:
            n (int): Value of n to be tested.

        :Trigger:

            - An ``n`` value < 1 or > 255 must raise a ValueError.

        """
        cmaps_ = cmaps.CMaps()
        cmaps_.get_cmap(map_name='Blues', n=n)
