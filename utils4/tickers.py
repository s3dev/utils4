#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a wait tickers for long-running
            processes in your program.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  The idea for this code was taken from:

                - https://stackoverflow.com/a/39504463/6340496

:Example:   For usage examples, refer to the following class docstrings:

               - :class:`~Spinner`
               - :class:`~WaitTicker`

# pylint: disable=super-with-arguments  # For Py35 compatibility.
"""

import sys
import threading
import time
import colorama
from utils4 import utils


class _GenericWait():
    """This generic class holds functionality which is inherited by
    each ticker type.

    Args:
        charset (str): Character set to be used for the ticker.
        delay (float): Time delay between each ticker increment.

    """

    def __init__(self, charset: str, delay: float):
        """Class initialiser."""
        self.busy = False
        self._is_windows()
        self._charset = charset
        self._delay = self._set_delay(delay=delay)
        self._gen = self._generator()
        self._esc_clearline = '\r\033[K'

    def stop(self, err: bool=False):
        """Stop the ticker.

        Args:
            err (bool, optional): If the ticker's processing is stopped under
                error, passing ``True`` will clear the output line rather than
                printing ``Done.`` to the console. Defaults to False.

        """
        self.busy = False
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
        # pylint: disable=use-yield-from  # Kept for backwards compatibliity.
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
        sys.stdout.write(f'\033[1;32m{text}:\033[0m  ')

    @staticmethod
    def _set_delay(delay: float) -> float:
        """Set the delay between each spinner tick.

        Args:
            delay (float): Time delay between each tick increment.

        Returns:
            float: If the passed delay time is not ``None`` and is > 0, return
            the passed delay time.  Otherwise, return the default delay
            time.

        """
        default = 0.15
        # Test delay is not None and is > 0.
        delay = delay if delay and delay > 0 else default
        return delay


class Spinner(_GenericWait):
    """This class provides a wait spinner for long-running processes.

    Args:
        delay (float, optional): The time delay between each spinner tick.
            Defaults to None.

    :Example:

        Implement a spinner into your program::

            >>> from time import sleep  # For demo only.
            >>> from utils4.tickers import Spinner

            >>> spinner = Spinner()
            >>> spinner.start()
            >>> # Some long running process:
            >>> for _ in range(50):
            >>>     sleep(0.05)
            >>> spinner.stop()


        The output looks like::

            Processing: < spinning >
            Done.

    """

    def __init__(self, delay=None):
        """Class initialiser."""
        self._charset = '|/-\\'
        super().__init__(charset=self._charset, delay=delay)

    def start(self):
        """Start the spinner in a new thread."""
        self.busy = True
        self._print_start()
        threading.Thread(target=self._spinner).start()

    def _spinner(self):
        """Run the spinner."""
        while self.busy:
            sys.stdout.write(next(self._gen))
            sys.stdout.flush()
            time.sleep(self._delay)
            sys.stdout.write('\b')
            sys.stdout.flush()


class WaitTicker(_GenericWait):
    """This class features a wait ticker for long-running processes
    within your program.

    Args:
        charset (str, optional): The character(s) to be used as the ticker.
            Defaults to ``.``.
        delay (float, optional): The time delay between each tick.
            Defaults to 0.05.
        nticks (int, optional): The length of the ticker, in characters.
            Defaults to 25.

    :Example:

        Implement a ticker into your program::

            >>> from time import sleep  # For demo only.
            >>> from utils4.tickers import WaitTicker

            >>> ticker = WaitTicker(charset='-->', delay=0.05, nticks=25)
            >>> ticker.start()
            >>> # Some long running process:
            >>> for _ in range(75):
            >>>     sleep(0.05)
            >>> ticker.stop()

        The output looks like::

            Processing: -->-->-->--> # Expanding and contracting
            Done.

    """

    def __init__(self, charset: str='.', delay: float=0.05, nticks: int=25):
        """Class initialiser."""
        self._nticks = nticks
        super().__init__(charset=charset, delay=delay)

    def start(self):
        """Start the ticker in a new thread."""
        self.busy = True
        self._print_start()
        threading.Thread(target=self._ticker).start()

    def _ticker(self):
        """Run the ticker."""
        i = 1
        while self.busy:
            if i <= self._nticks:
                # Add ticks.
                sys.stdout.write(next(self._gen))
                sys.stdout.flush()
                time.sleep(self._delay)
                i += 1
            else:
                # Remove ticks.
                while i > 1 and self.busy:
                    sys.stdout.write('\b\033[K')
                    sys.stdout.flush()
                    time.sleep(self._delay)
                    i -=1
