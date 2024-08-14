#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``palette`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name

import os
import pickle
import random
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4 import palette


class TestPalette(TestBase):
    """Testing class used to test the ``palette`` module."""

    _N = 100  # Number of colour names to be tested.
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases.

        :Tasks:
            - Print the startup message.
            - Run the test setup initialiser.

        """
        msgs.startoftest.startoftest(module_name='palette')
        cls._test_setup_init()

    def test01__hex(self):
        """Test the hex colours.

        :Test:
            - Verify (n) randomly selected (at the time of test) hex values
              match the matplotlib source data.

        """
        for name in self._test_names:
            with self.subTest(msg=f'name={name}'):
                test = getattr(palette.hexpalette, name)
                exp = self._hex.get(name)
                utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test02__rgb(self):
        """Test the RGB colours.

        :Test:
            - Verify (n) randomly selected (at the time of test) RGB values
              match the matplotlib source data.

        """
        for name in self._test_names:
            with self.subTest(msg=f'name={name}'):
                test = getattr(palette.rgbpalette, name)
                exp = self._rgb.get(name)
                utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    @classmethod
    def _read_expected_colours(cls):
        """Read the serialised RGB and hex files containing expected values.

        The data contained in the serialised file comes from the ``CSS_COLORS``
        property of the ``matplotlib.colors`` module.

        """
        with open(os.path.join(cls._DIR_RESRC, 'test_palette__hex.p'), 'rb') as f:
            cls._hex = pickle.load(f)
        with open(os.path.join(cls._DIR_RESRC, 'test_palette__rgb.p'), 'rb') as f:
            cls._rgb = pickle.load(f)

    @classmethod
    def _test_setup_init(cls):
        """Initialise the class in preparation for the tests.

        :Tasks:
            - Read the expected RGB an hex values from the serialised
              reference files.
            - Store the (n) colour names to be tested into a class attribute.

        """
        cls._read_expected_colours()
        cls._test_names = random.sample(population=list(cls._hex.keys()), k=cls._N)
