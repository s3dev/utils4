# -*- coding: utf-8 -*-
"""
:Purpose:   This is a small class module which provides access to a
            simple console progress bar.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

"""

import sys
import colorama

# TODO: Update to offer background colour.

# pylint:disable=too-few-public-methods
class ProgressBar(object):
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

            import time
            from utils3.progressbar import ProgressBar

            pb = ProgressBar(total_values=25, bar_len=25, symbol='#',
                             color='red')

            # SOME PROCESS
            for i range(26):
                # UPDATE PROGRESS
                pb.update_progress(current=i)
                # OPTIONAL PAUSE TO SEE UPDATES
                time.sleep(.1)

    """

    def __init__(self, total_values=25, bar_len=25, symbol='.', color='w'):
        """Class initialiser."""
        # MAKE COLORS WORK WITH WINDOWS
        colorama.init()
        # SET CLASS VARIABLES
        self._total   = total_values
        self._bar_len = bar_len
        self._symbol  = symbol
        self._color   = color
        self._reset   = '\x1b[0m'
        # GET USER'S COLOUR
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
        # CALCULATE PERCENT COMPLETE
        percent = float(current) / self._total
        # DETERMINE NUMBER OF 0 PLACEHOLDERS
        vals = len(str(self._total))
        # NUMBER OF TICKS
        ticks = self._symbol * int(round(percent * self._bar_len))
        # NUMBER OF SPACE PLACEHOLDERS
        spaces = ' ' * (self._bar_len - len(ticks))

        # PRINT OUTPUT
        sys.stdout.write(self._clr + '\rProcessing %s of %s [ %s ] %.0f%% Complete' % \
                         (str(current).zfill(vals),
                          self._total,
                          ticks + spaces,
                          percent*100) + self._reset)

        # FLUSH BUFFER
        sys.stdout.flush()


    def _getcolor(self) -> str:
        """Create ANSI colour escape sequence to user's colour.

        Returns:
            ANSI escape sequence string for the user's colour.

        """
        # ANSI COLOUR CONSTANTS
        red     = '31'
        green   = '32'
        yellow  = '33'
        blue    = '34'
        magenta = '35'
        cyan    = '36'
        white   = '37'
        # INITIALISE
        color = ''
        # RETURN USER COLOR AN ANSI STRING
        if self._color.lower().startswith('r'): color = '\x1b[%s;40m' % (red)
        if self._color.lower().startswith('g'): color = '\x1b[%s;40m' % (green)
        if self._color.lower().startswith('y'): color = '\x1b[%s;40m' % (yellow)
        if self._color.lower().startswith('b'): color = '\x1b[%s;40m' % (blue)
        if self._color.lower().startswith('m'): color = '\x1b[%s;40m' % (magenta)
        if self._color.lower().startswith('c'): color = '\x1b[%s;40m' % (cyan)
        if self._color.lower().startswith('w'): color = '\x1b[%s;40m' % (white)
        return color
