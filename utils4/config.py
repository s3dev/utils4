# -*- coding: utf-8 -*-
"""
:Purpose:   Small helper module designed to load a program's JSON-based
            config file.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:
    To load a program's JSON-based config file::

        >>> from utils4 import config

        >>> cfg = config.loadconfig()
        >>> my_param = cfg['my_param']

"""

import os
import sys
import json
from utils4.dict2obj import Dict2Obj


def loadconfig(filename: str='config.json', return_as_obj: bool=False):
    """Load a program's JSON config file and return it as a dict or object.

    Args:
        filename (str, optional): File name or (preferably) the
            **explicit** full file path path of the JSON config file to
            be loaded. Defaults to 'config.json'.
        return_as_object (bool, optional): If True, the dictionary is
            converted into an object, where the dictionary key/values
            are object attribute/values. Defaults to False.

    :Design:
        By default, this function will search the program's directory
        for a file named ``config.json``.  If the config file lives
        somewhere else, or you're using an IDE to develop, the safest
        option is to **explicitly define the path to the config file**.

        If a path is found in the passed parameter, this path is used,
        and the function does not have to try and work out where the
        config file lives.

        The ``return_as_obj`` parameter tells the function to convert
        and return the JSON file into an object, rather than a
        dictionary. This enables you to access the values from object
        attributes, rather than from dictionary keys.  See use option 2.

    :Assumptions:
        * The config file is a JSON file.
        * The config file lives in the program directory.

    :Examples:

        Option 1: Return the config file as a **dict**::

            >>> from utils4 import config

            >>> cfg = config.loadconfig()
            >>> my_param = cfg['my_param']


        Option 2: Return the config file as an **object**::

            >>> from utils4 import config

            >>> cfg = config.loadconfig(return_as_object=True)
            >>> my_param = cfg.my_param

    """
    # Filename only.
    if os.path.dirname(filename) == '':
        progdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        path_base = progdir if sys.argv[0] != '' else os.getcwd()
        fullpath = os.path.join(path_base, filename)
    # Full path.
    else:
        fullpath = filename
    if _file_exists(fullpath=fullpath):
        if return_as_obj:
            return Dict2Obj(source='json', filepath=fullpath)
        return _fromjson(filepath=fullpath)
    return None  # pragma: nocover  (unreachable due to raised IOError)

def _file_exists(fullpath: str) -> bool:
    """Test if the requested config file exists.

    Args:
        fullpath (str): Full path to the file being tested.

    Raises:
        IOError: If the file does not exist.

    Returns:
        bool: True of the file exists, otherwise False.

    """
    exists = os.path.exists(fullpath)
    if not exists:
        raise IOError(f'The config file ({fullpath}) could not be found.')
    return exists

def _fromjson(filepath: str) -> dict:
    """Extract values from the JSON file.

    Args:
        filepath (str): Full path to the file to be read.

    Returns:
        dict: JSON file content as a dictionary.

    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
