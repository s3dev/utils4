# -*- coding: utf-8 -*-
"""
:Purpose:   This class module is used to convert a dictionary (or JSON
            file) into a object - where the dictionary's key/value
            pairs become object attributes.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  Basic concept `attribution`_.

.. _attribution: https://stackoverflow.com/a/1639197/6340496

"""

import os
import json

# ALLOW SMALL CLASS
# pylint: disable=too-few-public-methods

class Dict2Obj(object):
    """
    Create a Python object from a standard dictionary, or JSON file.

    Args:
        dictionary (dict): A standard Python dictionary where all
            key/value pairs will be converted into an object.
        source (str): Source for the conversion.

            * 'dict': a standard Python dictionary
            * 'json': uses content from a JSON file

        filepath (str): Full file path to the JSON file to be used.

    :Design:
        A Python object is created from the passed dictionary (or JSON
        file), where each of the dictionary's key/value pairs is turned
        into an object attribute/value pair.

    Note:
        1) The dictionary or JSON file **must be in a flat format**.
        In other words, functionality **does not support** nested
        dictionaries and/or lists.

        2) This can be useful when loading a JSON config file into
        memory, as you can then access it like an object, rather than a
        dictionary.

    :Example:
        To convert a dictionary into an object::

            from utils3.dict2obj import Dict2Obj

            # A SAMPLE DICTIONARY
            d = dict(a=1, b=2, title='This is a title.')
            # CONVERT IT
            my_obj = Dict2Obj(dictionary=d)
            # TEST IT
            print(my_obj.title)
            > This is a title.

    """
    def __init__(self, dictionary=None, source='dict', filepath=None):
        """Class initialiser."""
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

    def _validate(self, source, filepath) -> bool:
        """
        Run the following validation tests:

            * The 'source' value is valid
            * If 'json' source, a file path is provided
            * If 'json' source, the provided file path exists

        Args:
            source (str): Source for the conversion.
                (i.e. 'dict' or 'json')
            filepath (str): Full file path to the JSON file.

        Returns:
            True if **all** tests pass, otherwise False.

        """
        success = self._validate_source_value(source=source)
        if success: success = self._validate_source(source=source, filepath=filepath)
        if success: success = self._validate_fileexists(source=source, filepath=filepath)
        return success

    @staticmethod
    def _validate_fileexists(source, filepath) -> bool:
        """
        Validation test: If a 'json' source, test the file path exists.

        Args:
            source (str): Source for the conversion.
                (i.e. 'dict' or 'json')
            filepath (str): Full file path to the JSON file.

        Returns:
            True if the source is 'dict'; or if source is 'json' and
            the file exists, otherwise False.

        """
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
    def _validate_source(source, filepath) -> bool:
        """
        Validation test: If a 'json' source, test a file path is
        provided.

        Args:
            source (str): Source for the conversion.
                (i.e. 'dict' or 'json')
            filepath (str): Full file path to the JSON file.

        Returns:
            True if the source is 'dict'; or if source is 'json' and a
            file path is provided, otherwise False.

        """
        success = False
        if all([source.lower() == 'json', filepath is None]):
            print('A file path must be provided for the JSON file.')
        else:
            success = True
        return success

    @staticmethod
    def _validate_source_value(source) -> bool:
        """
        Validation test: The value of the ``source`` parameter is valid.

        Args:
            source (str): Source for the conversion.
                (i.e. 'dict' or 'json')

        Returns:
            True if a valid source, otherwise False.

        """
        source_values = ['dict', 'json']
        success = False
        if source in ['dict', 'json']:
            success = True
        else:
            print('The source provided (\'%s\') is invalid.  Valid options are: %s.' %
                  (source, source_values))
        return success

    @staticmethod
    def _read_json(filepath) -> dict:
        """
        Read values from a JSON file into a dictionary.

        Args:
            filepath (str): Full file path to the JSON file.

        Returns:
            A dictionary containing the JSON data.

        """
        with open(filepath) as f:
            data = json.loads(f.read())
        return data
