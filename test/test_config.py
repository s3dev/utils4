'''------------------------------------------------------------------------------------------------
Program:    test_config
Purpose:    Unit test for utils.config

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
12.03.18    J. Berendt      1.2.0       Added test for dict2obj class using the return_as_obj 
                                        parameter in loadconfig().
                                        Added docstrings to test methods.
                                        Ordered test methods alphabetically, as this is how they 
                                        are run.
------------------------------------------------------------------------------------------------'''

import os
import unittest

import utils3
from utils3 import utils as u
from utils3 import config


class TestConfig(unittest.TestCase):

    #CLASS VARIABLES
    _path = 'c:/temp/'
    _file = 'config_test.json'
    _config_dict = {'path':'c:/temp/', 'file':'config_test.json'}

    def setUp(self):
        """Create the temp JSON files for testing."""
        #CREATE JSON FILE IN SPECIFIC LOCATION
        u.json_write(dictionary=self._config_dict, filepath=os.path.join(self._path, self._file))
        #CREATE JSON FILE IN CWD
        u.json_write(dictionary=self._config_dict, filepath=self._file)


    def tearDown(self):
        """Delete the temp JSON config files."""
        #DELETE TEST CONFIG FROM LOCATION
        os.remove(os.path.join(self._path, self._file))
        #DELETE TEST CONFIG FROM CWD
        os.remove(self._file)


    def test_config_defaults(self):
        """
        Test the 'CWD' config file using the _test_general() function.
        """
        #PULL IN CONFIG
        conf = config.loadconfig(filename=self._file)
        #RUN TESTS
        self.assertTrue(self._test_general(conf))
        
        
    def test_config_fullpath(self):
        """
        Test the 'defined path' config file using the _test_general()
        function.
        """
        #PULL IN CONFIG
        conf = config.loadconfig(filename=os.path.join(self._path, self._file))
        #RUN TESTS
        self.assertTrue(self._test_general(conf))

        
    def test_dict2obj(self):
        """Test the loadconfig() return_as_obj parameter."""
        # READ CONFIG
        cfg = config.loadconfig(filename=os.path.join(self._path, self._file), return_as_obj=True)
        # TEST DATA TYPE
        self.assertTrue(isinstance(cfg, utils3.dict2obj.Dict2Obj))
        # TEST CONTENTS
        self.assertTrue(cfg.path == self._path)
        self.assertTrue(cfg.file == self._file)

    def _test_general(self, conf):
        """
        Perform general tests on the JSON config files, and return a
        boolean result.
        """
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
