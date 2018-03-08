"""------------------------------------------------------------------------------------------------
Program:    config
Purpose:    Small helper module designed to load a program's config file.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        > from utils3 import config
            > cfg = config.loadconfig()
            > my_param = cfg['my_param']

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
06.03.18    J. Berendt      1.1.0       GENERAL:
                                        Removed devmode parameter from loadconfig() function.
                                        Updated docstring for loadconfig().  pylint (10/10)
08.03.18    J. Berendt      1.2.0       Added the return_as_object parameter to the loadconfig()
                                        function; which is used to convert the key/value dictionary
                                        pairs to object attribute/value pairs.  pylint (10/10)
------------------------------------------------------------------------------------------------"""

import os
import sys
import json

from utils3.dict2obj import Dict2Obj


# ----------------------------------------------------------------------
def loadconfig(filename='config.json', return_as_obj=False):
    """
    Load a program's JSON config file and return it as a dictionary or
    an object.

    DESIGN:
    By default, this function will search the program's directory for
    a file named 'config.json'.  If the config file lives somewhere
    else, or you're using an IDE to develop, the safest option is to
    **explicitly define the path to the config file**.

    If a path is found in the passed parameter, this path is used, and
    the function does not have to try and work out where the config file
    lives.

    The 'return_as_obj' parameter tells the function to convert and
    return the JSON file into an object, rather than a dictionary.
    This enables you to access the values from object attributes,
    rather than from dictionary keys.  See USE OPTION 2.

    PARAMETERS:
    - filename
    File name or (preferably) the **explicit full path** of the
    config (JSON) file to be loaded.
    - return_as_object (default=False)
    If True, the dictionary is converted into an object, where the
    dictionary key/values are object attribute/values.

    PREREQUESITES / ASSUMPTIONS:
    - The config file is a JSON file
    - The config file lives in the program directory

    USE OPTION 1:
    > from utils3 import config
    > cfg = config.loadconfig()
    > my_param = cfg['my_param']

    USE OPTION 2:
    > from utils3 import config
    > cfg = config.loadconfig(return_as_object=True)
    > my_param = cfg.my_param
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


# ----------------------------------------------------------------------
def _file_exists(fullpath):
    """Return a boolean value if the file exists."""

    # TEST IF THE FILE EXISTS
    if os.path.exists(fullpath):
        # LOAD CONFIG FILE
        return True
    else:
        # USER NOTIFICATION
        raise UserWarning('The config file (%s) could not be found.' % (fullpath))


# ----------------------------------------------------------------------
def _fromjson(filepath):
    """Return JSON file content as a dictionary."""

    # OPEN AND READ CONFIG FILE >> RETURN AS DICT
    with open(filepath, 'r') as config: return json.load(config)
