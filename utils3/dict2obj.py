"""------------------------------------------------------------------------------------------------
Module:     dict2obj
Platform:   Linux / Windows
Py Ver:     2.7
Purpose:    Class module used to convert a dictionary or JSON file into a class object.

Developer:  J. Berendt
Email:      jeremy.berendt@73rdstreetdevelopment.co.uk

Comments:   Basic concept attribution: https://stackoverflow.com/a/1639197/6340496

Use:        > Refer to help(Dict2Obj)
            >

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
07.02.18    J. Berendt      0.1.0       Written  pylint (10/10)
08.03.18    J. Berendt      0.2.0       Incorporated into the utils3 package for use with the
                                        config.loadconfig() function.
                                        Updated to test value passed to the 'source' parameter.
                                        Updated to work with Py3.
                                        Minor docstring updates.
------------------------------------------------------------------------------------------------"""

import os
import json

# ALLOW SMALL CLASS
# pylint: disable=too-few-public-methods


class Dict2Obj(object):
    """
    Create a Python object from a standard dictionary, or JSON file.

    A Python object is created from the passed dictionary or JSON file,
    where each key/value pair is turned into an attribute/value pair
    of the object.

    This can be useful when loading a config file into memory, as you
    can then access it like an object, rather than a dictionary.
    """

    def __init__(self, dictionary=None, source='dict', filepath=None):
        """
        Transform a Python dictionary into object attributes.

        The dictionary may be either passed in directly, or loaded from
        a JSON file.

        PARAMETERS:
        - dictionary
        A standard Python dictionary where all key/value pairs will be
        converted into an object.
        - source (default 'dict')
        This is the source of the dictionary.  Valid strings are:
            - 'dict'
            - 'json'
            Where 'dict' is a standard Python dictionary, and 'json' uses a
            JSON file as the dictionary source.
        - filepath
        Path to the JSON file to be used.

        USE:
        > from dict2obj import Dict2Obj
        > d = dict(a=1, b=2, title='This is a title.')
        > my_obj = Dict2Obj(dictionary=d)
        > print my_obj.title
        > This is a title.
        """

        self._dictionary = dictionary
        self._source = source
        self._filepath = filepath

        # VALIDATE PARAMETERS
        if self._validate(source=self._source, filepath=self._filepath):

            # TEST SOURCE OF DICT
            if self._source.lower() == 'json':
                # READ FROM JSON FILE
                dict_ = self._read_json(filepath=self._filepath)
            else:
                # CREATE OBJECT FROM PASSED DICTIONARY
                dict_ = self._dictionary

            # LOOP THROUGH THE DICT AND SET CLASS ATTRIBUTES
            for k, v in dict_.items(): setattr(self, k, v)


    # ------------------------------------------------------------------
    def _validate(self, source, filepath):
        """Run all validation functions."""
        success = self._validate_source_value(source=source)
        if success: success = self._validate_source(source=source, filepath=filepath)
        if success: success = self._validate_fileexists(source=source, filepath=filepath)
        return success

    @staticmethod
    def _validate_fileexists(source, filepath):
        """Test the file exists, if the source is JSON."""
        success = False
        # ONLY TEST IF SOURCE IS JSON
        if source.lower() == 'json':
            if all([source.lower() == 'json', os.path.exists(filepath)]):
                success = True
            else:
                print('The file provided does not exist:\n(%s)' % (filepath))
        else:
            success = True
        return success

    @staticmethod
    def _validate_source(source, filepath):
        """Test the source of the dictionary is valid."""
        success = False
        if all([source.lower() == 'json', filepath is None]):
            print('A file path must be provided for the JSON file.')
        else:
            success = True
        return success

    @staticmethod
    def _validate_source_value(source):
        """Validate the value passed to the source parameter."""
        source_values = ['dict', 'json']
        success = False
        if source in ['dict', 'json']:
            success = True
        else:
            print('The source provided (\'%s\') is invalid.  Valid options are: %s.' %
                  (source, source_values))
        return success

    @staticmethod
    def _read_json(filepath):
        "Read values from json and convert to dictionary."
        return json.loads(open(filepath).read())
