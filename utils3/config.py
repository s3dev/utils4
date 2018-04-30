"""
:Purpose:   Small helper module designed to load a program's config file.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
    To load a program's config file::

        from utils3 import config

        cfg = config.loadconfig()
        my_param = cfg['my_param']

"""

import os
import sys
import json
from utils3.dict2obj import Dict2Obj

def loadconfig(filename='config.json', return_as_obj=False):
    """
    Load a program's JSON config file and return it as a dictionary or
    an object.

    Args:
        filename (str): File name or (preferably) the **explicit** full
            path of the config (JSON) file to be loaded.
        return_as_object (bool): If True, the dictionary is converted
            into an object, where the dictionary key/values are object
            attribute/values.

    :Design:
        By default, this function will search the program's directory
        for a file named 'config.json'.  If the config file lives
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
        * The config file is a JSON file
        * The config file lives in the program directory

    :Example:
        Option 1: return the config file as a **dictionary**::

            from utils3 import config

            cfg = config.loadconfig()
            my_param = cfg['my_param']

        Option 2: return the config file as an **object**::

            from utils3 import config

            cfg = config.loadconfig(return_as_object=True)
            my_param = cfg.my_param

    """
    # TEST FOR FULLPATH OR FILENAME ONLY
    if os.path.dirname(filename) == '':
        # USE THE PROGRAM'S DIRECTORY AS ROOT FOR THE CONFIG FILE
        progdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        # IF THE PROGRAM DIR IS NOT AVAILABLE (NOT USED) USE CWD
        curdir = os.getcwd()

        # TEST PROGRAM DIR >> USE CWD IF NO PROGRAM DIR
        path_base = progdir if sys.argv[0] != '' else curdir

        # BUILD FULL PATH TO CONFIG FILE
        fullpath = os.path.join(path_base, filename)

    else:
        # ASSIGN PASSED FULL PATH
        fullpath = filename

    # TEST FILE EXISTS AND TYPE OF RETURN REQUESTED
    if all([_file_exists(fullpath=fullpath), return_as_obj is False]):
        # RETURN DICTIONARY
        to_return = _fromjson(filepath=fullpath)
    elif all([_file_exists(fullpath=fullpath), return_as_obj is True]):
        # RETURN OBJECT
        to_return = Dict2Obj(source='json', filepath=fullpath)

    return to_return


def _file_exists(fullpath) -> bool:
    """Test if the requested config file exists.

    Returns:
        True of the file exists, otherwise False.

    """
    # TEST IF THE FILE EXISTS
    if os.path.exists(fullpath):
        # LOAD CONFIG FILE
        return True
    else:
        # USER NOTIFICATION
        raise UserWarning('The config file (%s) could not be found.' % (fullpath))


def _fromjson(filepath) -> dict:
    """Extract values from the JSON file.

    Returns:
        JSON file content as a dictionary.

    """
    # OPEN AND READ CONFIG FILE >> RETURN AS DICT
    with open(filepath, 'r') as config: return json.load(config)
