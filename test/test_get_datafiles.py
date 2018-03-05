'''------------------------------------------------------------------------------------------------
Program:    test_get_datafiles
Purpose:    Unit test for get_datafiles.py

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        > cd /package_root/test
            > python test_log.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
------------------------------------------------------------------------------------------------'''

# BUILT-IN IMPORTS
import os
import unittest

# SELF-DEPENDENT IMPORTS
import utils3.get_datafiles as gdf


class TestGetDataFiles(unittest.TestCase):

    def test_get_datafiles(self):

        #BUILD STRING FOR ROOT
        search_root = os.path.realpath(os.path.dirname(__file__))

        #GET LIST OF FILES
        files = gdf.get_datafiles(pkg_dir=search_root, exts=['.test'])

        #EXTRACT UI CONFIG FILE FROM LIST
        ui_cfg = [os.path.split(fname[1][0])[1] for fname in files
                  if os.path.split(fname[1][0])[1] == 'user_interface_config.test']

        #TEST FOR EXPECTED FILE
        self.assertEqual(ui_cfg[0], 'user_interface_config.test')


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
