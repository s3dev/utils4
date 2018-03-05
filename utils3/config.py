"""------------------------------------------------------------------------------------------------
Program:    config
Purpose:    Small helper program designed to load a program's config file.

Dependents: os
            sys
            json

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        >>> import utils3.config as config
            >>> global CFG
            >>> CFG = config.loadconfig()
            >>> my_param = CFG['my_param']

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
------------------------------------------------------------------------------------------------"""

# BUILT-IN IMPORTS
import os
import sys
import json


# ----------------------------------------------------------------------
def loadconfig(filename='config.json', devmode=False):
    """
    Setup for loading a JSON file, then read and return JSON config
    file content as a dictionary.

    DESIGN:
    The devmode parameter can be used if you are programming through an
    IDE which defaults the sys.argv[0] value to the cwd of the IDE,
    rather than from where the program is actually being run.
    It just makes design and debugging easier.

    PREREQUESITES / ASSUMPTIONS:
    - The config file is a JSON file
    - The config file lives in the program directory

    USE:
    > import utils3.config as config
    > c = config.loadconfig()

    > param_value = c['someparam_name']
    """

    # TEST IF FULL PATH OR ONLY FILENAME WAS PASSED
    if os.path.dirname(filename) == '':

        # TEST PROGRAM MODE
        if devmode:

            # STORE PROGRAM DIRECTORY
            path_base = os.getcwd()

        else:

            # ASSIGN DIRECTORIES
            # USE THE PROGRAM'S DIRECTORY AS ROOT FOR THE CONFIG FILE
            progdir = os.path.dirname(os.path.realpath(sys.argv[0]))
            # IF THE PROGRAM DIR IS NOT AVAILABLE (NOT USED) USE CWD
            curdir = os.getcwd()

            # TEST PROGRAM DIR >> USE CWD IF NO PROGRAM DIR
            path_base = progdir if sys.argv[0] != '' else curdir

        # CONSOLIDATE PATH AND FILENAME
        fullpath = os.path.join(path_base, filename)

    else:

        # ASSIGN PASSED PATH/FILENAME TO TESTED VARIABLE
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
