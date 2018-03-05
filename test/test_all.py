'''---------------------------------------------------------------------
Program:    test_all
Purpose:    Program for running all unit test files.

Dependents: os

Developer:  J. Berendt
Email:      jeremy.berendt@rolls-royce.com

Comments:   This module should be run from the command line, as shown
            below.  Test output will not be shown if run inside IDE.

Use:        >>> cd /path/to/tests
            >>> python test_all.py

------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for
                                        Python 3 from the Python 2.7
                                        utils module.
---------------------------------------------------------------------'''

# BUILT-IN IMPORTS
import os

#-----------------------------------------------------------------------
#METHOD FOR RUNNING THE TESTS
def runit(module):

    #NOTIFICATION
    print('\nRUNNING TEST(S) FOR: %s' % (module))
    #DO IT!
    os.system('python %s' % module)


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #VARIABLES
    testlist = 'testlist.txt'

    try:
        #VERIFY TESTLIST FILE EXISTS
        if os.path.exists(testlist):
            #GET LIST OF TEST MODULES FROM TEXT FILE
            modules = [item.strip() for item in open('testlist.txt', 'r').readlines()
                       if item.strip() != '' and not item.startswith('#')]

            #LOOP THROUGH MODULES >> RUN MODULE
            for module in modules: runit(module=module)

        else:
            #NOTIFICATION
            print('ERR: The %s file cannot be found.' % testlist)

    except Exception as err:
            #NOTIFICATION
        print('ERR: %s' % err)


#RUN PROGRAM
if __name__ == '__main__': main()
