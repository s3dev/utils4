#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``dict2obj`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import json
import os
import shutil
from string import punctuation
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4.dict2obj import Dict2Obj


class TestDict2Obj(TestBase):
    """Testing class used to test the ``dict2obj`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    def setUp(self):
        """Create a translation for dictionary keys."""
        trans = str.maketrans({p: '' for p in punctuation})
        trans.update({32: '_'})
        self._trans = trans

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='dict2obj')

    @property
    def dataset_01_valid_dict(self):
        """Dataset containing a valid ``dict``.

        This dataset intentionally uses keys with spaces and punctuation
        characters to ensure the library handles these correctly.

        """
        d = {'A Brief History of Time': 'Stephen Hawking',
             'The Art of Computer Programming, Vol 3': 'Donald Knuth',
             'Schrodinger\'s Kittens': 'John Gribbin',
             'The Science of Superman': 'Mark Wolverton',
             'Hitchhiker\'s Guide to the Galaxy': 'Douglas Adams'}
        return d

    @property
    def dataset_02_valid_json_filepath(self):
        """Full path to a valid JSON file.

        If the file does not exist, it is created automatically based on
        the value of the :attr:`~dataset_01_valid_dict` property.

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_dict2obj__dataset02.json')
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(self.dataset_01_valid_dict, f)
        return fpath

    @property
    def dataset_03_nested_dict(self):
        """Dataset containing a valid, but nested ``dict``."""
        d = {'Science': {'Hawking': ['A Brief History of Time',
                                     'The Universe in a Nutshell'],
                         'Gribbin': ['In Search of Schrodingers Cat',
                                     'Schrodingers Kittens']},
             'Comedy': {'Adams': ['The Hitchhikers Guide to the Galaxy',
                                  'The Restaurant at the End of the Universe',
                                  'Life, the Universe and Everything']}}
        return d

    @property
    def dataset_04_nested_json_filepath(self):
        """Full path to a valid nested JSON file.

        If the file does not exist, it is created automatically based on
        the value of the :attr:`~dataset_03_nested_dict` property.

        """
        fpath = os.path.join(self._DIR_RESRC, 'test_dict2obj__dataset04.json')
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(self.dataset_03_nested_dict, f)
        return fpath

    @property
    def dataset_05_invalid_dict(self):
        """Dataset containing an  invalid ``dict``.

        This dataset intentionally uses an invalid structure to ensure the
        library handles these correctly.

        """
        d = [{'A Brief History of Time': 'Stephen Hawking',
             'The Art of Computer Programming, Vol 3': 'Donald Knuth',
             'Schrodinger\'s Kittens': 'John Gribbin',
             'The Science of Superman': 'Mark Wolverton',
             'Hitchhiker\'s Guide to the Galaxy': 'Douglas Adams'}]
        return d

    @property
    def dataset_06_invalid_dict_key(self):
        """Dataset containing ``dict`` with a non-string key."""
        d = {'1a': 'value'}
        return d

    def test01__valid_dict(self):
        """Test the logic for converting a ``dict`` to an object.

        :Test:
            - An object is created using a valid dict.
            - The source dataset is translated to remove/replace any special
              characters.
            - Each key/value pair of the source dataset is iterated and tested
              using the object's ``__getattribute__`` method to verify the
              value is as expected.
            - If the expected and test values match, the test passes,
              otherwise it fails.

        """
        obj = Dict2Obj(dictionary=self.dataset_01_valid_dict)
        dict_t = self._translate_keys(dict_=self.dataset_01_valid_dict)
        for idx, (k, v) in enumerate(dict_t.items()):
            with self.subTest(i=idx):
                utilities.assert_true(expected=v, test=getattr(obj, k), msg=self._MSG1)

    def test02__valid_json_file(self):
        """Test the logic for converting a JSON file's contents to an object.

        :Test:
            - An object is created using a valid dict.
            - The source dataset is translated to remove/replace any special
              characters.
            - Each key/value pair of the source dataset is iterated and tested
              using the object's ``__getattribute__`` method to verify the
              value is as expected.
            - If the expected and test values match, the test passes,
              otherwise it fails.

        """
        obj = Dict2Obj(source='json', filepath=self.dataset_02_valid_json_filepath)
        dict_t = self._translate_keys(dict_=self.dataset_01_valid_dict)
        for idx, (k, v) in enumerate(dict_t.items()):
            with self.subTest(i=idx):
                utilities.assert_true(expected=v, test=getattr(obj, k), msg=self._MSG1)

    def test03__nested_dict(self):
        """Test the logic for converting a nested ``dict`` to an object.

        :Test:
            - An object is created using a valid nested dict.
            - The source dataset is translated to remove/replace any special
              characters.
            - Each key/value pair of the source dataset is iterated and tested
              using the object's ``__getattribute__`` method to verify the
              value is as expected.
            - If the expected and test values match, the test passes,
              otherwise it fails.

        """
        obj = Dict2Obj(dictionary=self.dataset_03_nested_dict)
        dict_t = self._translate_keys(dict_=self.dataset_03_nested_dict)
        for idx, (k, v) in enumerate(dict_t.items()):
            with self.subTest(i=idx):
                utilities.assert_true(expected=v, test=getattr(obj, k), msg=self._MSG1)

    def test04__nested_json_file(self):
        """Test the logic for converting a nested JSON file's contents to an
        object.

        :Test:
            - An object is created using a valid nestd JSON file.
            - The source dataset is translated to remove/replace any special
              characters.
            - Each key/value pair of the source dataset is iterated and tested
              using the object's ``__getattribute__`` method to verify the
              value is as expected.
            - If the expected and test values match, the test passes,
              otherwise it fails.

        """
        obj = Dict2Obj(source='json', filepath=self.dataset_04_nested_json_filepath)
        dict_t = self._translate_keys(dict_=self.dataset_03_nested_dict)
        for idx, (k, v) in enumerate(dict_t.items()):
            with self.subTest(i=idx):
                utilities.assert_true(expected=v, test=getattr(obj, k), msg=self._MSG1)

    def test05__json_no_filepath(self):
        """Test the library correctly detects a 'json' source with no filepath.

        :Test:
            - Verify passing a source of 'json' with no filepath raises a
              ValueError.

        """
        self.assertRaises(ValueError, self._errortest05__json_no_filepath)

    def test06__json_bad_file_ext(self):
        """Test the library correctly detects a non-json file extension.

        :Test:
            - Verify passing a source of 'json' with a filepath which does not
              have a '.json' file extension raises a ValueError.

        """
        self.assertRaises(ValueError, self._errortest06__json_bad_file_ext)

    def test07__json_bad_filepath(self):
        """Test the library correctly detects a JSON file which does not exist.

        :Test:
            - Verify passing a source of 'json' with a non-existant filepath
              raises a ValueError.

        """
        self.assertRaises(ValueError, self._errortest07__json_bad_filepath)

    def test08__not_a_dict(self):
        """Test the library correctly detects a the passed object is not a dict.

        :Test:
            - Verify passing a source of 'dict' with a non-dict object raises
            a TypeError.

        """
        self.assertRaises(TypeError, self._errortest08__not_a_dict)

    def test09__invalid_dict_key(self):
        """Test the library correctly detects a dict with an invalid key.

        :Test:
            - Verify passing a source of 'dict' with an invalid key raises a
            TypeError.

        """
        self.assertRaises(TypeError, self._errortest09__invalid_dict_key)

    def test10__invalid_source(self):
        """Test the library correctly detects an invalid source.

        :Test:
            - Verify passing a source of 'bob' raises a ValueError.

        """
        self.assertRaises(ValueError, self._errortest10__invalid_source)

    @staticmethod
    def _errortest05__json_no_filepath():
        """Test method to raise a ValueError."""
        Dict2Obj(source='json')

    def _errortest06__json_bad_file_ext(self):
        """Test method to raise a ValueError.

        This method copies a valid JSON file and renames the copy to have a
        ``.csv`` extension. This enables the code path to be tested where the
        file exists, but the extension is invalid.

        """
        # Create a file that exists, with a CSV file extension.
        src = self.dataset_02_valid_json_filepath
        dst = f'{os.path.splitext(src)[0]}.csv'
        shutil.copy(src=src, dst=dst)
        Dict2Obj(source='json', filepath=dst)

    @staticmethod
    def _errortest07__json_bad_filepath():
        """Test method to raise a ValueError."""
        Dict2Obj(source='json', filepath='a/bad/path/file.json')

    def _errortest08__not_a_dict(self):
        """Test method to raise a TypeError."""
        Dict2Obj(dictionary=self.dataset_05_invalid_dict, source='dict')

    def _errortest09__invalid_dict_key(self):
        """Test method to raise a TypeError."""
        Dict2Obj(dictionary=self.dataset_06_invalid_dict_key, source='dict')

    @staticmethod
    def _errortest10__invalid_source():
        """Test method to raise a ValueError."""
        Dict2Obj(dictionary={}, source='bob')

    def _translate_keys(self, dict_: dict) -> dict:
        """Remove/replace any special characters from the dict's keys.

        Args:
            dict_ (dict): Dictionary for which the keys are translated.

        Returns:
            dict: A new ``dict`` object with translated keys.

        """
        return {k.translate(self._trans): v for k, v in dict_.items()}
