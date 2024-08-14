#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``convert`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=too-many-public-methods
# pylint: disable=wrong-import-order

from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4 import convert


class TestConvert(TestBase):
    """Testing class used to test the ``convert`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Print the test's startup message."""
        msgs.startoftest.startoftest(module_name='convert')

    def test01__ascii2bin(self):
        """Test the ``ascii2bin`` method.

        :Test:
            - Verify method's output can be converted (by another means) to
              the input value.

        """
        inp = 'HelloZik!'
        out = convert.ascii2bin(asciistring=inp)
        binlist = [out[i:i+8] for i in range(0, len(out), 8)]
        test = ''.join(map(chr, map(lambda x: int(x, 2), binlist)))
        utilities.assert_true(expected=inp, test=test, msg=self._MSG1)

    def test01__ascii2hex(self):
        """Test the ``ascii2hex`` method.

        :Test:
            - Verify method's output can be converted (by another means) to
              the input value.

        """
        inp = 'HelloZik!'
        out = convert.ascii2hex(asciistring=inp)
        hexlist = [out[i:i+2] for i in range(0, len(out), 2)]
        test = ''.join(map(chr, map(lambda x: int(x, 16), hexlist)))
        utilities.assert_true(expected=inp, test=test, msg=self._MSG1)

    def test01__ascii2int(self):
        """Test the ``ascii2int`` method.

        :Test:
            - Verify method's output can be converted (by another means) to
              the input value.

        """
        inp = 'HelloZik!'
        out = convert.ascii2int(asciistring=inp)
        test = ''.join(map(chr, out))
        utilities.assert_true(expected=inp, test=test, msg=self._MSG1)

    def test02__bin2ascii_bits8(self):
        """Test the ``bin2ascii`` method using ``bits=8``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 8
        inp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        exp = 'HelloZik!'
        test = convert.bin2ascii(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2ascii_bits7(self):
        """Test the ``bin2ascii`` method using ``bits=7``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 7
        inp = '100100011001011101100110110011011111011010110100111010110100001'
        exp = 'HelloZik!'
        test = convert.bin2ascii(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2ascii_bits6(self):
        """Test the ``bin2ascii`` method using ``bits=6``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 6
        inp =  '110000110001110010110011110100110101110110110111111000111001'
        exp = '0123456789'
        test = convert.bin2ascii(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2int_bits8(self):
        """Test the ``bin2int`` method using ``bits=8``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 8
        inp = '0000000100000010000000110000010000000101'
        exp = [1, 2, 3, 4, 5]
        test = convert.bin2int(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2int_bits6(self):
        """Test the ``bin2int`` method using ``bits=6``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 6
        inp = '000001000010000011000100000101'
        exp = [1, 2, 3, 4, 5]
        test = convert.bin2int(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2int_bits3(self):
        """Test the ``bin2int`` method using ``bits=3``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 3
        inp = '001010011100101'
        exp = [1, 2, 3, 4, 5]
        test = convert.bin2int(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2hex_bits8(self):
        """Test the ``bin2hex`` method using ``bits=8``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 8
        inp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        exp = '48656c6c6f5a696b21'
        test = convert.bin2hex(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test02__bin2hex_bits7(self):
        """Test the ``bin2hex`` method using ``bits=7``.

        :Test:
            - Verify method's output matches the expected output.

        """
        bits = 7
        inp = '100100011001011101100110110011011111011010110100111010110100001'
        exp = '48656c6c6f5a696b21'
        test = convert.bin2hex(binstring=inp, bits=bits)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__hex2ascii(self):
        """Test the ``hex2ascii`` method.

        :Test:
            - Verify method's output matches the expected output.

        """
        inp = '48656c6c6f5a696b21'
        exp = 'HelloZik!'
        test = convert.hex2ascii(hexstring=inp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__hex2bin(self):
        """Test the ``hex2bin`` method.

        :Test:
            - Verify method's output matches the expected output.

        """
        inp = '48656c6c6f5a696b21'
        exp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        test = convert.hex2bin(hexstring=inp)
        utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test03__hex2int_nbytes1(self):
        """Test the ``hex2int`` method using ``nbytes=1``.

        :Test:
            - Verify method's output matches the expected output.

        """
        nbytes = 1
        inp = 'c0ffee'
        exp = [192, 255, 238]
        test = convert.hex2int(hexstring=inp, nbytes=nbytes)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test03__hex2int_nbytes2(self):
        """Test the ``hex2int`` method using ``nbytes=2``.

        :Test:
            - Verify method's output matches the expected output.

        """
        nbytes = 2
        inp = 'c0ffee'
        exp = [49407, 238]
        test = convert.hex2int(hexstring=inp, nbytes=nbytes)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test03__hex2int_nbytes3(self):
        """Test the ``hex2int`` method using ``nbytes=3``.

        :Test:
            - Verify method's output matches the expected output.

        """
        nbytes = 3
        inp = 'c0ffee'
        exp = [12648430]
        test = convert.hex2int(hexstring=inp, nbytes=nbytes)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test04__int2ascii(self):
        """Test the ``int2ascii`` method.

        :Test:
            - Verify method's output matches the expected output.

        """
        inp = [72, 101, 108, 108, 111, 90, 105, 107, 33]
        exp = 'HelloZik!'
        test = ''.join(convert.int2ascii(i=i) for i in inp)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test04__int2bin(self):
        """Test the ``int2bin`` method.

        :Test:
            - Verify method's output matches the expected output.

        """
        inp = [0, 1, 13, 37, 73, 196, 255]
        exp = '00000000000000010000110100100101010010011100010011111111'
        test = ''.join(convert.int2bin(i=i) for i in inp)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test04__int2hex(self):
        """Test the ``int2hex`` method.

        :Test:
            - Verify method's output matches the expected output.

        """
        inp = [0, 1, 13, 37, 73, 196, 255]
        exp = '0010d2549c4ff'
        test = ''.join(convert.int2hex(i=i) for i in inp)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test05__bin2ascii__valueerror(self):
        """Test the ``bin2ascii`` method for a ValueError.

        :Test:
            - Verify the method raises a ValueError for a binary string which
              cannot be broken into the requested chunks evenly.

        """
        bits = 7  # Raises an error as the input string is 8bit chunks.
        inp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        with self.assertRaises(ValueError):
            self._test05__bin2ascii__valueerror(binstring=inp, bits=bits)

    def test05__bin2int__valueerror(self):
        """Test the ``bin2int`` method for a ValueError.

        :Test:
            - Verify the method raises a ValueError for a binary string which
              cannot be broken into the requested chunks evenly.

        """
        bits = 7  # Raises an error as the input string is 8bit chunks.
        inp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        with self.assertRaises(ValueError):
            self._test05__bin2int__valueerror(binstring=inp, bits=bits)

    def test05__bin2hex__valueerror(self):
        """Test the ``bin2hex`` method for a ValueError.

        :Test:
            - Verify the method raises a ValueError for a binary string which
              cannot be broken into the requested chunks evenly.

        """
        bits = 7  # Raises an error as the input string is 8bit chunks.
        inp = '010010000110010101101100011011000110111101011010011010010110101100100001'
        with self.assertRaises(ValueError):
            self._test05__bin2hex__valueerror(binstring=inp, bits=bits)

    def test05__int2ascii__valueerror(self):
        """Test the ``int2ascii`` method for a ValueError.

        :Test:
            - Verify the method throws a ValueError for ints > 127.

        """
        inp = [128, 200, 500]
        for i in inp:
            with self.subTest(msg=f'i={i}'):
                with self.assertRaises(ValueError):
                    self._test05__int2ascii__valueerror(i=i)

    def test05__int2bin__valueerror(self):
        """Test the ``int2bin`` method for a ValueError.

        :Test:
            - Verify the method throws a ValueError for ints > 255.

        """
        inp = [256, 500, 1000]
        for i in inp:
            with self.subTest(msg=f'i={i}'):
                with self.assertRaises(ValueError):
                    self._test05__int2bin__valueerror(i=i)

    @staticmethod
    def _test05__int2ascii__valueerror(i: int):
        """Test the ``int2ascii`` method for a ValueError.

        :Trigger:
            - Throw a ValueError for int values > 127.

        """
        convert.int2ascii(i=i)

    @staticmethod
    def _test05__int2bin__valueerror(i: int):
        """Test the ``int2bin`` method for a ValueError.

        :Trigger:
            - Throw a ValueError for int values > 255.

        """
        convert.int2bin(i=i)

    @staticmethod
    def _test05__bin2ascii__valueerror(binstring: str, bits: int):
        """Test the ``bin2ascii`` method for a ValueError.

        :Trigger:
            - Throw a ValueError if the binary string cannot be broken into
              n-bit chunks evenly.

        """
        convert.bin2ascii(binstring=binstring, bits=bits)

    @staticmethod
    def _test05__bin2hex__valueerror(binstring: str, bits: int):
        """Test the ``bin2hex`` method for a ValueError.

        :Trigger:
            - Throw a ValueError if the binary string cannot be broken into
              n-bit chunks evenly.

        """
        convert.bin2hex(binstring=binstring, bits=bits)

    @staticmethod
    def _test05__bin2int__valueerror(binstring: str, bits: int):
        """Test the ``bin2int`` method for a ValueError.

        :Trigger:
            - Throw a ValueError if the binary string cannot be broken into
              n-bit chunks evenly.

        """
        convert.bin2int(binstring=binstring, bits=bits)
