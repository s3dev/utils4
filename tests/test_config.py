#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``config`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import os
import pickle
import shutil
from base import TestBase
from testlibs import msgs
from testlibs.utilities import utilities
from utils4 import config


class TestConfig(TestBase):
    """Testing class used to test the ``config`` module."""

    _P_CONFIG = os.path.join(TestBase._DIR_RESRC, 'test_config.json')
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run these statements on test startup."""
        msgs.startoftest.startoftest(module_name='config')

    def test01__loadconfig_dict(self):
        """Test the ``loadconfig`` method, returning a ``dict``.

        :Test:
            - Verify the loaded ``test_config.json`` file matched the
              expectation.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_config__test1.p')
        test = config.loadconfig(self._P_CONFIG, return_as_obj=False)
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test01__loadconfig_dict_fname_only(self):
        """Test the ``loadconfig`` method, using *filename only*.

        :Test:
            - Verify the loaded ``config.json`` file matched the
              expectation.

        """
        shutil.copy(src=self._P_CONFIG, dst='./config.json')
        fname = os.path.join(self._DIR_RESRC, 'test_config__test1.p')
        test = config.loadconfig(filename='config.json', return_as_obj=False)
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)
        os.remove(path='./config.json')

    def test02__loadconfig_obj(self):
        """Test the ``loadconfig`` method, returning an ``object``.

        :Test:
            - Verify the objects created from the loaded
              ``test_config.json`` file match the expectation.

        """
        fname = os.path.join(self._DIR_RESRC, 'test_config__test2.p')
        test = config.loadconfig(filename=self._P_CONFIG, return_as_obj=True)
        with open(fname, 'rb') as f:
            exp = pickle.load(f)
        keys = [i for i in vars(test) if not i.startswith('_')]
        # Test each expected object key against the object read by the loadconfig method.
        for k in keys:
            utilities.assert_true_pyiter(expected=exp[k],
                                         test=getattr(test, k),
                                         msg=self._MSG1)

    def test03__loadconfig__file_not_exist(self):
        """Test the ``loadconfig`` method, with a non-existant file.

        :Test:
            - Verify the ``loadconfig`` method raises an IOError if the
              requested config file does not exist.

        """
        with self.assertRaises(IOError):
            config.loadconfig(filename='doesnotexist.txt')
