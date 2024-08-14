#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
:Purpose:   This module provides easy-access wrappers for C-based
            utilities.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

    Example for wiping a password from memory::

        >>> from utils4 import cutils

        >>> pwd = 'B0bsP@$$word&'
        >>> _ = cutils.memset(pwd, 0)
        >>> pwd
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

"""

import ctypes
import gc
from utils4.reporterror import reporterror


def memset(obj: object, fill: int=0) -> bool:
    """Fill the memory address block occupied by ``obj`` with ``repl``.

    Args:
        obj (object): Object to be overwritten, usually a string, can be an
            int. *Not* to be used with complex objects, such as lists, dicts,
            etc.
        fill (int, optional): Value to be filled. Defaults to 0.

    Per the ``ctypes.memset`` documentation:

      "Same as the standard C memset library function: fills the memory
      block at address dst with count bytes of value c. dst must be an
      integer specifying an address, or a ctypes instance."

    This function is a soft wrapper around the ``ctypes.memset`` function and
    provides a boolean return value, enabling the caller to test the success
    of the operation.

    Additionally, the reference to the ``obj`` object is manually deleted and
    a garbage collection call is made.

    Returns:
        bool: True if the operation succeeds, otherwise False. An operation
        is deemed successful if the return value from ``ctypes.memset`` is
        equal to the original memory address of ``obj``.

    """
    try:
        ovh = type(obj)().__sizeof__() - 1
        loc = id(obj) + ovh
        size = obj.__sizeof__() - ovh
        id_ = ctypes.memset(loc, fill, size)
        del obj
        gc.collect()
    except Exception as err:
        reporterror(err)
    return loc == id_
