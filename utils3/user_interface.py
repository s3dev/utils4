# -*- coding: utf-8 -*-
"""
:Purpose:   This class module provides an interface to the Win / Linux
            Command Line Interpreters (CLI).

            It contains a :class:`~UserInterface` class whose methods
            provide a standard way of reporting normal, alternative and
            abnormal behaviour.  The following formats are built-in:

                - **fully customisable messages and headers** via the
                    :meth:`~UserInterface.print_` method
                - **headings**
                    black text, cyan background
                    black text, green background
                    black text, white background
                    black text, yellow background
                - **user input expected**
                    white text, black background
                - **normal behaviour**
                    green text, black background
                - **alternative behaviour** (e.g. a warning)
                    yellow text, black background
                - **abnormal or erroneous behaviour**
                    red text, black background

:Platform:  Linux/Windows | Python 3.5
:Developer: M Critchard / J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

"""

import inspect
import os
import platform
import time

import win_unicode_console
from colorama import Fore, Back, Style
from colorama import init as colourinit

import utils3.config as config
import utils3.reporterror as reporterror

# ALLOW OUR IMPORT ORDER
# pylint: disable=wrong-import-order
# TEST OS BEFORE IMPORTING THESE:
if 'win' in platform.system().lower():
    from ctypes import windll


class UserInterface(object):
    """This class encapsulates the Linux/Windows CLIs and provides a
    standard way of reporting normal, alternative and abnormal
    behaviour.

    :Example:
        To print a green header to the console::

            import utils3.user_interface as ui

            _UI = ui.UserInterface()
            _UI.print_heading_green(text='THIS IS MY HEADER')

    """

    def __init__(self):
        """Class initialiser.

        :Purpose:
            This constructor initialises ``colorama`` - which enables
            the user to print coloured text to the Windows CLI - and
            loads the config file, which is used throughout the class.

        :Background win_unicode_console:
            ``win_unicode_console`` is used here to fix a problem
            between the Python :func:`~input` function and the Windows
            CLI. The problem causes ANSI characters to be **displayed**
            to the console, rather than **setting** colours.

        Note:
            It **may** be possible to remove use of
            ``win_unicode_console`` when/if we move to Python 3.6.

        :Background colorama:
            Colorama is initialised here to "strip ANSI characters from
            stdout and convert them into the equivalent win32 calls";
            per Jonathan Hartley, creator of Colorama.

            The Win32 console (excluding *some* versions of Win10) does
            not support ANSI escape sequences, and therefore (unlike
            *nix) simply printing the escape sequence to the native
            Win CLI with the text does not work.  So we use Colorama
            for the low-level win32 work.  Thanks Jonathan!!

        """
        # INSTALL FIX FOR PYTHON 3 WINDOWS CLI ISSUE
        win_unicode_console.enable()
        # COLORAMA INITIALISATION
        colourinit()
        # SET LOCATION OF THE UI CONFIG FILE EXPLICITLY (SHOULD WORK FOR WIN AND LINUX)
        ui_config_file = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                      'user_interface_config.json')
        # LOAD CONFIG FILE
        self._cfg = config.loadconfig(filename=ui_config_file)
        # BUILD REFERENCE DICTS OF COLORAMA FORE / BACK / STYLE
        self._fore  = self._build_color_dict(class_=Fore)
        self._back  = self._build_color_dict(class_=Back)
        self._style = self._build_color_dict(class_=Style)

    def get_input(self, prompt, fore='white', back='black',
                  style='normal', ending_char='\n', add_space=False):
        """Get user input via a CLI prompt formatted by the caller.

        This method extends the built-in :func:`~raw_input()` user
        prompt by adding appearance control and text colouring through
        ``colorama``.  Like the :func:`~raw_input()` function, the
        user's input is returned to the caller.

        Args:
            prompt (str): The prompt text to be displayed.
            fore (str): The text colour, as a string.
            back (str): Background colour, as a string.
            style (str): The 'normal' style selects the 8 original
                foreground colours (SGR 30-37).
                The 'bright' style provides access to the 8 additional
                foreground colours (SGR 90-97).
            ending_char (str): Character to be added to the end of the
                prompt.
            add_space (bool): Add a space separator between the prompt
                and the user's input.

        :Options:

            - **fore / back**
                black, blue, cyan, green, magenta, red, white, yellow
            - **style**
                bright, dim, normal

        """
        # DECODE COLOR FROM STRING TO ANSI SEQUENCE
        _fore   = self._fore[fore.lower()]
        _back   = self._back[back.lower()]
        _style  = self._style[style.lower()]
        # TEST FOR SPACE TO BE ADDED TO THE END OF THE PROMPT
        space = ' ' if add_space is True else ''
        # RESET COLOURS BEFORE PRINTING A NEW LINE ENDING CHAR
        if ending_char == '\n': ending_char = '%s%s' % (Style.RESET_ALL, '\n')
        # BUILD THE PROMPT STRING
        prompt = '%s%s%s%s%s%s%s' % (_fore, _back, _style, prompt, ending_char,
                                     Style.RESET_ALL, space)
        # PROMPT USER AND RETURN INPUT TO THE CALLER
        return input(prompt)

    def print_(self, text, fore='white', back='black', style='bright',
               h_pad=0, v_pad=0, sleep=0):
        """Print the passed text in the specified format.

        :Design:
            This method extends the functionality of the built-in
            :func:`~print` function by adding the options for
            text/background colouring and padding.  The user can pass
            specific text/background colours along with a style and
            horizontal and vertical padding.

            The colour and style strings are referenced against
            colorama's .Fore() .Back() and .Style() classes -
            (via a dictionary built into this class' constructor) -
            where the ANSI escape sequences are extracted and added to
            the output text string.

            In addition to colour, horizontal and vertical padding are
            available.

            After a message or banner is printed, the sleep timer can be
            called to pause the program for (n) seconds, for the user to
            read the message or banner.  If the ``v_pad`` value is > 0,
            and the sleep value is 0, the sleep timer value is
            overridden with the value defined in the config file's
            ``v_pad_sleep`` key.

            For further detail, refer to the **Parameters** section
            of this docstring, and refer to the **Options** section for
            each string parameter's available options.

        Args:
            text (str): The text to be printed to the console.
            fore (str): The text colour, as a string.
            back (str): Background colour, as a string.
            style (str): The 'normal' style selects the 8 original
                foreground colours (SGR 30-37).
                The 'bright' style provides access to the 8 additional
                foreground colours (SGR 90-97).
            h_pad (int): The amount of horizontal padding, in
                characters.
                This option will increase the field size to the value
                of ``h_pad`` and add (n) blank characters of background
                colour after the text string.
                If greater than the number of text characters, colour
                will extend past the end of the text.  Note: the
                ``h_pad`` value is a **field size** value, **not** the
                number of spaces past the end of the text string.
            v_pad (int): The amount of vertical padding, in lines.
                This option will add (n) blank lines of backgound
                colour above and below the text string - acting like a
                banner.  The banner will extend to the number of spaces
                specified in the ``h_pad`` parameter.
            sleep (float): Number of seconds to pause the program after
                a message or banner is printed.
                Although the default sleep value is 0 seconds, the
                default changes to (n) second, if the ``v_pad``
                parameter is > 0.  This provides a default pause for
                the user to read the banner.  The default ``v_pad``
                sleep time can be updated in the config file.

        :Options:

            - **fore / back**
                black, blue, cyan, green, magenta, red, white, yellow
            - **style**
                bright, dim, normal

        """
        # DECODE COLOR FROM STRING TO ANSI SEQUENCE
        _fore   = self._fore[fore.lower()]
        _back   = self._back[back.lower()]
        _style  = self._style[style.lower()]

        # TEST FOR HORIZONTAL PADDING
        if h_pad > 0:
            # PAD TEXT
            text = self._pad(text=text, padto=h_pad)
            # CREATE SPACES FOR V-PADDING
            spaces = self._pad(text='', padto=h_pad)
        else:
            # CREATE SPACES FOR V-PADDING
            spaces = self._pad(text='', padto=len(text))

        # TEST FOR UPPER AND LOWER PADDING
        if v_pad > 0:
            # ADD BLANK LINE ABOVE BANNER
            print('')
            for _ in range(v_pad):
                # PRINT UPPER PAD (N) TIMES
                print('%s%s%s %s%s' % (_fore, _back, _style, spaces, Style.RESET_ALL))
            # PRINT MESSAGE & ADD SPACE BEFORE TEXT TO BRING OFF CONSOLE WALL
            print('%s%s%s %s%s' % (_fore, _back, _style, text, Style.RESET_ALL))
            for _ in range(v_pad):
                # PRINT LOWER PAD (N) TIMES
                print('%s%s%s %s%s' % (_fore, _back, _style, spaces, Style.RESET_ALL))
            # ADD BLANK LINE BELOW BANNER
            print('')
            # UPDATE SLEEP TIMER FOR BANNER IF SLEEP=0
            sleep = self._cfg['v_pad_sleep'] if sleep == 0 else sleep
        else:
            # PRINT MESSAGE
            print('%s%s%s%s%s' % (_fore, _back, _style, text, Style.RESET_ALL))

        # PAUSE FOR USER TO READ OUTPUT
        time.sleep(sleep)

    def print_error_enviro(self):
        """Print red environment error text on a black background.

        :Design:
            It uses the stack and the config file to print a message for
            environment errors.

        """
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['enviro'].format(mtd, cls)
        self.print_error(text)

    def print_error_intoor(self):
        """Print red 'integer out of range' error text on black background.

        :Design:
            It uses the stack and the config file to print a message for
            'integer out of range' errors.

        """
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['intoor'].format(mtd, cls)
        self.print_error(text)

    def print_error_notimp(self):
        """Print red 'not implemented' error text on black background.

        :Design:
            It uses the stack and the config file to print a message
            for 'not implemented' errors.

        """
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['notimp'].format(mtd, cls)
        self.print_error(text)

    def print_error_unexpd(self):
        """Print red 'unexpected error' text on black background.

        :Design:
            It uses the stack and the config file to print a message for
            'unexpected error' errors.

        """
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['unexpd'].format(mtd, cls)
        self.print_error(text)

    def print_error_windws(self):
        """Print red 'Windows error' text on black background.

        :Design:
            It uses the stack and the config file to print a message for
            'Windows error' errors.

        """
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['windws'].format(mtd, cls)
        self.print_error(text)

    def print_heading_cyan(self, text, padto=0):
        """Print black text on a cyan background."""
        self.print_(text=text, fore='black', back='cyan', style='normal', h_pad=padto)

    def print_heading_green(self, text, padto=0):
        """Print black text on a green background."""
        self.print_(text=text, fore='black', back='green', style='normal', h_pad=padto)

    def print_heading_red(self, text, padto=0):
        """Print black text on a red background."""
        self.print_(text=text, fore='black', back='lightred_ex', style='dim', h_pad=padto)

    def print_heading_white(self, text, padto=0):
        """Print black text on a white background."""
        self.print_(text=text, fore='black', back='white', style='normal', h_pad=padto)

    def print_heading_yellow(self, text, padto=0):
        """Print black text on a yellow background."""
        self.print_(text=text, fore='black', back='yellow', style='normal', h_pad=padto)

    def print_alert(self, text):
        """Print red text on a black background."""
        self.print_(text=text, fore='red', back='black', style='bright')

    def print_normal(self, text):
        """Print green text on a black background."""
        self.print_(text=text, fore='green', back='black', style='bright')

    def print_warning(self, text):
        """Print yellow text on a black background."""
        self.print_(text=text, fore='yellow', back='black', style='bright')

    @staticmethod
    def print_blank_lines(quantity=1):
        """Print (n) blank lines."""
        for _ in range(quantity): print('')

    @staticmethod
    def print_error(text):
        """Print red error text on a black background.

        Args:
            text (str): This is the **error object** generated by the
                Exception.

        :Example:
            ::

                import utils3.user_interface as ui

                _ui = ui.UserInterface()

                try:
                    1/0
                except Exception as err
                    _ui.print_error(text=err)

        """
        print(Fore.LIGHTRED_EX)
        reporterror.reporterror(text)
        print(Style.RESET_ALL)

    @staticmethod
    def _pad(text, padto):
        """Pad the text value, with (n) spaces.

        Args:
            text (str): Text to print.
            padto (int): Field size for text block.

        :Design:
            The padto value is a **field size** value, **not** the
            number of blank characters added to the end of the text
            string.

        """
        return '{:{padto}}'.format(text.expandtabs(4), padto=padto)

    @staticmethod
    def _build_color_dict(class_):
        """Create a dictionary of colours available in the ``colorama``
        ``.Fore`` and ``.Back`` classes.

        :Example:
            For example, when the ``colorama.Fore`` class is passed,
            the output looks like::

                {'black': '\x1b[30m', 'blue': '\x1b[34m', ...,
                 'white': '\x1b[37m', 'yellow': '\x1b[33m'}

        """
        return {k.lower():v for k, v in vars(class_).items()}


class PrintBanner(object):
    """
    PURPOSE:
    This class is used to print a program information banner to the CLI,
    which may be useful if you want to use a 'standardised' program
    header across all of your programs.  This class can be called at
    the start of a program.

    Refer to the DESIGN and PARAMETERS sections for configuration
    details; as this banner is highly configurable.

    For example:
    ------------------------------------------------------------------
    Program     :    bob_the_great
    Version     :    2.0.3

    Description :    Gives conclusive proof why Bob is so great.
    ------------------------------------------------------------------

    USE:
    import utils3.user_interface as ui
    ui.PrintBanner(name='bob_the_great', version='2.0.3',
                   desc='Gives conclusive proof why Bob is so great.')
    """

    # ALLOW MANY ATTRIBS AND FEW METHODS
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(self, name=None, version=None, desc=None, info=None, chars=72,
                 ribbon='-', fore='white', back='black', style='bright'):
        """
        Display program info to the CLI at the start of a program.

        DESIGN:
        In short, if the 'info' parameter is left as None, a default
        banner is generated using the values passed into the name,
        version and desc parameters.

        The string templates used for the banner layout may be
        configured in the UI config file.

        Additional configuration is available through the other
        parameters, which are all defined in the PARAMETERS section
        below.

        Also, the title of the console window is updated to show the
        program's name and version, if all of the following criteria
        are met:
            - Windows OS
            - name parameter is not None
            - version parameter is not None

        BASIC PARAMETERS:
        - name
        Name of your program.
        - version
        The version number of your program.
        - desc
        Description of what your program is all about.

        INFO PARAMETER:
        - info
        The info parameter is used to generate a completely customised
        banner.  Basically, whatever key/value pairs you pass in, are
        what will be printed in the banner.

        This parameter accepts a list of dictionaries.  For example:
        info = [{'Program':'bob_the_great'},
                {'Version':'2.0.3'},
                {'':''},
                {'Description':'Gives proof why Bob is great.'},
                {'Comments':'Some more reasons Bob is so great.'}]

        This info parameter would be parsed into:
        ----------------------------------------------------------------
         Program          :    bob_the_great
         Version          :    2.0.3

         Description      :    Gives proof why Bob is great.
         Comments         :    Some more reasons Bob is so great.
        ----------------------------------------------------------------

        CONFIG PARAMETERS:
        - chars
        In the number of characters, the size of the buffer used for
        the background colour, and the length of the ribbon.
        - ribbon
        The character(s) to use for the ribbon.
        If multiple characters are passed into this parameter, these
        characters will be repeated until the length of the 'chars'
        parameter is met.
        - fore
        Text colour.  The eight basic colour names are accepted as
        strings.
        - back
        Background colour.  The eight basic colour names are accepted
        as strings.
        - style
        Brightness of the text/background.  Accepted strings:
            - dim
            - bright (default)
            - normal

        USE:
        import utils3.user_interface as ui
        ui.PrintBanner(name='bob_the_great', version='2.0.3',
                       desc='Gives proof why Bob is so great.',
                       chars=55, ribbon='~-', fore='yellow',
                       back='black', style='bright')

        Will print this:
        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
         Program        :    bob_the_great
         Version        :    2.0.3

         Description    :    Gives proof why Bob is so great.
        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
        """

        # SET LOCATION OF THE UI CONFIG FILE EXPLICITLY
        conf_file = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                 'user_interface_config.json')

        # INITIALISE
        self._name      = name
        self._version   = version
        self._desc      = desc
        self._info      = info
        self._chars     = chars
        self._ribbon    = ribbon * (chars // len(ribbon))
        self._fore      = fore
        self._back      = back
        self._style     = style
        self._to_print  = []
        self._blank     = ''
        self._spaces    = ' '*4
        self._pad       = 15
        self._adtl      = 4
        self._cfg       = config.loadconfig(conf_file)
        self._ui        = UserInterface()

        # PRINT PROGRAM INFO BANNER
        self._print_prog_banner()

        # UPDATE CONSOLE WINDOW TITLE
        self._update_console_title()

    # ------------------------------------------------------------------
    def _add_ribbon(self):
        """Add blank line and ribbon to start and end of banner."""
        # ADD BLANK START/END LINES AND RIBBON
        self._to_print.insert(0, '')
        self._to_print.insert(1, self._ribbon)
        self._to_print.append(self._ribbon)
        self._to_print.append('')

    # ------------------------------------------------------------------
    def _get_longest_key(self):
        """Return the length of the longest key, as an integer."""
        keys = [list(i)[0] for i in self._info]
        longest = max([len(i) for i in keys])
        return longest

    # ------------------------------------------------------------------
    def _print_prog_banner(self):
        """
        Using the 'info' parameter as reference, determine if the
        default or user-defined banner should be printed; then print
        the banner using the UserInterface class.
        """
        # TEST TYPE OF BANNER TO CREATE
        if self._info is not None:
            self._setup_custom()
        else:
            self._setup_default()

        # PRINT PROGRAM INFO BANNER
        for text in self._to_print:
            self._ui.print_(text=text, fore=self._fore, back=self._back,
                            style=self._style, h_pad=self._chars)

    # ------------------------------------------------------------------
    def _setup_custom(self):
        """
        Set up the user-defined banner.

        DESIGN:
        Set the buffer (pad) for all 'key' elements using the length of
        the longest dict key.  This allows all ':' characters to align,
        regardless of the varying lengths of each key.

        Then, iterate through the list of dictionaries and extract the
        key/value pairs for use in the banner.  The banner's layout
        template is defined in the UI config file.

        Finally, add the starting/ending blank line and ribbon to the
        compiled list.  This list is then used by the
        _print_prog_banner() method to print the banner to the CLI.
        """
        # DETERMINE REQUIRED PADDING
        pad = self._get_longest_key() + self._adtl

        # BUILD PRINT STRING FROM LIST OF DICTS
        for i in self._info:
            for key, val in i.items():
                # TEST IF LINE SHOULD BE LEFT BLANK
                if key != '':
                    self._to_print.append(self._cfg['cust_str'].format(key=key, pad=pad,
                                                                       spaces=self._spaces,
                                                                       val=val))
                else:
                    # ADD A BLANK LINE
                    self._to_print.append('')

        # ADD START/END RIBBON
        self._add_ribbon()

    # ------------------------------------------------------------------
    def _setup_default(self):
        """
        Set up the default banner.

        DESIGN:
        A pre-defined list of 'key' items is iterated, which is used to
        build the list containing the lines to print.

        Finally, add the starting/ending blank line and ribbon to the
        compiled list.  This list is then used by the
        _print_prog_banner() method to print the banner to the CLI.
        """
        # BUILD PRINT STRING
        for title, name in zip(['Program', 'Version', '', 'Description'],
                               [self._name, self._version, '', self._desc]):
            # TEST IF LINE SHOULD BE LEFT BLANK
            if title != '':
                self._to_print.append(self._cfg['def_str'].format(title=title, pad=self._pad,
                                                                  spaces=self._spaces, name=name))
            else:
                # ADD A BLANK LINE
                self._to_print.append('')

        # ADD START/END RIBBON
        self._add_ribbon()

    # ------------------------------------------------------------------
    def _update_console_title(self):
        """
        For Windows, update the console window title.

        DESIGN:
        This method is only functional if the OS is Windows and the
        name and version arguments are passed.
        """
        # TEST OS
        is_win = 'win' in self._get_os()
        # TEST QUALIFIERS
        if all([self._name is not None, self._version is not None, is_win]):
            # CHANGE CMD WINDOW TITLE
            windll.kernel32.SetConsoleTitleW(u'%s - %s' % (self._name, self._version))

    # ------------------------------------------------------------------
    @staticmethod
    def _get_os():
        """Return the OS."""
        return platform.system().lower()
