"""------------------------------------------------------------------------------------------------
Program:    test_utils
Purpose:    Unit testing module for the utils module.

Developer:  J. Berendt
Email:      jeremy.berendt@rolls-royce.com

Comments:   Due to an unknown unit test issue, unidecode cannot be
            tested as decoded characters are not being read by unittest
            correctly.

Use:        >>> python test_utils.py
            >>>

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
05.03.18    J. Berendt      0.0.2       Updated testimport test to close the devnull device handle
                                        automatically after writing to it.
                                        Disabled the 'unclosed file' ResourceWarning for the
                                        test_testimport_false() test; based on Py version.
------------------------------------------------------------------------------------------------"""

# BUILT-IN IMPORTS
import os
import sys
import unittest

# EXTERNAL IMPORTS
import pandas as pd
import six

# SELF-DEPENDENT IMPORTS
import utils3.utils as u


#UNIT TEST CLASS FOR UTILITIES
class TestUtils(unittest.TestCase):

    #CLASS VARIABLES
    _json_path  = 'c:/temp/json_unittest.json'
    _json_dict  = {'key_01':'a', 'key_02':'b', 'key_03':'c', 'key_04':'d'}
    _df_dirty   = pd.DataFrame([['a  ', 'b  ', 'c  '], ['  a', '  b', '  c']],
                               columns=['this is AN a', 'THIS is a_b', 'tHIs is_a C'])
    _df_clean   = pd.DataFrame([['a', 'b', 'c'], ['a', 'b', 'c']],
                               columns=['this_is_an_a', 'this_is_a_b', 'this_is_a_c'])


    def setUp(self):
        pass


    def tearDown(self):
        pass


    #FUNCTION MUST RETURN A CLEANED DATAFRAME
    def test_clean_df(self):
        #CLEAN THE DATAFRAME
        df_cleaned = u.clean_df(self._df_dirty)
        #COMPARE DATAFRAMES
        cols = self._df_clean.columns == df_cleaned.columns
        vals = self._df_clean.values == df_cleaned.values
        #GET RESULTS
        cols_passed = False if False in cols else True
        vals_passed = False if False in vals else True
        #TEST
        self.assertTrue(cols_passed)
        self.assertTrue(vals_passed)


    #FUNCTION MUST RETURN A TRUE VALUE AFTER DIR IS CREATED
    def test_direxists_create_true(self):
        #PATH TO TEST DIR
        dir_path = 'c:/temp/test_dir_1001001'
        #TEST PATH >> NOT EXIST >> CREATE
        self.assertTrue(u.direxists(path=dir_path, create_path=True))
        #DELETE DIR
        os.rmdir(dir_path)


    #FUNCTION MUST RETURN A TRUE VALUE
    def test_direxists_create_false(self):
        #PATH TO TEST DIR
        dir_path = 'c:/temp/test_dir_1373'
        #CREATE DIR
        os.mkdir(dir_path)
        #TEST PATH >> NOT EXIST >> CREATE
        self.assertTrue(u.direxists(path=dir_path, create_path=False))
        #DELETE DIR
        os.rmdir(dir_path)


    #FUNCTION MUST RETURN A TRUE VALUE (FILE IS CREATED AND DELETED)
    def test_fileexists(self):
        #FILE PATH
        file_name = 'c:/temp/myfile_1373.log'
        #CREATE FILE >> CLOSE FILE HANDLE
        fname = open(file_name, 'w')
        fname.close()
        #TEST
        self.assertTrue(u.fileexists(filepath=file_name))
        #DELETE FILE
        os.remove(file_name)


    #FUNCTION MUST RETURN A FORMATTED EXIF DATETIME
    def test_format_exif_date(self):
        #ORIGINAL AND EXPECTED DATE FORMATS
        original = '2017:12:31 00:34:56'
        expected = '20171231003456'
        #TEST
        self.assertEqual(u.format_exif_date(datestring=original), expected)


    #FUNCTION MUST RETURN A LIST OF COLOURS
    def test_getcolormap(self):
        #DEFINED EXPECTED COLOUR LIST
        expected = [u'#67001f', u'#f7f7f7', u'#053061']
        #TEST
        self.assertEqual(u.getcolormap(colormap='RdBu', n=3, dtype='hex', preview=False), expected)


    #FUNCTION MUST RETURN A TRUE VALUE (LIBRARY INSTALLED)
    def test_testimport_true(self):
        #TEST
        self.assertTrue(u.testimport('os'))


    #FUNCTION MUST RETURN A FALSE VALUE (LIBRARY NOT INSTALLED)
    def test_testimport_false(self):
        # DISABLE THE UNCLOSED FILE RESOURCEWARNING
        if six.PY3:
            import warnings
            warnings.simplefilter('ignore', ResourceWarning)
        #SUPPRESS STDOUT (PRINTING FROM FUNCTION)
        with open(os.devnull, 'w') as devnull_:
            save_stdout = sys.stdout
            sys.stdout = devnull_
            try:
                #TEST
                self.assertFalse(u.testimport('some_other_library'))
            finally:
                #RESTORE STDOUT (RE-ENABLE PRINTING)
                sys.stdout = save_stdout


    #METHOD MUST CREATE A JSON FILE, TO BE READ BY json_read()
    #@unittest.skip('')
    def test_json_write(self):
        #CREATE JSON FROM DICT
        u.json_write(dictionary=self._json_dict, filepath=self._json_path)
        #TEST FILE EXISTS
        self.assertTrue(os.path.exists(self._json_path))
        #DELETE FILE
        if os.path.exists(self._json_path): os.remove(self._json_path)


    #FUNCTION MUST READ THE JSON FILE AND RETURN IT AS A DICTIONARY
    #@unittest.skip('')
    def test_json_read(self):
        #CREATE JSON FROM DICT
        u.json_write(dictionary=self._json_dict, filepath=self._json_path)
        #READ JSON
        json_dict = u.json_read(filepath=self._json_path)
        #TEST
        self.assertEqual(self._json_dict, json_dict)
        #DELETE FILE
        if os.path.exists(self._json_path): os.remove(self._json_path)


    #FUNCTION MUST RETURN AN RGBA STRING CONVERTED TO HEX
    #RETURNED HEX MUST NOT CONTAIN AN ALPHA CHANNEL
    def test_rgb2hex_rgb(self):
        #DEFINE RGB(A) LIST
        l_rgba = ['rgba(195, 00, 0, 0)', 'rgba(0, 100, 33, 253)',
                  'rgba(105, 0, 10, 0.75)', 'rgba(65, 125, 50, 1)',
                  'rgba(65, 125, 50, 1.0)', 'rgba(65, 125, 50, 0.25)',
                  'rgba(65, 125, 50, 0.4)']
        #DEFINE HEX LIST
        l_hex = ['#c30000', '#006421',
                 '#69000a', '#417d32',
                 '#417d32', '#417d32',
                 '#417d32']

        #COMPARE RGB AND HEX VALUES FOR EACH PAIR >> STORE RESULT TO LIST
        passed = [u.rgb2hex(rgb_string=r, drop_alpha=True) == h for r, h in zip(l_rgba, l_hex)]

        #UNIT TEST
        self.assertFalse(False in passed)


    #FUNCTION MUST RETURN AN RGBA STRING CONVERTED TO HEX
    def test_rgb2hex_rgba(self):
        #DEFINE RGB(A) LIST
        l_rgba = ['rgba(195, 00, 0, 0)', 'rgba(0, 100, 33, 253)',
                  'rgba(105, 0, 10, 0.75)', 'rgba(65, 125, 50, 1)',
                  'rgba(65, 125, 50, 1.0)', 'rgba(65, 125, 50, 0.25)',
                  'rgba(65, 125, 50, 0.4)']
        #DEFINE ALPHA HEX LIST
        l_ahex = ['#00c30000', '#fd006421',
                  '#bf69000a', '#ff417d32',
                  '#ff417d32', '#40417d32',
                  '#66417d32']

        #COMPARE RGB AND HEX VALUES FOR EACH PAIR >> STORE RESULT TO LIST
        passed = [u.rgb2hex(rgb_string=r, drop_alpha=False) == h for r, h in zip(l_rgba, l_ahex)]

        #UNIT TEST
        self.assertFalse(False in passed)


#-----------------------------------------------------------------------
#MAIN CONTROLLER METHOD
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
