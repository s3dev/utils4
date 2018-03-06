"""------------------------------------------------------------------------------------------------
Program:    progressbar

Purpose:    This is a small class module which provides access to a simple console progress bar.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        Refer to USE section of the docstring.

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
06.03.18    J. Berendt      1.1.0       Minor docstring clarifications and updates.
                                        Revised the user color to ANSI lookup process.
                                        Updated to move the 'total number of items' from the
                                        inner update_progress function to the instantiation.
                                        NOTE: This **will break** current implementations.  A minor
                                        update will be required to your program.
------------------------------------------------------------------------------------------------"""

import sys
import colorama

# TODO: Update to offer background colour.

class ProgressBar(object):
    """
    DESIGN:
    This is a simple console progress bar which should be called
    inside a processing loop.

    You can pass in the bar colour, length and symbol parameters if
    you want to configure the appearance a little bit.

    PARAMETERS:
    - total_values (default=50)
    Integer value defining the total iterations.
    - bar_len (default=50)
    Integer value defining the length of the progress bar, in chars.
    - symbol (default='.')
    The symbol which is used to track progress.
    - color (default='white')
    Color of the progress bar; where only the first letter of to colour
    is required.
        COLOUR OPTIONS:
        - red, green, yellow, blue, magenta, cyan, white

    USE:
    > from utils3.progressbar import ProgressBar
    >
    > pb = ProgressBar(total_values=25, bar_len=25, symbol='#',
    >                  color='red')
    >
    > # SOME PROCESS
    > for i range(26):
    >     # UPDATE PROGRESS
    >     pb.update_progress(current=i)
    >     # SOME PAUSE TO SEE UPDATES
    >     time.sleep(.1)
    """

    # ------------------------------------------------------------------
    def __init__(self, total_values=25, bar_len=25, symbol='.', color='w'):
        """Create the progress bar object."""

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


    # ------------------------------------------------------------------
    def update_progress(self, current):
        """
        Incrementally update the progress bar.

        PARAMETERS
        - current
        Integer value for the current iteration.
        This value is compared against the initialised total_values
        parameter to determine the current position in the overall
        progress.

        USE:
        Refer to the class docstring: help(progressbar.ProgressBar)
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


    # ------------------------------------------------------------------
    def _getcolor(self):
        """
        Assign the ANSI colour string for the user's colour, using
        the colour constants.
        """

        # ANSI COLOUR CONSTANTS
        RED     = '31'
        GREEN   = '32'
        YELLOW  = '33'
        BLUE    = '34'
        MAGENTA = '35'
        CYAN    = '36'
        WHITE   = '37'
        # INITIALISE
        color = ''

        # RETURN USER COLOR AN ANSI STRING
        if self._color.lower().startswith('r'): color = '\x1b[%s;40m' % (RED)
        if self._color.lower().startswith('g'): color = '\x1b[%s;40m' % (GREEN)
        if self._color.lower().startswith('y'): color = '\x1b[%s;40m' % (YELLOW)
        if self._color.lower().startswith('b'): color = '\x1b[%s;40m' % (BLUE)
        if self._color.lower().startswith('m'): color = '\x1b[%s;40m' % (MAGENTA)
        if self._color.lower().startswith('c'): color = '\x1b[%s;40m' % (CYAN)
        if self._color.lower().startswith('w'): color = '\x1b[%s;40m' % (WHITE)

        return color
