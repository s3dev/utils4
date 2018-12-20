#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a wait ticker for long-running
            processes in your program.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  The idea for this code was taken from:

                * https://stackoverflow.com/a/39504463/6340496

:Example:
    To implement the spinner into your program::

        import time
        from utils3.tickers import Spinner

        spinner = Spinner()
        spinner.start()
        # SOME LONG RUNNING PROCESS
        # < ... >
        spinner.stop()

"""

import sys
import threading
import time
import colorama
from utils3 import utils

# pylint: disable=too-few-public-methods
class _GenericWait(object):
    """This generic class holds functionality which is inherited by 
    each ticker type.
    
    """

    def __init__(self, charset, delay):
        """Class initialiser."""
        self._is_windows()
        self._busy = False
        self._charset = charset
        self._delay = self._set_delay(delay=delay)
        self._gen = self._generator()
        self._esc_clearline = '\r\033[K'

    def stop(self, err=False):
        """Stop the ticker.
        
        Args:
            err (bool): If the ticker's processing is stopped under 
                error, passing ``True`` will clear the output line
                rather than printing ``Done.`` to the console.

        """
        self._busy = False
        if not err:
            self._print_end()
        else:
            self._clearline()

    def _clearline(self):
        """Clear the current line of the console."""
        sys.stdout.write(self._esc_clearline)
        sys.stdout.flush()

    def _generator(self):
        """Generate the character set."""
        while True:
            for i in self._charset:
                yield i

    @staticmethod
    def _is_windows():
        """If Win, run colorama init so colours display properly."""
        if 'win' in utils.get_os():
            colorama.init()

    def _print_end(self):
        """Write this to the console when the ticker is stopped."""
        sys.stdout.write(self._esc_clearline)
        sys.stdout.write('Done.')
        sys.stdout.flush()
        time.sleep(self._delay)
        sys.stdout.write('\n')
        sys.stdout.flush()

    @staticmethod
    def _print_start():
        """Write this to the console when the ticker is started."""
        text = 'Processing'
        # TODO: Offer text colour options in a future update.
        sys.stdout.write('\033[1;32m%s:\033[0m  ' % (text))

    @staticmethod
    def _set_delay(delay) -> float:
        """Set the delay between each spinner tick.

        Returns:
            If the passed delay time is not ``None`` and is > 0, return
            the passed delay time.  Otherwise, return the default delay
            time.

        """
        default = 0.15
        # TEST DELAY IS NOT None AND IS > 0
        delay = delay if delay and delay > 0 else default
        return delay


class Spinner(_GenericWait):
    """This class features a wait spinner for long-running processes
    within your program.

    Args:
        delay (float): The time delay between each spinner tick.

    :Example:
        To implement the spinner into your program::

            import time
            from utils3.tickers import Spinner

            spinner = Spinner()
            spinner.start()
            # SOME LONG RUNNING PROCESS
            # < ... >
            spinner.stop()

    """

    def __init__(self, delay=None):
        """Class initialiser."""
        self._charset = '|/-\\'
        super(Spinner, self).__init__(charset=self._charset, delay=delay)

    def start(self):
        """Start the spinner in a new thread."""
        self._busy = True
        self._print_start()
        threading.Thread(target=self._spinner).start()

    def _spinner(self):
        """Run the spinner."""
        while self._busy:
            sys.stdout.write(next(self._gen))
            sys.stdout.flush()
            time.sleep(self._delay)
            sys.stdout.write('\b')
            sys.stdout.flush()


class WaitTicker(_GenericWait):
    """This class features a wait ticker for long-running processes
    within your program.

    Args:
        charset (str): The character to be used as the ticker.
        delay (float): The time delay between each spinner tick.
        nticks (int): The length of the ticker, in characters.

    :Example:
        To implement the ticker into your program::

            import time
            from utils3.tickers import WaitTicker

            ticker = WaitTicker(charset='#')
            ticker.start()
            # SOME LONG RUNNING PROCESS
            # < ... >
            ticker.stop()

    """

    def __init__(self, charset='.', delay=0.05, nticks=25):
        """Class initialiser."""
        self._nticks = nticks
        super(WaitTicker, self).__init__(charset=charset, delay=delay)

    def start(self):
        """Start the ticker in a new thread."""
        self._busy = True
        self._print_start()
        threading.Thread(target=self._ticker).start()

    def _ticker(self):
        """Run the ticker."""
        i = 1
        while self._busy:
            if i <= self._nticks:
                # ADD TICKS
                sys.stdout.write(next(self._gen))
                sys.stdout.flush()
                time.sleep(self._delay)
                i += 1
            else:
                # REMOVE TICKS
                while i > 1 and self._busy:
                    sys.stdout.write('\b\033[K')
                    sys.stdout.flush()
                    time.sleep(self._delay)
                    i -=1
