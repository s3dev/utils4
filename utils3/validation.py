# -*- coding: utf-8 -*-
"""
:Purpose:   This module serves as a general validation processor.

            Note: This is a **basic** module at the minute.  More
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
# pylint: disable=too-few-public-methods

import os
import re


class _FileExtensionRule():
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
        result = _ext == ext
        return result

    @staticmethod
    def _prepare_ext(ext) -> str:
        """Convert the extension to lowercase and remove any dots."""
        return ext.replace('.', '').lower()


class _IsInstanceRules():
    """Validation rules for Python data types."""

    @staticmethod
    def is_list(value, indexes=None) -> bool:
        """Validate if ``value`` is a list with (n) number of indexes.

        The ``indexes`` argument is optional.

        Args:
            value (list): The object to be tested.
            indexes (int): Number of expected indexes in the list.

        Returns:
            True if ``value`` is a ``list`` with (n) indexes, otherwise
            False.

        """
        len_match = True
        is_list = isinstance(value, list)
        if is_list and indexes:
            len_match = len(value) == indexes
        result = all([is_list, len_match])
        return result

    @staticmethod
    def is_string(value) -> bool:
        """Validate if ``value`` is a string.

        Args:
            value (str): The object to be tested.

        Returns:
            True if ``value`` is a ``str``, otherwise False.

        """
        return isinstance(value, str)


class RegEx():
    """This class holds a variety of validation regex strings."""

    @property
    def ip_ipv4(self):
        """Regex string for an IPv4 IP address."""
        return self._set_ip_ipv4()

    @property
    def latitude(self):
        """Regex string for latitude."""
        return self._set_latitude()

    @property
    def longitude(self):
        """Regex string for longitude."""
        return self._set_longitude()

    @property
    def yymmdd(self):
        """Regex string for yymmdd."""
        return self._set_yymmdd()

    @staticmethod
    def _set_ip_ipv4() -> str:
        """Return the regex for an IPv4 IP address."""
        return (r'^((?:(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}'
                '(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))$')

    @staticmethod
    def _set_latitude() -> str:
        """Return the regex for latitude."""
        return r'^(-)?(([0-9]|[1-8][0-9])(\.[0-9]{1,})?|90)$'

    @staticmethod
    def _set_longitude() -> str:
        """Return the regex for longitude."""
        return r'^(-)?(([0-9]|[1-9][0-9]|1[0-7][0-9])(\.[0-9]{1,})?|180)$'

    @staticmethod
    def _set_yymmdd() -> str:
        """Return the regex for yymmdd.

        Note:
            This pattern only validates 2015, onwards.

        """
        return '((1[56789]|2[0-9]))(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])'


class Rules():
    """A collection of validation rules."""

    def __init__(self):
        """Class initialiser."""
        self._regex = RegEx()
        self._f_ext = _FileExtensionRule()
        self._is_inst = _IsInstanceRules()

    def is_coordinates(self, value) -> bool:
        """Test ``value`` is a valid set of geo coordinates.

        :Rules:

            * The value is a list
            * The index 0 is a valid latitude coordinate (-90, 90)
            * the index 1 is a valid longitude coordinate (-180, 180)

        Returns:
            True if ``value`` is a valid set of coordinates, otherwise
            False.

        """
        is_lat = False
        is_lon = False
        is_list = self._is_inst.is_list(value, indexes=2)
        if is_list:
            is_lat = self.is_latitude(value=value[0])
            is_lon = self.is_longitude(value=value[1])
        result = all([is_list, is_lat, is_lon])
        return result

    def is_ip(self, value) -> bool:
        """Test if ``value`` is a valid IPv4 IP address.

        This function matches four sets of numbers from 0-255,
        separated by a decimal; where **leading zeros are not allowed**.

        Args:
            value (str): The IP address to be tested.

        Returns:
            True if ``value`` is a valid IPv4 IP address, otherwise
            False.

        """
        result = bool(re.match(self._regex.ip_ipv4, value))
        return result

    def is_latitude(self, value) -> bool:
        """Test ``value`` is a latitude coordinate (-90, 90).

        Args:
            value (str): The coordinate to be tested.

        Returns:
            True if ``value`` is a valid latitude coordinate, otherwise
            False.

        """
        result = bool(re.match(self._regex.latitude, value))
        return result

    def is_list(self, value, indexes=None) -> bool:
        """Test if ``value`` is a list with (n) number of indexes.

        The ``indexes`` argument is optional.

        Args:
            value (list): The object to be tested.
            indexes (int): Number of expected indexes in the list.

        Returns:
            True if ``value`` is a ``list`` with (n) indexes, otherwise
            False.

        """
        result = self._is_inst.is_list(value=value, indexes=indexes)
        return result

    def is_longitude(self, value) -> bool:
        """Test ``value`` is a longitude coordinate (-180, 180).

        Args:
            value (str): The coordinate to be tested.

        Returns:
            True if ``value`` is a valid longitude coordinate, otherwise
            False.

        """
        result = bool(re.match(self._regex.longitude, value))
        return result

    def is_string(self, value) -> bool:
        """Test if ``value`` is a string.

        Args:
            value (str): The value to be tested.

        Returns:
            True if ``value`` is a ``str``, otherwise False.

        """
        result = self._is_inst.is_string(value=value)
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

        With the current implementation, this function only validates
        2015, onwards.

        Args:
            value (str): The value to be tested.

        Returns:
            True if ``value`` matches the pattern, otherwise False.

        """
        result = bool(re.match(self._regex.yymmdd, value))
        return result
