#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``validation`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

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
# The imports for utils4 must be after TestBase.
from utils4 import validation


class TestValidation(TestBase):
    """Testing class used to test the ``validation`` module."""

    _COORD = [['0', '0'],
              ['0', '-180'],
              ['0', '180'],
              ['-90', '0'],
              ['90', '0'],
              ['90', '180'],
              ['90', '-180'],
              ['-90', '-180'],
              ['-90', '180'],
              ['-54.933333', '-67.616667'],
              ['64.75111', '-147.34944'],
              ['4.6097100', '-74.0817500'],
              ['51.50853', '-0.12574'],
              ['-6.214862', '106.84513']]
    _COORD_X = [['0', '-180.01'],
                ['0', '180.1'],
                ['-90.001', '0'],
                ['90.01', '0'],
                ['90.1', '180'],
                ['91', '-180'],
                ['-90', '-180.1'],
                ['-90', '181'],
                ['-94.933333', '-67.616667'],
                ['64.75111', '-187.34944'],
                ['104.6097100', '-74.0817500'],
                ['51.50853', '-181.12574'],
                ['-960.214862', '1006.84513']]
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='validation')

    def test01__is_coordinates__invalid(self):
        """Test the ``is_coordinates`` method for invalid sets of coordinates.

        :Test:
            - Iterate through coordinate sets and test each set is valid.

        This test also tests the following methods, as these are all called by
        the ``is_coordinates`` method:

            - ``RegEx.latitude``
            - ``RegEx.longitude``
            - ``Rules.is_latitude``
            - ``Rules.is_longitude``

        """
        for c in self._COORD_X:
            with self.subTest(msg=f'c={c}'):
                test = validation.rules.is_coordinates(value=c)
                utilities.assert_true(expected=False, test=test, msg=self._MSG1)

    def test01__is_coordinates__valid(self):
        """Test the ``is_coordinates`` method for valid sets of coordinates.

        :Test:
            - Iterate through coordinate sets and test each set is valid.

        This test also tests the following methods, as these are all called by
        the ``is_coordinates`` method:

            - ``RegEx.latitude``
            - ``RegEx.longitude``
            - ``Rules.is_latitude``
            - ``Rules.is_longitude``

        """
        for c in self._COORD:
            with self.subTest(msg=f'c={c}'):
                test = validation.rules.is_coordinates(value=c)
                utilities.assert_true(expected=True, test=test, msg=self._MSG1)

    def test02__is_list(self):
        """Test the ``is_list`` method.

        :Test:
            - Loop through a set of so-called 'lists' and verify each pass the
              validation on two counts:

                  - Must be a list
                  - Must contain the specified number of elements

        """
        exp = (True, True, True, True, False, False, False, False)
        lists = [([1, 2, 3], None), (['a'], 1), (['a', 1], 2), (['a', 1, 1.0], 3),
                 (('tuple1', 'tuple2'), None), ('string', None), (1, None), (1.0, None)]
        for e, (obj, obj_i) in zip(exp, lists):
            with self.subTest(msg=f'obj={obj}, obj_i={obj_i}'):
                test = validation.rules.is_list(value=obj, indexes=obj_i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test03__is_ip__ipv4(self):
        """Test the ``is_ip`` method, for IPv4 addresses.

        :Test:
            - Iterate through a list of IP addresses and verify the method
              validates each address as expected.

        """
        exp = [True] * 7 + [False] * 7
        ips = ['0.0.0.0', '127.0.0.1', '127.0.0.255', '192.168.0.1',    # Good (7)
               '8.8.8.8', '128.31.0.62', '104.16.181.15',
               '0.0.0.256', '256.225.255.255', '127.0.0.256', '0.0.0',   # Bad (7)
               '123.123', 'alpha', 'string.string']
        for e, ip in zip(exp, ips):
            with self.subTest(msg=f'ip={ip}, e={e}'):
                test = validation.rules.is_ip(value=ip)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test03__is_ip__ipv6(self):
        """Test the ``is_ip`` method, for IPv6 addresses.

        :Test:
            - Iterate through a list of IP addresses and verify the method
              validates each address as expected.

        Note:
            All good IPv6 addresses have been taken from Wikipedia. The
            invalid addresses are simply invalid variations of the good
            addresses.

        """
        exp = [True] * 3 + [False] * 3
        ips = ['2001:0db8:85a3:0000:0000:8a2e:0370:7334',   # Good (3)
               '2001:db8:1234:ffff:ffff:ffff:ffff:ffff',
               'fe80::1ff:fe23:4567:890a',
               'fg::0db8:85a3:0000:0000:8a2e:0370:7334',    # fg is invalid and has 9 groups
               '2003:0db8:85a3:0000:0000:8a2e:0370:73fz',   # 73fz is invalid
               ':64:ff9b:1::0.0.0.0']                       # :64 is invalid
        for e, ip in zip(exp, ips):
            with self.subTest(msg=f'ip={ip}, e={e}'):
                test = validation.rules.is_ip(value=ip)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)
