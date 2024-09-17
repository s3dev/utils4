#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains various low-level conversion functions.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  Often, these types of conversions are called from a high-iteration
            loop. Therefore, the implementation of these functions has been
            written as close to core Python as possible, or in a C style, for
            efficiency purposes.

"""

# TODO: Move repeated messages into a central messaging class.

def ascii2bin(asciistring: str) -> str:
    """Convert an ASCII string into a binary string representation.

    Args:
        asciistring (str): ASCII string to be converted.

    Returns:
        str: A binary string representation for the passed ASCII text, where
        each ASCII character is represented by an 8-bit binary string.

    """
    return ''.join(map(int2bin, ascii2int(asciistring)))

def ascii2hex(asciistring: str) -> str:
    """Convert an ASCII string into a hexidecimal string.

    Args:
        asciistring (str): ASCII string to be converted.

    Returns:
        str: A hexidecimal string representation of the passed ASCII
        text.

    """
    return ''.join(map(int2hex, ascii2int(asciistring)))

def ascii2int(asciistring: str) -> list:
    """Convert an ASCII string to a list of integers.

    Args:
        asciistring (str): ASCII string to be converted.

    Returns:
        list: A list of integers, as converted from he ASCII string.

    """
    return [ord(i) for i in asciistring]

def bin2ascii(binstring: str, bits: int=8) -> str:
    """Convert a binary string representation into ASCII text.

    Args:
        binstring (str): Binary string to be converted.
        bits (int, optional): Bit chunks into which the binary string is
            broken for conversion. Defaults to 8.

    Returns:
        str: An ASCII string representation of the passed binary string.

    """
    if len(binstring) % bits:
        raise ValueError('The string length cannot be broken into '
                         f'{bits}-bit chunks.')
    ints = []
    for chunk in range(0, len(binstring), bits):
        byte_ = binstring[chunk:chunk+bits]
        ints.append(bin2int(byte_, bits=bits)[0])
    text = ''.join(map(int2ascii, ints))
    return text

def bin2int(binstring: str, bits: int=8) -> int:
    """Convert a binary string representation into an integer.

    Args:
        binstring (str): Binary string to be converted.
        bits (int, optional): Bit chunks into which the binary string is
            broken for conversion. Defaults to 8.

    Returns:
        int: Integer value from the binary string.

    """
    if len(binstring) % bits:
        raise ValueError('The string length cannot be broken into '
                         f'{bits}-bit chunks.')
    ints = []
    for chunk in range(0, len(binstring), bits):
        int_ = 0
        s = 0
        byte = binstring[chunk:chunk+bits]
        for b in range(len(byte)-1, -1, -1):
            int_ += int(byte[b]) << s
            s += 1
        ints.append(int_)
    return ints

def bin2hex(binstring: str, bits: int=8) -> str:
    """Convert a binary string representation into a hex string.

    Args:
        binstring (str): Binary string to be converted.
        bits (int, optional): Bit chunks into which the binary string is
            broken for conversion. Defaults to 8.

    Returns:
        A hexidecimal string representation of the passed binary string.

    """
    if len(binstring) % bits:
        raise ValueError('The string length cannot be broken into '
                         f'{bits}-bit chunks.')
    return ''.join(int2hex(i) for i in bin2int(binstring, bits=bits))

def hex2ascii(hexstring: str) -> str:
    """Convert a hexidecimal string to ASCII text.

    Args:
        hexstring (str): Hex string to be converted.

    Returns:
        str: An ASCII string representation for the passed hex string.

    """
    return ''.join(map(int2ascii, hex2int(hexstring)))

def hex2bin(hexstring: str) -> str:
    """Convert a hexidecimal string into a binary string representation.

    Args:
        hexstring (str): Hex string to be converted.

    Returns:
        str: A binary string representation of the passed hex string.

    """
    return ''.join(map(int2bin, hex2int(hexstring)))

def hex2int(hexstring: str, nbytes: int=1) -> int:
    """Convert a hexidecimal string to an integer.

    Args:
        hexstring (str): Hex string to be converted.
        nbytes (int, optional): Number of bytes to consider for each
            decimal value. Defaults to 1.

    :Examples:
        Example usage::

            hex2int(hexstring='c0ffee', nbytes=1)
            >>> [192, 255, 238]

            hex2int(hexstring='c0ffee', nbytes=2)
            >>> [49407, 238]

            hex2int(hexstring='c0ffee', nbytes=3)
            >>> [12648430]

    Returns:
        list: A list of decimal values, as converted from the hex string.

    """
    # pylint: disable=multiple-statements
    nbytes *= 2
    out = []
    # Split hex string into (n)-byte size chunks.
    for chunk in range(0, len(hexstring), nbytes):
        i = 0
        nib = 0
        for char in hexstring[chunk:nbytes+chunk]:
            if (char >= '0') & (char <= '9'): nib = ord(char)
            if (char >= 'a') & (char <= 'f'): nib = ord(char) + 9
            if (char >= 'A') & (char <= 'F'): nib = ord(char) + 9
            i = (i << 4) | (nib & 0xf)
        out.append(i)
    return out

def int2ascii(i: int) -> str:
    """Convert an integer to an ASCII character.

    Args:
        i (int): Integer value to be converted to ASCII text.

    Note:
        The passed integer value must be <= 127.

    Raises:
        ValueError: If the passed integer is > 127.

    Returns:
        str: The ASCII character associated to the passed integer.

    """
    if i > 127:
        raise ValueError('The passed integer value must be <= 127.')
    return chr(i)

def int2bin(i: int) -> str:
    """Convert an 8-bit integer to a binary string.

    Args:
        i (int): Integer value to be converted.

    Note:
        The passed integer value must be <= 255.

    Raises:
        ValueError: If the passed integer is > 255.

    Returns:
        str: A binary string representation of the passed integer.

    """
    if i > 255: # Limited to 1 byte.
        raise ValueError(f'Passed value exceeds 1 byte: i={i}')
    return ''.join(str((i >> shift) & 1) for shift in range(7, -1, -1))

def int2hex(i: int) -> str:
    """Convert an integer into a hexidecimal string.

    Args:
        i (int): Integer value to be converted.

    Returns:
        str: A two character hexidecimal string for the passed integer
        value.

    """
    chars = '0123456789abcdef'
    out = ''
    out_ = ''
    while i > 0:
        out_ += chars[i % 16]
        i //= 16
    # Output string must be reversed.
    for x in range(len(out_)-1, -1, -1):
        out += out_[x]
    # Pad so all hex values are two characters.
    if len(out) < 2:
        out = '0' + out
    return out
