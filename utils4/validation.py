# -*- coding: utf-8 -*-
r"""
:Purpose:   This module serves as a general validation processor.

            .. note::
                This is currently **very basic** module, and only contains
                validation rules which are commonly used by S3DEV projects.
                More functionality will be added as needed.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:

    Test if an IP address is valid::

        >>> from utils4 import validation

        >>> validation.rules.is_ip(value='128.31.0.62')
        True


    Test if a set of geo coordinates is valid::

        >>> from utils4 import validation

        >>> validation.rules.is_coordinates(value=['4.6097100', '-74.0817500'])
        True


    Return the regex pattern for latitude::

        >>> from utils4 import validation

        >>> validation.regex.latitude
        re.compile(r'^(-)?(([0-9]|[1-8][0-9])(\.[0-9]{1,})?|90)$', re.UNICODE)

"""

import re
import ipaddress
from typing import List


class RegEx:
    """This class holds a variety of validation regex strings.

    Each property in this class returns a *compiled* regex pattern, of the
    type ``re.Pattern``.

    """

    @property
    def latitude(self):
        """Regex string for latitude.

        Returns:
            re.Pattern: A compiled regex pattern for latitude.

        """
        return re.compile(r'^(-)?(([0-9]|[1-8][0-9])(\.[0-9]{1,})?|90)$')

    @property
    def longitude(self):
        """Regex string for longitude.

        Returns:
            re.Pattern: A compiled regex pattern for longitude.

        """
        return r'^(-)?(([0-9]|[1-9][0-9]|1[0-7][0-9])(\.[0-9]{1,})?|180)$'


class Rules:
    """A collection of validation rules."""

    def __init__(self):
        """Class initialiser."""
        self._re = RegEx()

    def is_coordinates(self, value: List[str]) -> bool:
        """Test ``value`` is a valid set of geo coordinates.

        Args:
            value (List[str]): A list containing latitude and longitude as
                strings.

        :Rules:

            - ``value`` is a ``list``
            - The index 0 is a valid latitude coordinate (-90, 90)
            - The index 1 is a valid longitude coordinate (-180, 180)
            - For example::

                ['4.6097100', '-74.0817500']

        Returns:
            bool: True if ``value`` is a *valid* set of coordinates, otherwise
            False.

        """
        is_lat = False
        is_lon = False
        is_list = self.is_list(value, indexes=2)
        if is_list:
            is_lat = self.is_latitude(value=value[0])
            is_lon = self.is_longitude(value=value[1])
        return all([is_list, is_lat, is_lon])

    @staticmethod
    def is_ip(value: str) -> bool:
        """Test if an IP address (IPv4 or IPv6) is valid.

        This function wraps the built-in :func:`ipaddress.ip_address` function
        to test whether an IP address is valid, or not.

        Args:
            value (str): The IP address to be tested.

        Returns:
            bool: True if ``value`` is a valid IPv4 or IPv6 address, otherwise
            False.

        """
        try:
            ipaddress.ip_address(address=value)
            return True
        except ValueError:
            return False

    def is_latitude(self, value: str) -> bool:
        """Test ``value`` is a latitude coordinate (-90, 90).

        Args:
            value (str): The latitude coordinate to be tested.

        Returns:
            bool: True if ``value`` is a valid latitude coordinate, otherwise
            False.

        """
        return bool(re.match(self._re.latitude, value))

    @staticmethod
    def is_list(value: object, indexes: int=None) -> bool:
        """Validate if ``value`` is a ``list`` with (n) number of indexes.

        Args:
            value (list): The object to be tested.
            indexes (int, optional): Number of expected indexes in the list.
                Defaults to None.

        Returns:
            bool: True if ``value`` is a ``list`` with (n) indexes, otherwise
            False.

        """
        _idx = True
        _list = isinstance(value, list)
        if _list and indexes:
            _idx = len(value) == indexes
        return all([_list, _idx])

    def is_longitude(self, value: str) -> bool:
        """Test ``value`` is a longitude coordinate (-180, 180).

        Args:
            value (str): The longitude coordinate to be tested.

        Returns:
            bool: True if ``value`` is a valid longitude coordinate, otherwise
            False.

        """
        return bool(re.match(self._re.longitude, value))


regex = RegEx()
rules = Rules()
