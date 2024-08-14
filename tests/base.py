#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the superclass which is to be inherited
            by the test-specific modules.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Example:
    Example code use.

    Run all tests via the shell script::

        $ ./run.sh

    Run all tests using unittest::

        $ python -m unittest discover

    Run a single test::

        $ python -m unittest test_name.py

"""
# pylint: disable=wrong-import-position

import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest


class TestBase(unittest.TestCase):
    """Private generalised base-testing class.

    This class is designed to be inherited by each test-specific class.

    There is no special functionality provided by this class at this time.

    """

    if 'linux' in sys.platform.lower():
        _DIR_DSK = os.path.join(os.environ.get('HOME'), 'Desktop')
        _DIR_TMP = '/tmp'
    elif 'win' in sys.platform.lower():
        _DIR_DSK = os.path.join(os.environ.get('USERPROFILE'), 'Desktop')
        _DIR_TMP = 'c:/temp'
    else: _DIR_TMP = None

    _DIR_RESRC = os.path.realpath('./resources')

    @staticmethod
    def disable_terminal_output():
        """Turn off all output to the terminal."""
        sys.stdout = io.StringIO()

    @staticmethod
    def enable_terminal_output():
        """Turn on output to the terminal."""
        sys.stdout = sys.__stdout__
