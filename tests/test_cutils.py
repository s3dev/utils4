#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``cutils`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""

import ctypes
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4 import cutils


class TestCUtils(TestBase):
    """Testing class used to test the ``cutils`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='cutils')

    def test01__memset_str(self):
        """Test the ``memset`` function for a given string.

        :Test:
            - A string to be overwritten is defined.
            - The string is overwritten with 0 values using the
              ``cutils.memset`` function call.
            - A test is performed on the memory location to ensure all memory
              addresses occupied by the string are now 0, or ``\x00``.

        """
        inp = "String to be overwritten.\nLine 2.\nLine3."
        fill = 0
        ovh = str().__sizeof__() - 1
        loc = id(inp) + ovh
        size = inp.__sizeof__() - ovh
        success = cutils.memset(obj=inp, fill=fill)
        mem_cont_test = ctypes.string_at(loc, size)
        mem_cont_exp = b'\x00'*size
        utilities.assert_true_pyiter(expected=(True, True),
                                     test=(success, mem_cont_exp == mem_cont_test),
                                     msg=self._MSG1)

    def test01__memset_int(self):
        """Test the ``memset`` function for a given integer value.

        :Test:
            - An integer value to be overwritten is defined.
            - The value is overwritten with 0 values using the
              ``cutils.memset`` function call.
            - A test is performed on the memory location to ensure all memory
              addresses occupied by the string are now 0, or ``\x00``.

        """
        inp = (1 << 64) - 1
        fill = 0
        ovh = int().__sizeof__() - 1
        loc = id(inp) + ovh
        size = inp.__sizeof__() - ovh
        success = cutils.memset(obj=inp, fill=fill)
        mem_cont_test = ctypes.string_at(loc, size)
        mem_cont_exp = b'\x00'*size
        utilities.assert_true_pyiter(expected=(True, True),
                                     test=(success, mem_cont_exp == mem_cont_test),
                                     msg=self._MSG1)
