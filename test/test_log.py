"""------------------------------------------------------------------------------------------------
Program:    test_log
Purpose:    Unit test for utils.log

Dependents: utils.log

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        > cd /package_root/test
            > python test_log.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
05.03.18    J. Berendt      0.0.2       BUG01: "ResourceWarning: unclosed file <_io.TextIOWrapper \
                                        name='nul' mode='w' encoding='cp1252'>" thrown on:
                                        text = [line.strip() for line in open(log_path, 'r')
                                                                             .readlines()]
                                        FIX01: Replaced statement with 'with' statement, so the
                                        file is closed automatically on completion.
------------------------------------------------------------------------------------------------"""

import os
import re
import unittest

from utils3.log import Log


class TestLog(unittest.TestCase):

    def test_log(self):

        # VARIABLES
        log_path       = 'c:/temp/utils_log_unittest.log'
        header         = 'datetime,host,user,text'
        entry          = 'this is a test'
        pattern_entry  = r'([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6},' \
                          '[0-9a-zA-Z].*,' \
                          '[0-9a-zA-Z].*,' + entry + ')'
        exp            = re.compile(pattern_entry)

        # INSTANTIATE LOG CLASS
        _log = Log(filepath=log_path, autofill=True, printheader=True,
                   headertext=header)

        # WRITE LOG FILE
        _log.write(text=entry)
        _log.write_blank_line()

        # READ IN LOG FILE
        with open(log_path, 'r') as f:
            text = [line.strip() for line in f.readlines()]

        # TEST HEADER
        self.assertTrue(text[0] == header)

        # TEST LOG ENTRY AGAINST REGEX
        self.assertTrue(len(exp.findall(text[1])) == 1)

        # TEST FOR BLANK LINE (WRITTEN BY write_blank_line() METHOD)
        self.assertTrue(text[2] == '')

        # DELETE THE LOG FILE
        if os.path.exists(log_path): os.remove(log_path)


# ----------------------------------------------------------------------
# MAIN PROGRAM CONTROLLER
def main():

    # RUN UNIT TESTS
    unittest.main()


# RUN PROGRAM
if __name__ == '__main__': main()
