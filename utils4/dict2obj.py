# -*- coding: utf-8 -*-
"""
:Purpose:   This class module is used to convert a Python dictionary (``dict``)
            or JSON file into a object - where the dictionary's key/value
            pairs become object attribute/value pairs.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  Basic concept `attribution`_.


.. _attribution: https://stackoverflow.com/a/1639197/6340496

"""
# pylint: disable=too-few-public-methods

import os
import json
from string import punctuation


class Dict2Obj:
    """Create a Python object from a standard Python dictionary, or JSON file.

    Args:
        dictionary (dict, optional): A standard Python dictionary where all
            key/value pairs will be converted into an object. Defaults to None.
        source (str, optional): Source for the conversion. Defaults to 'dict'.

            - 'dict': a standard Python dictionary
            - 'json': uses content from a JSON file

        filepath (str, optional): Full file path to the JSON file to be used.
            Defaults to None.

    :Design:
        A Python object is created from the passed dictionary (or JSON
        file), where each of the dictionary's key/value pairs is turned
        into an object attribute/value pair.

    :Note:

        #. The dictionary or JSON file *should* be in a flat format. If a
           nested source is provided, the value of the object will be the
           nested structure. In other the object will *not* be nested.
        #. This can be useful when loading a JSON config file into
           memory, as you can then access it like an object, rather than a
           dictionary.

    :Example:
        To convert a dictionary into an object::

            >>> from utils4.dict2obj import Dict2Obj

            >>> d = dict(a=1, b=2, title='This is a title.')
            >>> obj = Dict2Obj(dictionary=d)
            >>> print(obj.title)

            This is a title.

    """

    _VALID = ['dict', 'json']

    def __init__(self, *, dictionary=None, source='dict', filepath=None):
        """Class initialiser."""
        self._dict = dictionary
        self._src = source
        self._fpath = filepath
        self._create()

    def _create(self):
        """Validate and create the object.

        Raises:
            TypeError: If a key is not a string, or is a string yet begins
                with any type other than a string..

        """
        if self._validate():
            if self._src.lower() == 'json':
                # Read from json file.
                dict_ = self._read_json()
            else:
                # Create object from passed dictionary.
                dict_ = self._dict
            # Create replacement translation.
            trans = str.maketrans({p: '' for p in punctuation})
            trans.update({32: '_'})
            # Loop through the dict and set class attributes.
            for k, v in dict_.items():
                if isinstance(k, str) & (not str(k)[0].isdigit()):
                    k = k.translate(trans)
                    setattr(self, k, v)
                else:
                    raise TypeError(f'Key error, string expected. Received {type(k)} for key: {k}.')

    def _read_json(self) -> dict:
        """Read values from a JSON file into a dictionary.

        Returns:
            dict: A dictionary containing the JSON data.

        """
        with open(self._fpath, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    def _validate(self) -> bool:
        """Run the following validation tests:

            - The ``source`` value is valid.
            - If 'json' source, a file path is provided.
            - If 'json' source, the provided file path exists.

        Returns:
            bool: True if **all** tests pass, otherwise False.

        """
        # pylint: disable=multiple-statements
        s = self._validate_source_value()
        if s: s = self._validate_source()
        if s: s = self._validate_is_dict()
        if s: s = self._validate_fileexists()
        return s

    def _validate_fileexists(self) -> bool:
        """Validation test: If a 'json' source, test the file path exists.

        Raises:
            ValueError: If the passed filepath is not a '.json' extension.
            ValueError: If the passed filepath does not exist.

        Returns:
            bool: True if the source is 'dict'; or if source is 'json' and
            the file exists, otherwise False.

        """
        success = False
        if self._src.lower() == 'json':
            if os.path.exists(self._fpath):
                if os.path.splitext(self._fpath)[1].lower() == '.json':
                    success = True
                else:
                    raise ValueError(f'The file provided must be a JSON file:\n- {self._fpath}')
            else:
                raise ValueError(f'The file provided does not exist:\n- {self._fpath}')
        else:
            success = True
        return success

    def _validate_is_dict(self) -> bool:
        """Validation test: Verify the object is a ``dict``.

        Raises:
            TypeError: If the passed object is not a ``dict``.

        Returns:
            bool: True if the passed object is a ``dict``.

        """
        if self._src == 'dict':
            if not isinstance(self._dict, dict):
                raise TypeError(f'Unexpected type. Expected a dict, received a {type(self._dict)}.')
        return True

    def _validate_source(self) -> bool:
        """Validation test: If a 'json' source, test a file path is provided.

        Raises:
            ValueError: If the source is 'json' and a filepath is not provided.

        Returns:
            bool: True if the source is 'dict'; or if source is 'json' and a
            file path is provided.

        """
        if all([self._src.lower() == 'json', not self._fpath]):
            raise ValueError('A file path must be provided for the JSON file.')
        return True

    def _validate_source_value(self) -> bool:
        """Validation test: The value of the ``source`` parameter is valid.

        Raises:
            ValueError: If the source string is invalid.

        Returns:
            bool: True if a valid source.

        """
        if self._src not in self._VALID:
            raise ValueError(f'The source provided ({self._src}) is invalid. '
                             f'Valid options are: {self._VALID}')
        return True
