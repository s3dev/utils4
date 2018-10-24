# -*- coding: utf-8 -*-
"""
:Purpose:   This module serves as a general validation processor.

            Note: This is a **very basic** module at the minute.  More
            functionality will be added as needed.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
    Example code use::

        from utils import validation

        r = validation.Rules()
        r.is_string('this is my string')
        >>> True

"""

import os
import re

# pylint: disable=too-few-public-methods
class _FileExtensionRule(object):
    """Validate file extensions."""

    def file_ext_match(self, filename, ext) -> bool:
        """Verify a filename has the expected extension.

        The matching rules are **case insensitive**.

        Args:
            filename (str): The filename to test.
            ext (str): The expected extension; either with or without
                the dot.

        Returns:
            True if the extension matched, otherwise False.

        """
        _filename, _ext = os.path.splitext(filename)
        _ext = self._prepare_ext(ext=_ext)
        ext = self._prepare_ext(ext=ext)
        result = True if _ext == ext else False
        return result

    @staticmethod
    def _prepare_ext(ext) -> str:
        """Convert the extension to lowercase and remove any dots."""
        return ext.replace('.', '').lower()


class _IsStringRule(object):
    """String validation rules."""

    @staticmethod
    def is_string(value) -> bool:
        """Validate if ``value`` is a string.

        Returns:
            True if ``value`` is a ``str``, otherwise False.

        """
        return isinstance(value, str)


class RegEx(object):
    """This class holds a variety of validation regex strings."""

    def __init__(self):
        """Class initialiser."""
        self._yymmdd = self._set_yymmdd()

    @property
    def yymmdd(self):
        """The regex string for yymmdd."""
        return self._yymmdd

    @staticmethod
    def _set_yymmdd() -> str:
        """Return the regex for yymmdd.

        Note:
            This pattern only validates 2015, onwards.

        """
        return '((1[56789]|2[0-9]))(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])'


class Rules(object):
    """A collection of validation rules."""

    def __init__(self):
        """Class initialiser."""
        self._regex = RegEx()
        self._f_ext = _FileExtensionRule()
        self._is_str = _IsStringRule()

    def is_string(self, value) -> bool:
        """Test if ``value`` is a string.

        Args:
            value (str): The value to be tested.

        Returns:
            True if ``value`` is a ``str``, otherwise False.

        """
        result = self._is_str.is_string(value=value)
        return result

    def file_ext_match(self, filename, ext) -> bool:
        """Test if a filename has the expected extension.

        The matching rules are **case insensitive**.

        Args:
            filename (str): The filename to test.
            ext (str): The expected extension; either with or without
                the dot.

        Returns:
            True if the extension is as expected, otherwise False.

        """
        result = self._f_ext.file_ext_match(filename=filename, ext=ext)
        return result

    def yymmdd(self, value) -> bool:
        """Test if ``value`` matches the 'yymmdd' date pattern.

        Args:
            value (str): The value to be tested.

        Returns:
            True if ``value`` matches the pattern, otherwise False.

        """
        result = bool(re.match(self._regex.yymmdd, value))
        return result
