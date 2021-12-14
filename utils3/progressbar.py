# -*- coding: utf-8 -*-
"""
:Purpose:   This is a small class module which provides access to a
            simple console progress bar.

:Platform:  Linux/Windows | Python 3.5+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

"""

import sys


class ProgressBar():
    """Implement a console progress bar into a processing loop.

    :Design:
        This is a simple console progress bar which should be called
        **inside** a processing loop.

        On instantiation, you can pass in the bar colour, length and
        symbol parameters if you want to configure the appearance a
        little bit.

    Args:
        total_values (int): Total number of iterations.
        bar_len (int): Complete length of the progress bar, in chars.
        symbol (str): The symbol which is used to track progress.
        color (str): Colour of the progress bar; where only the first
            letter of the colour is required.

    :Colour Options:
        red, green, yellow, blue, magenta, cyan, white

    :Example:
        You might implement the progress bar in a loop like this::

            >>> import time
            >>> from utils3.progressbar import ProgressBar

            >>> pb = ProgressBar(total_values=25, bar_len=25, symbol='#',
                                 color='red')

            # Some process.
            >>> for i range(26):
            >>>    # < some processing >
            >>>    # Update progress bar.
            >>>    pb.update_progress(current=i)
            >>>    # Optional pause to see updates.
            >>>    time.sleep(.1)

    """

    def __init__(self, total_values=25, bar_len=25, symbol='.', color='w'):
        """Progress bar class initialiser."""
        self._total   = total_values
        self._bar_len = bar_len
        self._symbol  = symbol
        self._color   = color
        self._reset   = '\x1b[0m'
        self._clr = self._getcolor()

    def update_progress(self, current):
        """Incrementally update the progress bar.

        Args:
            current (int): Index value for the current iteration.
                This value is compared against the initialised
                ``total_values`` parameter to determine the current
                position in the overall progress.

        :Example:
            Refer to the :class:`~progressbar.ProgressBar` class
            docstring.

        """
        # Calculate percent complete.
        percent = float(current) / self._total
        # Determine number of 0 placeholders.
        vals = len(str(self._total))
        # Number of ticks.
        ticks = self._symbol * int(round(percent * self._bar_len))
        # Number of space placeholders.
        spaces = ' ' * (self._bar_len - len(ticks))
        # Write output.
        sys.stdout.write(self._clr + '\rProcessing %s of %s [ %s ] %.0f%% Complete' % \
                         (str(current).zfill(vals),
                          self._total,
                          ticks + spaces,
                          percent*100) + self._reset)
        # Flush buffer.
        sys.stdout.flush()

    def _getcolor(self) -> str:
        """Create ANSI colour escape sequence to user's colour.

        Returns:
            str: ANSI escape sequence string for the user's colour.

        """
        # ANSI colour constants.
        red     = '31'
        green   = '32'
        yellow  = '33'
        blue    = '34'
        magenta = '35'
        cyan    = '36'
        white   = '37'
        color = ''
        if self._color.lower().startswith('r'): color = '\x1b[%s;40m' % (red)
        if self._color.lower().startswith('g'): color = '\x1b[%s;40m' % (green)
        if self._color.lower().startswith('y'): color = '\x1b[%s;40m' % (yellow)
        if self._color.lower().startswith('b'): color = '\x1b[%s;40m' % (blue)
        if self._color.lower().startswith('m'): color = '\x1b[%s;40m' % (magenta)
        if self._color.lower().startswith('c'): color = '\x1b[%s;40m' % (cyan)
        if self._color.lower().startswith('w'): color = '\x1b[%s;40m' % (white)
        return color
