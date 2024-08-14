#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains basic and bright (16 colours) text and
            background ANSI colour codes for colouring Linux and Windows
            terminal output.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  If used on Windows, the ``colorama.init()`` method is
            called by the ``utils4.__init__`` module to configure Windows
            to handle CLI colouring.

:Example:

    Print red text to the terminal::

        >>> from utils4.termcolour import Text

        >>> print(f'{Text.RED}ALERT! This is red text.{Text.RESET}')
        ALERT! This is red text.


    Print red text on a white background to the terminal::

        >>> from utils4.termcolour import Back, Text

        >>> print(f'{Text.RED}{Back.BRIGHTWHITE}ALERT! This is red text on white.{Text.RESET}')
        ALERT! This is red text on white.


    Print bold yellow text on a black background to the terminal::

        >>> from utils4.termcolour import Back, Text, Style

        >>> print(f'{Text.YELLOW}{Back.BLACK}{Style.BOLD}Bold yellow text.{Text.RESET}')
        Bold yellow text.

"""
# pylint: disable=too-few-public-methods


class _AnsiBase:
    """Generic base ANSI colours class.

    The colours for each class are dynamically created as class attributes
    by the initialiser of this base class.

    """

    RESET = 0

    def __init__(self):
        """ANSI generic base class initialiser."""
        for i in self.__dir__():
            if not i.startswith('_'):
                self.__setattr__(i, f'\033[{self.__getattribute__(i)}m')


class AnsiBack(_AnsiBase):
    """ANSI background colour codes.

    Note:
        The bright colours have been included, but are not always supported.

    """

    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    BRIGHTBLACK = 100
    BRIGHTRED = 101
    BRIGHTGREEN = 102
    BRIGHTYELLOW = 103
    BRIGHTBLUE = 104
    BRIGHTMAGENTA = 105
    BRIGHTCYAN = 106
    BRIGHTWHITE = 107

class AnsiStyle(_AnsiBase):
    """ANSI style codes."""

    BOLD = 1
    DIM = 2
    UNDERLINE = 4
    NORMAL = 22


class AnsiText(_AnsiBase):
    """ANSI foreground (text) colour codes.

    Note:
        The bright colours have been included, but are not always supported.

    """

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHTBLACK = 90
    BRIGHTRED = 91
    BRIGHTGREEN = 92
    BRIGHTYELLOW = 93
    BRIGHTBLUE = 94
    BRIGHTMAGENTA = 95
    BRIGHTCYAN = 96
    BRIGHTWHITE = 97


Text = AnsiText()
Back = AnsiBack()
Style = AnsiStyle()
