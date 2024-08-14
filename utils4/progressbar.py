# -*- coding: utf-8 -*-
"""
:Purpose:   This is a small class module which provides access to a
            simple console progress bar.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:   For a simple usage example, refer to the :class:`~ProgressBar`
            class docstring.

"""

import sys


class ProgressBar:
    """Implement a console progress bar into a processing loop.

    Args:
        total_values (int, optional): Total number of iterations.
            Defaults to 25.
        bar_len (int, optional): Complete length of the progress bar, in chars.
            Defaults to 25
        symbol (str, optional): The symbol which is used to track progress.
            Defaults to ``'.'``.
        color (str, optional): Colour of the progress bar; where only the first
            letter of the colour is required.
            Options are: red, green, yellow, blue, magenta, cyan, white.
            Defaults to 'w' (white).

    :Design:
        This is a simple console progress bar which should be called
        **inside** a processing loop.

        On instantiation, you can pass in the bar colour, length and
        symbol parameters if you want to configure the appearance a
        little bit.

    :Colour Options:
        red, green, yellow, blue, magenta, cyan, white

    :Example:
        You might implement the progress bar in a loop like this::

            >>> import time
            >>> from utils4.progressbar import ProgressBar

            >>> pb = ProgressBar(total_values=25,
                                 bar_len=25,
                                 symbol='#',
                                 color='red')

            >>> for i range(26):
            >>>    # < some processing >
            >>>    pb.update_progress(current=i)
            >>>    # Optional pause to see updates.
            >>>    time.sleep(.1)

            Processing 25 of 25 [ ......................... ] 100% Complete

    """

    def __init__(self, total_values: int=25, bar_len: int=25, symbol: str='.', color: str='w'):
        """Progress bar class initialiser."""
        self._total = total_values
        self._bar_len = bar_len
        self._symbol = symbol
        self._color = color
        self._len = len(str(self._total))
        self._rst = '\x1b[0m'
        self._clr = self._getcolor()

    def update_progress(self, current: int):  # pragma: nocover
        """Incrementally update the progress bar.

        Args:
            current (int): Index value for the current iteration.
                This value is compared against the initialised ``total_values``
                parameter to determine the current position in the overall
                progress.

        :Example:

            Refer to the :class:`~ProgressBar` class docstring.

        """
        # Calculate percent complete.
        percent = float(current) / self._total
        # Number of ticks.
        ticks = self._symbol * int(round(percent * self._bar_len))
        # Number of space placeholders.
        spaces = ' ' * (self._bar_len - len(ticks))
        msg = (f'{self._clr}'
               f'\rProcessing {str(current).zfill(self._len)} of {self._total} [ {ticks+spaces} ] '
               f'{percent*100:.0f}% Complete{self._rst}')
        sys.stdout.write(msg)
        sys.stdout.flush()

    def _getcolor(self) -> str:
        """Create ANSI colour escape sequence to user's colour.

        Returns:
            str: ANSI escape sequence string for the user's colour.

        """
        clrs = {'r': 31, 'g': 32, 'y': 33, 'b': 34, 'm': 35, 'c': 36, 'w': 37}
        seq = f'\033[{clrs.get(self._color[0])};40m'
        return seq
