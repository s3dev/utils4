#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``crypto`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import base64
import hashlib
import os
import zlib
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
# The imports for utils4 must be after TestBase.
from utils4.crypto import crypto


class TestCrypto(TestBase):
    """Testing class used to test the ``crypto`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):

        """Print the test's startup message."""
        msgs.startoftest.startoftest(module_name='crypto')

    def test01__b64_encoded(self):
        """Test the ``b64`` method, without decoding.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = base64.b64encode(inp.encode())
        test = crypto.b64(data=inp, decode=False)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test01__b64_decoded(self):
        """Test the ``b64`` method, with decoding.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = base64.b64encode(inp.encode()).decode()
        test = crypto.b64(data=inp, decode=True)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test01__b64__valueerror(self):
        """Test the ``b64`` method, triggering a ValueError.

        :Test:
            - Verify the ``b64`` method throws a ValueError for unexpected
              input values - non-string / non-bytes.

        """
        inp = [0, 1, 1.0, object, ['abcd'], ('abcd', ), {'abcd': 1234}]
        for data in inp:
            with self.subTest(msg=f'data={data}'):
                with self.assertRaises(ValueError):
                    crypto.b64(data=data, decode=False)

    def test02__b64md5(self):
        """Test the ``b64md5`` method, without truncating.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = base64.b64encode(hashlib.md5(inp.encode()).hexdigest().encode()).decode()
        test = crypto.b64md5(data=inp, trunc=False)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__b64md5_trunc16(self):
        """Test the ``b64md5`` method, truncated to 16 characters.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = base64.b64encode(hashlib.md5(inp.encode()).hexdigest().encode()).decode()[:16]
        test = crypto.b64md5(data=inp, trunc=16)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__md5_encoded(self):
        """Test the ``md5`` method, without decoding.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = hashlib.md5(inp.encode()).hexdigest().encode()
        test = crypto.md5(data=inp, decode=False)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__md5_decoded(self):
        """Test the ``md5`` method, with decoding.

        :Test:
            - Test the method's output matches the output created by calling
              the built-in's functions manually.

        """
        inp = 'The red fox was running.'
        exp = hashlib.md5(inp.encode()).hexdigest()
        test = crypto.md5(data=inp, decode=True)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_crc32__int(self):
        """Test the ``checksum_crc32`` method, returning an integer.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``zlib.crc32`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = zlib.crc32(f.read())
        test = crypto.checksum_crc32(path=fp, return_integer=True)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_crc32__hex(self):
        """Test the ``checksum_crc32`` method, returning a hex string.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``zlib.crc32`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = f'{zlib.crc32(f.read()):0x}'  # Convert returned int to hex.
        test = crypto.checksum_crc32(path=fp, return_integer=False)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_md5(self):
        """Test the ``checksum_md5`` method.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``hashlib.md5`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = hashlib.md5(f.read()).hexdigest()
        test = crypto.checksum_md5(path=fp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_sha1(self):
        """Test the ``checksum_sha1`` method.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``hashlib.sha1`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = hashlib.sha1(f.read()).hexdigest()
        test = crypto.checksum_sha1(path=fp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_sha256(self):
        """Test the ``checksum_sha256`` method.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``hashlib.sha256`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = hashlib.sha256(f.read()).hexdigest()
        test = crypto.checksum_sha256(path=fp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test04__checksum_sha512(self):
        """Test the ``checksum_sha512`` method.

        :Test:
            - Use the method to checksum *this* file.
            - Use the ``hashlib.sha512`` method to checksum *this* file.
            - Verify the two checksum values are the same.

        """
        fp = os.path.realpath(__file__)
        with open(fp, 'rb') as f:
            exp = hashlib.sha512(f.read()).hexdigest()
        test = crypto.checksum_sha512(path=fp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)
