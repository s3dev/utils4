# -*- coding: utf-8 -*-
"""
:Purpose:   This class module provides an interface to the Windows/Linux
            command line interfaces (CLI), enabling the user to easily print
            text, headings and banners in a variety of pre-defined
            (and customisable) colour layouts, to the terminal.

            The callable printing methods in this module mean the user does not
            need to mess with ANSI escape sequences and other formatting
            overhead. Rather, just call the method and the overhead is taken
            care of.

            This module contains a :class:`~UserInterface` class whose methods
            provide a standard way of reporting normal, alternative and
            abnormal behaviour. The following formats are built-in:

                - **Fully customisable messages and headers** via the
                  :meth:`~UserInterface.print_` method.
                - **The ability to print headings**, such as:

                    - black text on a cyan background
                    - black text on a green background
                    - black text on a white background
                    - black text on a yellow background
                    - white text on a blue background
                    - etc ...

                - **User input expected**: as white text on a black background
                - **Normal behaviour**:  as green text on a black background
                - **Alternative behaviour**: (e.g. a warning) as yellow text
                  on a black background
                - **Abnormal or erroneous behaviour**: as red text on a black
                  background

:Platform:  Linux/Windows | Python 3.7+
:Developer: M Critchard, J Berendt
:Email:     support@s3dev.uk

:Example:   For usage examples, please refer to the following class docstrings:

                - :class:`~PrintBanner`
                - :class:`~UserInterface`

"""
# pylint: disable=line-too-long
# pylint: disable=too-few-public-methods
# pylint: disable=wrong-import-position


import inspect
import os
import platform
import sys
import time
import warnings
from utils4.reporterror import reporterror
from utils4.termcolour import Back, Text, Style

# Only import if windows.
if 'win' in platform.system().lower():
    # import win_unicode_console
    from ctypes import windll


class _Config:
    """Storage class for the module's config items."""

    v_pad_sleep = 1
    default_string = " {title:{pad}}:{spaces}{name}"
    custom_string = " {key:{pad}}:{spaces}{val}"


class PrintBanner:
    """This class is used to print an information banner to the terminal.

    Generally, this class is used in the startup routine of an application
    to display information about the application. For example, information such
    as the application title, version, security classification, etc.

    :Design:
        This may be useful if you want to use a 'standardised' program
        header across all of your programs.  This class can be called in the
        program's startup routine.

        The banner can also be used to display and report expected error
        information.  For example, if a certain validation type of
        error is expected, a customised version of this banner can wrap
        the error information such as error type, the issue, the file
        name/location, and the resolution.

    For further detail, refer to the **Design** and **Parameters**
    sections of the :meth:`~PrintBanner.__init__` method, as the banner
    is highly configurable.

    :Example Banner:
        Below is a printed example of a program header banner::

            ------------------------------------------------------------
            Program     :    Spam and Eggs
            Version     :    2.0.3

            Description :    The complete spam and eggs recipe guide.
            ------------------------------------------------------------

    :Example Code:

        This code can be used to print the banner above::

            >>> from utils4.user_interface import PrintBanner

            >>> PrintBanner(name='Spam and Eggs',
                            version='2.0.3',
                            desc='The complete spam and eggs recipe guide.')

    """
    def __init__(self,
                 name: str=None,
                 version: str=None,
                 desc: str=None,
                 info: dict=None,
                 chars: int=72,
                 ribbon: str='-',
                 fore: str='brightwhite',
                 back: str='black',
                 style: str='normal'):
        """Display a configurable information banner to the terminal.

        Args:
            name (str, optional): Name of your program. Defaults to None.
            version (str, optional): The program's version number.
                Defaults to None.
            desc (str, optional): Description of what your program is all
                about. Defaults to None.
            info (list, optional): A list of dictionaries containing the fields
                to be used. Defaults to None.

                The ``info`` parameter is used to generate a completely
                customised banner.  Essentially, whatever key/value pairs you
                pass in, are what will be printed in the banner.

                .. hint::

                    For example, this ``info`` parameter::

                        >>> info = [{'Program':'Spam and Eggs'},
                        >>>         {'Version':'2.0.3'},
                        >>>         {'':''},  # Gives an empty line.
                        >>>         {'Description':'The complete spam and eggs recipe guide.'},
                        >>>         {'Comments':'They\'re even better in green!'}]

                        >>> PrintBanner(info=info)

                    ... will print the banner::

                        ------------------------------------------------------------------------
                         Program        :    Spam and Eggs
                         Version        :    2.0.3

                         Description    :    The complete spam and eggs recipe guide.
                         Comments       :    They're even better in green!
                        ------------------------------------------------------------------------

            chars (int, optional): In the number of characters, the size of the
                buffer used for the background colour, and the length of the
                ribbon. Defaults to 72.
            ribbon (str, optional): The character(s) to use for the ribbon.
                If multiple characters are passed into this parameter, these
                characters will be repeated until the length of the ``chars``
                parameter is met. Defaults to ``'-'``.
            fore (str, optional): Text colour.  The eight `basic colour names`_
                are accepted as strings. Defaults to 'brightwhite'.
            back (str, optional): Background colour. The eight
                `basic colour names`_ are accepted as strings. Defaults to
                'black'.
            style (str, optional): Style of the text. Defaults to 'normal'.

                Options:
                    - dim
                    - bold
                    - normal
                    - underline

        :Design:
            In short, if the ``info`` parameter is left as ``None``, a
            default banner is generated using the values passed into
            the ``name``, ``version`` and ``desc`` parameters.

            The string templates used for the banner layout may be
            configured in this module's private :class:`~_Config` class.

            Additional configuration is available through the other
            parameters, which are all defined in the **Parameters**
            section above.

            Also, the title of the console window is updated to show the
            program's name and version, if *all* of the following criteria
            are met:

                - Windows OS
                - ``name`` parameter is not ``None``
                - ``version`` parameter is not ``None``

        :Example:

            The following code block::

                >>> from utils4.user_interface import PrintBanner

                >>> PrintBanner(name='Spam and Eggs',
                                version='2.0.3',
                                desc='The complete spam and eggs guide.',
                                chars=55,
                                ribbon='~-',
                                fore='brightyellow',
                                back='black',
                                style='normal')

            ... will print this banner in yellow text on a black background::

                ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
                 Program        :    Spam and Eggs
                 Version        :    2.0.3

                 Description    :    The complete spam and eggs guide.
                ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-


        .. _basic colour names: https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit

        """
        self._name = name
        self._version = version
        self._desc = desc
        self._info = info
        self._chars = chars
        self._ribbon = ribbon * (chars // len(ribbon))
        self._fore = fore
        self._back = back
        self._style = style
        self._to_print = []
        self._blank = ''
        self._spaces = ' '*4
        self._pad = 15
        self._adtl = 4
        self._cfg = _Config()
        self._print_prog_banner()
        self._update_console_title()

    def _add_ribbon(self):
        """Add a blank line and ribbon to start and end of banner."""
        self._to_print.insert(0, '')
        self._to_print.insert(1, self._ribbon)
        self._to_print.append(self._ribbon)
        self._to_print.append('')

    def _get_longest_key(self) -> int:
        """Return the length of the longest key, as an integer.

        :Design:
            The longest key is used to determine where the field
            separator is placed.

        Returns:
            int: Length of the longest dictionary key, in the number of
            characters.

        """
        return max(len(next(iter(i.keys()))) for i in self._info)

    @staticmethod
    def _get_os() -> str:
        """Get and return the system's OS.

        Returns:
            str: The system's OS as a string.

        """
        return platform.system().lower()

    def _print_prog_banner(self):
        """Print the banner.

        :Design:
            Using the ``info`` parameter as reference, determine if the
            default or user-defined banner should be printed; then print the
            banner using the :meth:`~UserInterface.print_` method.

        """
        # Test type of banner to create.
        if self._info is not None:
            self._setup_custom()
        else:
            self._setup_default()
        # Print program info banner.
        for line in self._to_print:
            ui.print_(text=line,
                      fore=self._fore,
                      back=self._back,
                      style=self._style,
                      h_pad=self._chars)

    def _setup_custom(self):
        """Set up the user-defined banner.

        :Design:
            Set the buffer (padding) for all 'key' elements using the length
            of the longest dict key.  This allows all ``':'`` characters to
            align, regardless of the varying lengths of each key.

            Next, iterate through the list of dictionaries and extract the
            key/value pairs for use in the banner. The banner's layout
            template is defined in this module's private :class:`~_Config`
            class.

            Finally, add the starting/ending blank line and ribbon to
            the compiled list.  This list is then used by the
            :meth:`~PrintBanner._print_prog_banner` method to print the banner
            to the terminal.

        """
        pad = self._get_longest_key() + self._adtl
        # Build print string from list of dicts.
        for i in self._info:
            for key, val in i.items():
                # Test if line should be left blank.
                if key:
                    text = self._cfg.custom_string.format(key=key,
                                                          pad=pad,
                                                          spaces=self._spaces,
                                                          val=val)
                    self._to_print.append(text)
                else:
                    # Add a blank line.
                    self._to_print.append('')
        # Add start/end ribbons.
        self._add_ribbon()

    def _setup_default(self):
        """Set up the default banner.

        :Design:
            A pre-defined list of 'key' items is iterated, which is used to
            build the list containing the lines to print.

            Finally, add the starting/ending blank line and ribbon to the
            compiled list. This list is then used by the
            :meth:`~PrintBanner._print_prog_banner` method to print the banner
            to the terminal.

        """
        # Build print string.
        for title, name in zip(['Program', 'Version', '', 'Description'],
                               [self._name, self._version, '', self._desc]):
            # Test if line should be left blank.
            if title:
                text = self._cfg.default_string.format(title=title,
                                                       pad=self._pad,
                                                       spaces=self._spaces,
                                                       name=name)
                self._to_print.append(text)
            else:
                # Add a blank line.
                self._to_print.append('')
        # Add start/end ribbons.
        self._add_ribbon()

    def _update_console_title(self):
        """For **Windows only**, update the cmd window's title.

        :Design:
            This method is only functional if the OS is Windows and the
            ``name`` and ``version`` arguments are passed.

        """
        # pylint: disable=possibly-used-before-assignment  # Referring to windll
        is_win = 'win' in self._get_os()
        if all([self._name is not None, self._version is not None, is_win]):
            # Change cmd window title.
            windll.kernel32.SetConsoleTitleW(f'{self._name} - {self._version}')


class UserInterface:
    """This class encapsulates the Linux/Windows command line interfaces and
    provides a standard way of reporting normal, alternative and abnormal
    behaviour.

    :Example:

        Below are a couple of examples showing how easy it is to print
        coloured text to the terminal.

        To print a green text to the console::

            >>> from utils4.user_interface import ui

            >>> ui.print_(text='Some text ...', fore='green', style='normal')


        To print a blue text on a white background to the console::

            >>> from utils4.user_interface import ui

            >>> ui.print_(text='Some text ...', fore='blue', back='white', style='normal')


        To print a green header to the console::

            >>> from utils4.user_interface import ui

            >>> ui.print_heading_green(text='Header for a section of output')

    """

    def __init__(self):
        """UserInterface class initialiser.

        - **Purpose**:

            If Windows is detected as the system's OS, the ``utils4.__init__``
            module initialises the ``colorama`` library, which enables the
            user to print coloured text to the Windows terminal.

        - **Background on** ``win_unicode_console``:

            The ``win_unicode_console`` library is used here to fix a problem
            between the Python :func:`~input` function and the Windows
            CLI. The problem causes ANSI characters to be **displayed** to the
            terminal, rather than **setting** colours.

        - **Background on** ``colorama``:

            The ``colorama`` library is initialised to:

              'strip ANSI characters from stdout and convert them into the
              equivalent win32 calls.'

              -- Jonathan Hartley, creator of colorama.

            The Win32 console (excluding *some* later versions of Win10) does
            not support ANSI escape sequences, and therefore (unlike UNIX and
            Unix-like systems) simply printing the escape sequence to the
            native Windows CLI with the text does *not* work. To address this,
            we use the ``colorama`` library for the low-level Win32 work.
            Thanks Jonathan!

        Note:
            It **may** be possible to remove use of ``win_unicode_console``
            in later versions of Python, possibly 3.6+.

        """
        # Removed in v1.0.0a1.
        # Only initialise win_unicode_console if on Windows.
        # if 'win' in platform.system().lower():
            # self._enable_win_unicode_console()
        self._cfg = _Config()
        self._fore = self._build_color_dict(class_=Text)
        self._back = self._build_color_dict(class_=Back)
        self._style = self._build_color_dict(class_=Style)

    def get_input(self,
                  prompt: str,
                  fore: str='white',
                  back: str='black',
                  style: str='normal',
                  ending_char: str='',
                  add_space: bool=True):
        """Deprecated version of the new method: :meth:`~prompt`.

        Warning:
            This method has been deprecated.

        """
        warnings.warn('This method has been deprecated and will be removed in a future version. '
                      'Please use the `prompt()` method instead.',
                      category=FutureWarning)
        return self.prompt(text=prompt,
                           fore=fore,
                           back=back,
                           style=style,
                           ending_char=ending_char,
                           add_space=add_space)

    def print_(self,
               text: str,
               fore: str='brightwhite',
               back: str='black',
               style: str='normal',
               h_pad: int=0,
               v_pad: int=0,
               sleep: float=0.0):
        """Wrap the built-in :func:`print` function to provide colour customisation.

        Args:
            text (str): The text to be printed to the terminal.
            fore (str, optional): The text colour. Defaults to 'brightwhite'.
            back (str, optional): Background colour. Defaults to 'black'.
            style (str, optional): ANSI style selector. Defaults to 'normal.'
            h_pad (int, optional): The amount of horizontal padding, in
                characters. This option will increase the field size to the
                value of ``h_pad`` and add (n) blank characters of background
                colour after the text string. If greater than the number of
                text characters, colour will extend past the end of the text.
                Defaults to 0.

                Note:
                    The ``h_pad`` value is a **field size** value, **not** the
                    number of spaces past the end of the text string.

            v_pad (int, optional): The amount of vertical padding, in lines.
                This option will add (n) blank lines of backgound colour above
                and below the text string, acting like a banner. The banner
                will extend to the number of spaces specified in the ``h_pad``
                parameter. Defaults to 0.
            sleep (float, optional): Number of seconds to pause the program
                after a message or banner is printed. Although the default
                sleep value is 0 seconds, the default changes to (n) second,
                if the ``v_pad`` parameter is > 0. This provides a default
                pause for the user to read the banner. The default ``v_pad``
                sleep time can be updated in this module's private
                :class:`~_Config` class. Defaults to 0.

        **Colour and Style Options:**

            - **fore / back**
                black, blue, cyan, green, magenta, red, white, yellow,
                brightblack, brightblue, brightcyan, brightgreen,
                brightmagenta, brightred, brightwhite, brightyellow

            - **style**
                bold, dim, normal, underline

        :Design:
            This method extends the functionality of the built-in :func:`print`
            function by adding the options for text/background colouring and
            padding. The user can pass specific text/background colours along
            with a style and horizontal and vertical padding.

            The colour and style strings are implemented using ANSI escape
            sequences, which are added to the text string.

            In addition to colour, horizontal and vertical padding are
            available.

            After a message or banner is printed, the sleep timer can be
            called to pause the program for (n) seconds, for the user to read
            the message or banner. If the ``v_pad`` value is > 0, and the
            sleep value is 0, the sleep timer value is overridden with the
            value defined in this module's private :class:`~_Config` class,
            under the ``v_pad_sleep`` key.

            For further detail, refer to the **Parameters** section
            of this docstring, and refer to the **Colour and Style Options**
            section for each string parameter's available options.

        """
        _fore = self._fore[fore.lower()]
        _back = self._back[back.lower()]
        _style = self._style[style.lower()]
        # Test for horizontal padding.
        if h_pad > 0:
            text = self._pad(text=text, padto=h_pad)
            spaces = self._pad(text='', padto=h_pad)
        else:
            # Create spaces for v-padding.
            spaces = self._pad(text='', padto=len(text))
        # Test for upper and lower padding.
        if v_pad > 0:
            # Add blank line above banner.
            print('')
            # Print upper pad (n) times.
            for _ in range(v_pad):
                print(f'{_fore}{_back}{_style}{spaces}{Text.RESET}')
            # Print message & add space before text to bring off console wall.
            print(f'{_fore}{_back}{_style}{text}{Text.RESET}')
            # Print lower pad (n) times.
            for _ in range(v_pad):
                print(f'{_fore}{_back}{_style}{spaces}{Text.RESET}')
            # Add blank line below banner.
            print('')
            # Update sleep timer for banner if sleep=0.
            sleep = self._cfg.v_pad_sleep if sleep == 0 else sleep
        else:
            # Print message with no v-padding.
            print(f'{_fore}{_back}{_style}{text}{Text.RESET}')
        # Pause for user to read output.
        time.sleep(sleep)

    def print_alert(self, text: str, style: str='normal'):
        """Print red text on a black background.

        Args:
            text (str): Text to be printed.
            style (str, optional): Style to be used. Defaults to 'normal'.

        """
        self.print_(text=text, fore='brightred', back='black', style=style)

    @staticmethod
    def print_blank_lines(quantity: int=1):
        """Print (n) blank lines.

        Args:
            qualtity (int, optional): Number of blank lines to print.
                Defaults to 1.

        """
        for _ in range(quantity):
            print('')

    @staticmethod
    def print_error(error: object):
        """Print red error text on a black background.

        Args:
            error (object): This is the **error object** generated by the
                Exception.

        This method calls the :meth:`~reporterror.reporterror` method
        to generate the error message.

        :Example:

            To print an error message::

                >>> from utils4.user_interface import ui

                >>> try:
                >>>     1/0
                >>> except Exception as err:
                >>>     ui.print_error(error=err)

                ERROR:	division by zero
                TYPE:	<class 'ZeroDivisionError'>
                MODU:	/tmp/ipykernel_27103/573922745.py
                FUNC:	<module>
                LINE:	2
                CMD:    1/0

        """
        print(Text.BRIGHTRED)
        reporterror(error)
        print(Text.RESET)

    def print_error_unexpected(self):
        """Print red 'unexpected error' text on black background.

        :Design:
            This method uses the call stack to print a message for
            'unexpected error' errors.

        """
        stack = inspect.stack()
        mthd = inspect.currentframe().f_back.f_code.co_name
        last = stack[1][0]
        clss = last.f_locals.get('self').__class__
        line = last.f_lineno
        text = (f'An unexpected error has occurred whilst running the "{mthd}" method\n'
                f'in "{clss}", on line number {line}')
        self.print_alert(text)

    def print_heading_blue(self, text: str, fore: str='brightwhite', style: str='normal', padto: int=0):
        """Print white text on a blue background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'brightwhite'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='blue', style=style, h_pad=padto)

    def print_heading_cyan(self, text: str, fore: str='black', style: str='normal', padto: int=0):
        """Print black text on a cyan background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'black'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='cyan', style=style, h_pad=padto)

    def print_heading_green(self, text: str, fore: str='black', style: str='normal', padto: int=0):
        """Print black text on a green background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'black'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='green', style=style, h_pad=padto)

    def print_heading_red(self, text: str, fore: str='black', style: str='normal', padto: int=0):
        """Print black text on a red background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'black'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='brightred', style=style, h_pad=padto)

    def print_heading_white(self, text: str, fore: str='black', style: str='normal', padto: int=0):
        """Print black text on a white background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'black'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='white', style=style, h_pad=padto)

    def print_heading_yellow(self, text: str, fore: str='black', style: str='normal', padto: int=0):
        """Print black text on a yellow background.

        Args:
            text (str): Text to be printed.
            fore (str, optional): Text colour. Defaults to 'black'.
            style (str, optional): Style to be used. Defaults to 'normal'.
            padto (int, optional): Padding width, as number of characters.
                Defaults to 0.

        """
        self.print_(text=text, fore=fore, back='yellow', style=style, h_pad=padto)

    def print_normal(self, text: str, style: str='normal'):
        """Print green text on a black background.

        Args:
            text (str): Text to be printed.
            style (str, optional): Style to be used. Defaults to 'normal'.

        """
        self.print_(text=text, fore='brightgreen', back='black', style=style)

    def print_warning(self, text: str, style: str='normal'):
        """Print yellow text on a black background.

        Args:
            text (str): Text to be printed.
            style (str, optional): Style to be used. Defaults to 'normal'.

        """
        self.print_(text=text, fore='brightyellow', back='black', style=style)

    def prompt(self,
               text: str,
               fore: str='brightwhite',
               back: str='black',
               style: str='normal',
               ending_char: str='',
               add_space: bool=True):
        r"""Get user input via a CLI prompt formatted by the caller.

        This method extends the built-in :func:`input` function (although not
        used by this method) by adding appearance control and text colouring.
        Like the :func:`input` function, the user's input is returned to the
        caller as a ``str`` type.

        Args:
            text (str): The text to be displayed.
            fore (str, optional): Text colour. Defaults to 'brightwhite'.
            back (str, optional): Background colour. Defaults to 'black'.
            style (str, optional): The 'normal' style selects the 8 original
                foreground colours (SGR 30-37). The 'bright' style provides
                access to the 8 additional foreground colours (SGR 90-97).
                Defaults to 'normal'.
            ending_char (str, optional): Character to be added to the end of
                the prompt. If the user's input should be on a new line,
                pass ``\n`` into this parameter. Defaults to ``''``.
            add_space (bool, optional): Add a space separator between the
                prompt and the user's input. Defaults to True.

        **Colour and Style Options:**

            - **fore / back**
                black, blue, cyan, green, magenta, red, white, yellow,
                brightblack, brightblue, brightcyan, brightgreen,
                brightmagenta, brightred, brightwhite, brightyellow

            - **style**
                bold, dim, normal, underline

        :Example:

            To use the prompt in its standard form::

                >>> inp = ui.prompt('Enter a number:')

                Enter a number: 73

                >>> inp
                '73'


            Request user input in red text::

                >>> inp = ui.prompt('Enter a number:', fore='brightred')

                Enter a number: 13

                >>> inp
                '13'


            Request user input in red text in a new line::

                >>> inp = ui.prompt('An unnecessarily long prompt requesting a number:',
                                    fore='brightred',
                                    ending_char='\n',
                                    add_space=False)

                An unnecessarily long prompt requesting a number:
                37

                >>> inp
                '37'

        """
        _fore = self._fore[fore.lower()]
        _back = self._back[back.lower()]
        _style = self._style[style.lower()]
        space = ' ' if add_space else ''
        # Reset colours before printing a new line char.
        if ending_char == '\n':
            ending_char = os.linesep
        text_ = f'{_fore}{_back}{_style}{text}{Text.RESET}{space}'
        # Prompt user and return input to the caller.
        # print() and sys calls are used as the input() function does not
        # play nicely with the ANSI sequences on Windows.
        print(text_, end=ending_char)
        sys.stdout.flush()
        resp = sys.stdin.readline().strip()  # Remove the newline character from the read.
        return resp

    @staticmethod
    def _build_color_dict(class_: object) -> dict:
        """Create a dictionary of colours available in the ``termcolours``
        ``.Text``, ``.Back`` and ``.Style`` classes.

        Args:
            class_ (object): Class object to be parsed and extracted into a
                dict.

        :Example:

            For example, when the ``termcolours.Text`` class is passed,
            the output looks like::

                {'black': '\x1b[30m',
                 'blue': '\x1b[34m',
                 ...,
                 'white': '\x1b[37m',
                 'yellow': '\x1b[33m'}

        Returns:
            dict: A dictionary of key/values (attr/values) from the passed
            class object, with the keys in lower case.

        """
        return {k.lower():v for k, v in class_.__dict__.items()}

    # Removed in v1.0.0a1.
    # @staticmethod
    # def _enable_win_unicode_console():
    #     """Enable the Windows CLI console colours for Py3."""
    #     win_unicode_console.enable(use_readline_hook=False)

    @staticmethod
    def _pad(text: str, padto: int):
        """Pad the text value, with (n) spaces.

        Args:
            text (str): Text to print.
            padto (int): Field size for text block.

        :Design:
            The ``padto`` parameter is a **field size** value, **not** the
            number of blank characters added to the end of the text string.

        """
        return f'{text.expandtabs(4):{padto}}'


ui = UserInterface()
