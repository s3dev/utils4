#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a simple wrapper around Python's
            built-in ``warnings`` library, and enables easy access
            to ignore (a given set of) Python warnings.  These warnings
            can be configured in your app's config file.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
    Example code use::

        from utils3 import pywarnings

        class MyApp(object):
            '''My really cool app!'''

            def __init__(self):
                '''Class initialiser.'''
                self._cfg = # You app's config file
                self._pywarns = pywarnings.PyWarnings(config=self._cfg)

            def main():
                '''Main app controller.'''
                self._pywarns.ignore_warnings()
                # DO APP STUFF
                # ...
                self._pywarns.reset_warnings()

"""

import warnings

class PyWarnings(object):
    """A simple wrapper around Python's built-in ``warnings`` library.

    This class provides easy access to ignore (a given set of) warnings
    using your program's config file.

    An example of your ``py_warnings`` config file key is shown below::

        {"py_warnings": {"ignore": true,
                         "categories": ["PendingDeprecationWarning",
                                        "FutureWarning"]}}

    * The ``ignore`` key toggles if the listed warnings are disabled.
    * The ``categories`` key is a list of Python warnings you wish
      to disable.  This list **is not** case sensitive.

    Args:
        config (dict): A dictionary containing your app's config.
            (Or, at least a dictionary containing the ``py_warnings``
            key.)

    Note:
        Remember to call the :meth:`~reset_warnings` method at the end
        of your program!

    """

    def __init__(self, config):
        """Class initialiser."""
        self._cfg = config

    def ignore_warnings(self):
        """Ignore Python warnings.

        This method is designed to ignore (a given set of) Python
        warnings. Remember, the **warnings must be reset at the end of
        your program**.  This is **not** done automatically.

        These actions are controlled via the ``py_warnings`` key in
        your config file.

            * ``ignore``: Boolean flag to ignore the warnings
            * ``categories``: A list of warning type(s) to ignore

        Reference:
            The list of warnings in the ``warn_types`` local dictionary
            variable was taken from `here`_.

            .. _here: https://docs.python.org/3.5/library/warnings.html#warning-categories

        """
        ignore = self._cfg['py_warnings']['ignore']
        categories = self._cfg['py_warnings']['categories']
        # MAKE CASE INSENSITIVE
        categories = [c.lower() for c in categories]
        if ignore:
            warn_types = {'byteswarning': BytesWarning,
                          'deprecationwarning': DeprecationWarning,
                          'futurewarning': FutureWarning,
                          'importwarning': ImportWarning,
                          'pendingdeprecationwarning': PendingDeprecationWarning,
                          'resourcewarning': ResourceWarning,
                          'runtimewarning': RuntimeWarning,
                          'syntaxwarning': SyntaxWarning,
                          'unicodewarning': UnicodeWarning,
                          'userwarning': UserWarning,
                          'warning': Warning}
            for category in categories:
                warnings.simplefilter('ignore', warn_types[category])

    @staticmethod
    def reset_warnings():
        """Turn Python warnings back on."""
        warnings.resetwarnings()
