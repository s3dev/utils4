'''------------------------------------------------------------------------------------------------
Program:    test_config
Purpose:    Unit test for utils.config

Dependents: utils.config

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        > cd /package_root/test
            > python test_config.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
06.03.18    J. Berendt      1.1.0       Updated test to remove the devmode parameter.
------------------------------------------------------------------------------------------------'''

import os
import unittest

from utils3 import utils as u
from utils3 import config


class TestConfig(unittest.TestCase):

    #CLASS VARIABLES
    _path = 'c:/temp/'
    _file = 'config_test.json'
    _config_dict = {'path':'c:/temp/', 'file':'config_test.json'}


    def setUp(self):
        #CREATE JSON FILE IN SPECIFIC LOCATION
        u.json_write(dictionary=self._config_dict, filepath=os.path.join(self._path, self._file))
        #CREATE JSON FILE IN CWD
        u.json_write(dictionary=self._config_dict, filepath=self._file)


    def tearDown(self):
        #DELETE TEST CONFIG FROM LOCATION
        os.remove(os.path.join(self._path, self._file))
        #DELETE TEST CONFIG FROM CWD
        os.remove(self._file)


    #TEST CONFIG FROM DEFINED PATH
    def test_config_fullpath(self):
        #PULL IN CONFIG
        conf = config.loadconfig(filename=os.path.join(self._path, self._file))
        #RUN TESTS
        self.assertTrue(self._test_general(conf))


    #TEST CONFIG FROM CWD
    def test_config_defaults(self):
        #PULL IN CONFIG
        conf = config.loadconfig(filename=self._file)
        #RUN TESTS
        self.assertTrue(self._test_general(conf))


    #GENERAL TESTING FUNCTION
    def _test_general(self, conf):
        results = []
        #TEST: RETURNED OBJECT IS A DICT
        results.append(self.assertTrue(isinstance(conf, dict)))
        #TEST: VALUE
        results.append(self.assertEqual(conf['path'], self._path))
        results.append(self.assertEqual(conf['file'], self._file))
        #TEST IF ANY TESTS FAILED
        passed = True if False not in results else False

        #RETURN RESULTS
        return passed


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
