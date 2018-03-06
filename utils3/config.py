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
------------------------------------------------------------------------------------------------"""

import os
import sys
import json


# ----------------------------------------------------------------------
def loadconfig(filename='config.json'):
    """
    Load a program's JSON config file and return as a dictionary.

    DESIGN:
    By default, this function will search the program's directory for
    a file named 'config.json'.  If the config file lives somewhere
    else, or you're using an IDE to develop, the safest option is to
    **explicitly define the path to the config file**.

    If a path is found in the passed parameter, this path is used, and
    the function does not have to try and work out where the config file
    lives.

    PARAMETERS:
    - filename
    File name or the **explicit full path** of the config (JSON) file
    to be loaded.

    PREREQUESITES / ASSUMPTIONS:
    - The config file is a JSON file
    - The config file lives in the program directory

    USE:
    > from utils3 import config
    > cfg = config.loadconfig()
    > my_param = cfg['my_param']
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

    # TEST IF THE FILE EXISTS
    if os.path.exists(fullpath):
        # LOAD CONFIG FILE
        return _fromjson(filepath=fullpath)
    else:
        # USER NOTIFICATION
        raise UserWarning('The config file (%s) could not be found.' % (fullpath))


# ----------------------------------------------------------------------
def _fromjson(filepath):
    """Return JSON file content as a dictionary."""

    # OPEN AND READ CONFIG FILE >> RETURN AS DICT
    with open(filepath, 'r') as config: return json.load(config)
