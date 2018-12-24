#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains basic (8 colour) text and background
            colouring for Linux and Windows terminal output.

            The eight additional 'bright' colours are accessed by
            passing ``True`` to the ``bright`` argument.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  If used on Windows, the ``colorama.init()`` method is
            called to configure Windows to handle CLI colouring.

:Example:
    Example code use::

        from utils3 import colours

        t = colours.Colours().text
        print(t.red+'Hello!'+t.reset)

"""

import colorama
from utils3 import utils

# pylint: disable=too-few-public-methods
class _Generic(object):
    """The generic worker class inherited by the specific classes."""

    def __init__(self, bright):
        """Class initialiser."""
        self._os = self._get_os()
        self._colorama_init()
        self._bright = self._set_bright(bright)
        self._template = '\033[{bright};{code}m'

    @property
    def black(self):
        """Black"""
        return self._template.format(bright=self._bright, code=self._BLK)

    @property
    def blue(self):
        """Blue"""
        return self._template.format(bright=self._bright, code=self._BLU)

    @property
    def cyan(self):
        """Cyan"""
        return self._template.format(bright=self._bright, code=self._CYN)

    @property
    def green(self):
        """Green"""
        return self._template.format(bright=self._bright, code=self._GRN)

    @property
    def magenta(self):
        """Magenta"""
        return self._template.format(bright=self._bright, code=self._MAG)

    @property
    def red(self):
        """Red"""
        return self._template.format(bright=self._bright, code=self._RED)

    @property
    def reset(self):
        """Reset colour output."""
        return '\033[0m'

    @property
    def white(self):
        """White"""
        return self._template.format(bright=self._bright, code=self._WHT)

    @property
    def yellow(self):
        """Yellow"""
        return self._template.format(bright=self._bright, code=self._YLW)

    def _colorama_init(self):
        """If Windows, run colorama init so colours display properly."""
        if 'win' in self._os:
            colorama.init()

    @staticmethod
    def _get_os():
        """Get the OS."""
        my_os = utils.get_os()
        return my_os

    @staticmethod
    def _set_bright(bright):
        """Set the escape sequence template.

        Args:
            bright (bool): The ``bright`` flag passed in by the caller.

        """
        return 1 if bright else 0


class _Back(_Generic):
    """This class contains background colours."""

    _BLK=40
    _RED=41
    _GRN=42
    _YLW=43
    _BLU=44
    _MAG=45
    _CYN=46
    _WHT=47

    def __init__(self, bright):
        """Class initialiser."""
        super(_Back, self).__init__(bright=bright)


class _Text(_Generic):
    """This class contains colours for text."""

    _BLK=30
    _RED=31
    _GRN=32
    _YLW=33
    _BLU=34
    _MAG=35
    _CYN=36
    _WHT=37

    def __init__(self, bright):
        """Class initialiser."""
        super(_Text, self).__init__(bright=bright)


class Colours(object):
    """The main colours class, which contains text and bkg colours.

    Args:
        bright (bool): Provides access to the eight 'bright' colours.

    :Comments:
        If used on Windows, the ``colorama.init()`` method is called
        to configure Windows to handle CLI colouring.

    :Example:
        Example code use::

            from workers import colours

            t = colours.Colours().text
            print(t.red+'Hello!'+t.reset)

    """

    def __init__(self, bright=True):
        """Class initialiser."""
        self._back = _Back(bright=bright)
        self._text = _Text(bright=bright)

    @property
    def back(self):
        """Background colours."""
        return self._back

    @property
    def text(self):
        """Text colours."""
        return self._text

