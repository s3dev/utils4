#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a light wrapper around the ``base64``
            and ``hashlib`` libraries to provide some additional
            functionality.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:
    Example code use::

        from utils3.crypto import crypto

        # Obtain a quick MD5 hash.
        s = "The quick brown fox jumps over the lazy dog"
        output = crypto.md5(s)
        print(output)
        >>> 9e107d9d372bb6826bd81d3542a419d6

        # Obtain a Base64 encoded MD5 hash.
        s = "The quick brown fox jumps over the lazy dog"
        output = crypto.b64md5(s)
        print(output)
        >>> OWUxMDdkOWQzNzJiYjY4MjZiZDgxZDM1NDJhNDE5ZDY=

"""
# pylint: disable=invalid-name

import base64
import hashlib


class Crypto():
    """Class used for hashing and encoding.

    This class acts as a simple wrapper around the ``base64`` and
    ``hashlib`` libraries, providing additional functionality.

    """

    @staticmethod
    def _encode(data) -> bytes:
        """Test if a string is ``str`` or ``bytes`` before processing.

        If the string is ``str``, it is converted to ``bytes`` and
        returned.

        Returns:
            A ``bytes`` encoded string.

        """
        data = data.encode() if isinstance(data, str) else data
        return data

    def b64(self, data, decode=True):
        """Create an encoded/decoded Base64 encryption.

        Args:
            data (str): String to be encoded.  If a ``str`` data type
                is passed, it is encoded to ``bytes`` before encoding.
            decode (bool): Return a decoded string.

        Returns:
            An encoded or decoded Base64 encrypted string.

        """
        data = self._encode(data)
        b = base64.b64encode(data)
        if decode:
            b = b.decode()
        return b

    def b64md5(self, data, trunc=None) -> str:
        """Create a truncated Base64 encoded MD5 hash from a string or
        array.

        Args:
            data (str, iterable): Object containing string(s) to be
                encoded.
            trunc (int): Truncate the Base64 string to (n) characters.
                As string slicing is used, values such as ``-1`` are
                also valid.

        Returns:
            An (optionally truncated) Base64 encoded MD5 hash of the
            passed string or iterable.

        """
        s = ''.join(data).encode()
        h = self.md5(s, decode=False)
        b = self.b64(h, decode=True)
        b = b[:trunc] if trunc else b
        return b

    def md5(self, data, decode=True):
        """Create an encoded/decoded MD5 hash.

        Args:
            data (str): String to be hashed.  If a ``str`` data type
                is passed, it is encoded to ``bytes`` before hashing.
            decode (bool): Return a decoded string.

        Returns:
            An encoded or decoded MD5 hash.

        """
        data = self._encode(data)
        h = hashlib.md5(data).hexdigest()
        if not decode:
            h = h.encode()
        return h


crypto = Crypto()
