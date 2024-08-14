#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a light wrapper around the ``base64``
            and ``hashlib`` libraries to provide some additional
            functionality.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:
    Example code use::

        >>> from utils4.crypto import crypto


    To obtain a quick MD5 hash::

        >>> s = "The quick brown fox jumps over the lazy dog"
        >>> output = crypto.md5(s)
        >>> print(output)

        9e107d9d372bb6826bd81d3542a419d6


    To obtain a Base64 encoded MD5 hash::

        >>> s = "The quick brown fox jumps over the lazy dog"
        >>> output = crypto.b64md5(s)
        >>> print(output)

        OWUxMDdkOWQzNzJiYjY4MjZiZDgxZDM1NDJhNDE5ZDY=


    For examples on checksumming a file, please refer to:

        - :meth:`Crypto.checksum_crc32`
        - :meth:`Crypto.checksum_md5`
        - :meth:`Crypto.checksum_sha1`
        - :meth:`Crypto.checksum_sha256`
        - :meth:`Crypto.checksum_sha512`

"""
# pylint: disable=invalid-name

import base64
import hashlib
import zlib
from typing import Union
from utils4 import convert


class Crypto:
    """Main class used for hashing and encoding.

    This class acts as a simple wrapper around the ``base64`` and
    ``hashlib`` libraries, providing additional functionality.

    """

    def b64(self, data: str, decode: bool=True) -> Union[bytes, str]:
        """Create an encoded or decoded Base64 encryption.

        Args:
            data (str): String to be encoded. If a ``str`` data type is
                received, it is encoded to ``bytes`` before encoding.
            decode (bool, optional): Return a decoded string. Defaults to True.

        Returns:
            Union[bytes, str]: An encoded or decoded Base64 encrypted string.

        """
        data = self._encode(data)
        b = base64.b64encode(data)
        if decode:
            b = b.decode()
        return b

    def b64md5(self, data: Union[iter, str], trunc: int=None) -> str:
        """Create an optionally truncated Base64 encoded MD5 hash from a
        string or array.

        Args:
            data (Union[iter, str]): A string or an iterable object containing
                strings to be encoded.
            trunc (int, optional): Truncate the Base64 string to (n)
                characters. As string slicing is used, values such as ``-1``
                are also valid. Defaults to None.

        Returns:
            str: An (optionally truncated) Base64 encoded MD5 hash of the
            passed string or iterable.

        """
        s = ''.join(data).encode()
        h = self.md5(s, decode=False)
        b = self.b64(h, decode=True)
        b = b[:trunc] if trunc else b
        return b

    @staticmethod
    def checksum_crc32(path: str, return_integer: bool=False) -> Union[int, str]:
        """Generate a 32-bit CRC32 checksum for the given file.

        Args:
            path (str): Full path to the file.
            return_integer (bool, optional): Return the original unsigned
                32-bit integer, rather than the hex string. Defaults to False.

        Important:
            This algorithm is *not* cryptographically strong and should not be
            used for authentication or digital signatures; nor is it suitable
            for use as a general hash algorithm.

            -- zlib.crc32 `Documentation`_

            .. _Documentation: https://docs.python.org/3/library/zlib.html#zlib.crc32

        :Design:
            This method breaks the file into 32768-byte chunks for more memory
            efficient reading. Meaning this method has a maximum memory use
            overhead of ~32K.

        :Example:

            Example for calculating the crc32 checksum for a file, returning a
            hex string::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_crc32(path='/tmp/test.txt')
                '2a30e66b'


            Example for calculating the crc32 checksum for a file, returning
            an integer::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_crc32(path='/tmp/test.txt', return_integer=True)
                707847787

        Returns:
            Union[int, str]: If the ``return_integer`` value is ``False``
            (default action), a CRC32 32-bit hex string (checksum string) of
            the file's contents is returned. Otherwise, an unsigned 32-bit
            integer is returned.

        """
        size = 1024*32 # 32K chunks
        with open(path, 'rb') as f:
            crcval = 0
            chunk = f.read(size)
            while len(chunk) > 0:
                crcval = zlib.crc32(chunk, crcval)
                chunk = f.read(size)
        if return_integer:
            rtn = crcval
        else:
            rtn = convert.int2hex(crcval & 0xFFFFFFFF)
        return rtn

    @staticmethod
    def checksum_md5(path: str) -> str:
        """Generate a 128-bit MD5 checksum for the given file.

        Args:
            path (str): Full path to the file.

        :Design:
            This method breaks the file into 32768-byte chunks
            (64-bytes * 512 blocks) for more memory efficient reading;
            taking advantage of the fact that MD5 uses 512-bit (64-byte) digest
            blocks. Meaning this method has a maximum memory use overhead of
            ~32K.

        :Example:

            Example calculating the MD5 checksum for a file::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_md5(path='/tmp/test.txt')
                '9ec06901e8f25eb9810c5e0db88e7dcd'

        Returns:
            str: A 128-bit MD5 hex digest (checksum string) of the file's
            contents.

        """
        md5 = hashlib.md5()
        size = 64*512  # 32K chunks - 64-byte digest blocks (x512 blocks)
        with open(path, 'rb') as f:
            chunk = f.read(size)
            while len(chunk) > 0:
                md5.update(chunk)
                chunk = f.read(size)
        return md5.hexdigest()

    @staticmethod
    def checksum_sha1(path: str) -> str:
        """Generate a 160-bit SHA1 checksum for the given file.

        Args:
            path (str): Full path to the file.

        :Design:
            This method breaks the file into 32768-byte chunks
            (64-bytes * 512 blocks) for more memory efficient reading;
            taking advantage of the fact that SHA1 uses 512-bit (64-byte)
            digest blocks. Meaning this method has a maximum memory use
            overhead of ~32K.

        :Example:

            Example calculating the SHA1 checksum for a file::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_sha1(path='/tmp/test.txt')
                'e49a1493c637a24800119fb53ef7dbc580221e89'

        Returns:
            str: A 160-bit SHA1 hex digest (checksum string) of the file's
            contents.

        """
        sha1 = hashlib.sha1()
        size = 64*512  # 32K chunks - 64-byte digest blocks (x512 blocks)
        with open(path, 'rb') as f:
            chunk = f.read(size)
            while len(chunk) > 0:
                sha1.update(chunk)
                chunk = f.read(size)
        return sha1.hexdigest()

    @staticmethod
    def checksum_sha256(path: str) -> str:
        """Generate a 256-bit SHA256 checksum for the given file.

        Args:
            path (str): Full path to the file.

        :Design:
            This method breaks the file into 32768-byte chunks
            (64-bytes * 512 blocks) for more memory efficient reading;
            taking advantage of the fact that SHA256 uses 512-bit (64-byte)
            digest blocks. Meaning this method has a maximum memory use
            overhead of ~32K.

        :Example:

            Example calculating the SHA256 checksum for a file::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_sha256(path='/tmp/test.txt')
                'e899df8e51b60bf8a6ede73fe5c7b4267bf5e48937e848bac3c6efd906833821'

        Returns:
            str: A 256-bit SHA256 hex digest (checksum string) of the file's
            contents.

        """
        sha256 = hashlib.sha256()
        size = 64*512  # 32K chunks - 64-byte digest blocks (x512 blocks)
        with open(path, 'rb') as f:
            chunk = f.read(size)
            while len(chunk) > 0:
                sha256.update(chunk)
                chunk = f.read(size)
        return sha256.hexdigest()

    @staticmethod
    def checksum_sha512(path: str) -> str:
        """Generate a 512-bit SHA512 checksum for the given file.

        Args:
            path (str): Full path to the file.

        :Design:
            This method breaks the file into 32768-byte chunks
            (128-bytes * 256 blocks) for more memory efficient reading;
            taking advantage of the fact that SHA512 uses 1024-bit (128-byte)
            digest blocks. Meaning this method has a maximum memory use
            overhead of ~32K.

        :Example:

            Example calculating the SHA512 checksum for a file::

                >>> from utils4.crypto import crypto

                >>> crypto.checksum_sha512(path='/tmp/test.txt')
                ('247adcb6f5b284b3e45c9281171ba7a6'
                 '2502692ee9ee8020bd5827602972409f'
                 '9bdfc2ec7e5452223c19b3745d3f04e2'
                 '542ef0d0e075139d1ee3b5f678c9aaec')  # Single string

        Returns:
            str: A 512-bit SHA512 hex digest (checksum string) of the file's
            contents.

        """
        sha512 = hashlib.sha512()
        size = 128*256  # 32K chunks - 128-byte digest blocks (x256 blocks)
        with open(path, 'rb') as f:
            chunk = f.read(size)
            while len(chunk) > 0:
                sha512.update(chunk)
                chunk = f.read(size)
        return sha512.hexdigest()

    def md5(self, data: str, decode: bool=True) -> str:
        """Create an optionally encoded or decoded MD5 hash.

        Args:
            data (str): String to be hashed. If a ``str`` data type
                is passed, it is encoded to ``bytes`` before hashing.
            decode (bool, optional): Return a decoded string. Defaults to True.

        Returns:
            str: An encoded or decoded MD5 hash, depending on the value passed
            to the ``decode`` parameter.

        """
        data = self._encode(data)
        h = hashlib.md5(data).hexdigest()
        if not decode:
            h = h.encode()
        return h

    @staticmethod
    def _encode(data: Union[bytes, str]) -> bytes:
        """Test if a string is ``str`` or ``bytes`` before processing.

        Args:
            data (Union[bytes, str]): String value to be encoded.

        If the received ``data`` parameter is a ``str`` type, it is converted
        to a ``bytes`` type and returned. If the string is already a ``bytes``
        type, it is returned, unmodified.

        Raises:
            ValueError: If the ``data`` object is neither a ``str`` or
                ``bytes`` type.

        Returns:
            bytes: A ``bytes`` encoded string.

        """
        if not isinstance(data, (bytes, str)):
            raise ValueError('Expected a bytes or str type.')
        data = data.encode() if isinstance(data, str) else data
        return data


crypto = Crypto()
