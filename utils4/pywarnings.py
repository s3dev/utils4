#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a simple wrapper around Python's built-in
            ``warnings`` library, and enables easy access to ignore a single
            or set of Python warnings.

            While this module can be used to ignore a single warning, the true
            purpose of this module is to enable 'passive' warning control by
            having the ability to use a ``dict`` from your app's config file
            to control the display (or non-display) of warnings. Refer to the
            use cases below for an example.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:

    Ignore a single warning manually::

        >>> import warnings  # Imported for test demo only.
        >>> from utils4 import pywarnings

        >>> pywarn = pywarnings.PyWarnings(ignore=True, categories='FutureWarning')
        >>> pywarn.ignore_warnings()

        >>> # Test.
        >>> warnings.warn('', FutureWarning)

        >>> # Re-enable warnings.
        >>> pywarn.reset_warnings()

        >>> # Test.
        >>> warnings.warn('', FutureWarning)
        /tmp/ipykernel_48184/477226589.py:1: FutureWarning:
          warnings.warn('', FutureWarning)


    Ignore a list of warnings manually::

        >>> import warnings  # Imported for test demo only.
        >>> from utils4 import pywarnings

        >>> pywarn = pywarnings.PyWarnings(ignore=True,
                                           categories=['FutureWarning',
                                                       'ResourceWarning',
                                                       'UserWarning'])
        >>> pywarn.ignore_warnings()

        >>> # Test.
        >>> for w in [FutureWarning, ResourceWarning, UserWarning]:
        >>>     warnings.warn('', w)

        >>> # Re-enable warnings.
        >>> pywarn.reset_warnings()

        >>> # Test.
        >>> for w in [FutureWarning, ResourceWarning, UserWarning]:
        >>>     warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: FutureWarning:
          warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: ResourceWarning:
          warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: UserWarning:
          warnings.warn('', w)


    Ignore a list of warnings manually using a ``dict`` from your app's config
    file::

        >>> import warnings  # Imported for test demo only.
        >>> from utils4 import pywarnings

        >>> config = {'key1': 'value1',
                      'key2': 'value2',
                      'py_warnings': {'ignore': True,
                                      'categories': ['FutureWarning',
                                                     'ResourceWarning',
                                                     'UserWarning']},
                      'keyN': ['value10', 'value11', 'value12']}

        >>> pywarn = pywarnings.PyWarnings(config=config)
        >>> pywarn.ignore_warnings()

        >>> # Test.
        >>> for w in [FutureWarning, ResourceWarning, UserWarning]:
        >>>     warnings.warn('', w)

        >>> # Re-enable warnings.
        >>> pywarn.reset_warnings()

        >>> # Test.
        >>> for w in [FutureWarning, ResourceWarning, UserWarning]:
        >>>     warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: FutureWarning:
          warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: ResourceWarning:
          warnings.warn('', w)
        /tmp/ipykernel_48184/3608596380.py:2: UserWarning:
          warnings.warn('', w)

"""

import warnings


class PyWarnings:
    """A simple wrapper around Python's built-in ``warnings`` library.

    This class provides easy access to ignore a single, or set of Python
    warnings using your program's config file.

    An example of your ``py_warnings`` config file key is shown below::

        {"py_warnings": {"ignore": True,
                         "categories": ["PendingDeprecationWarning",
                                        "FutureWarning"]}}

    -  The ``ignore`` key toggles if the listed warnings are disabled.
    -  The ``categories`` key is a list of Python warnings you wish
       to disable.  This list **is not** case sensitive.

    Args:
        ignore (bool): ``True`` will cause warnings to be ignored. This
            argument enables the ignoring/not ignoring of warnings, without
            needing to change your source code.

        categories (Union[str, list]): A single category to ignore, or a list
            of categories.
        config (dict): A dictionary *containing* the following::

            {"py_warnings": {"ignore": true,
                             "categories": ["PendingDeprecationWarning",
                                            "FutureWarning"]}}

    :Required Arguments:
        Either the (``ignore`` *and* ``categories``) arguments must be
        provided, *or* the ``config`` argument on its own.

    Note:
        Remember to call the :meth:`~reset_warnings` method at the end
        of your program!

    """

    _WARN_TYPES = {'byteswarning': BytesWarning,
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

    def __init__(self, ignore=None, categories=None, config=None):
        """Class initialiser."""
        if config:
            self._ignore = config['py_warnings']['ignore']
            self._categories = config['py_warnings']['categories']
        else:
            self._ignore = ignore
            self._categories = categories

    def ignore_warnings(self):
        """Ignore Python warnings.

        This method is designed to ignore a single, or set of Python warnings.
        Remember, the **warnings must be reset at the end of your program**,
        as this is **not** done automatically.

        These actions are controlled via the ``py_warnings`` key in
        your config file.

            - ``ignore``: Boolean flag to ignore the warnings
            - ``categories``: A list of warning type(s) to ignore

        :Reference:
            The list of warnings in the :attr:`_WARN_TYPES` class dictionary
            was taken from the Python ``warnings`` documentation, which can be
            found `here`_.

            .. _here: https://docs.python.org/3.5/library/warnings.html#warning-categories

        """
        if not isinstance(self._categories, list):
            self._categories = [self._categories]  # Ensure categories is a list.
        if self._ignore:
            for category in self._categories:
                warnings.simplefilter('ignore', self._WARN_TYPES[category.lower()])

    @staticmethod
    def reset_warnings():
        """Turn Python warnings back on."""
        warnings.resetwarnings()
