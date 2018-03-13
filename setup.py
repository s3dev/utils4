'''------------------------------------------------------------------------------------------------
Program:    setup.py
Purpose:    Setup packager for utils.

Comments:

            Installation:
            > cd /path/to/package_x.x.x
            > pip install . --no-deps

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
13.03.18    J. Berendt      1.1.0       Added win_unicode_console as a required package.
------------------------------------------------------------------------------------------------'''

import os
from setuptools import setup, find_packages

from utils3 import get_datafiles
from utils3._version import __version__


class Packager(object):

    @staticmethod
    def run():
        package = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'utils3')
        setup(name='utils3',
              version=__version__,
              platforms='Python 3.5',
              description='Bespoke general utilities package for Python 3.5.',
              author='J. Berendt',
              author_email='support@73rdstreetdevelopment.co.uk',
              url='https://github.com/s3dev/utils3',
              license='MIT',
              packages=find_packages(),
              install_requires=['colorama',
                                'cx_Oracle',
                                'matplotlib',
                                'mysql-connector==2.1.4',
                                'numpy',
                                'pyodbc',
                                'plotly',
                                'unidecode',
                                'win_unicode_console'],
              data_files=get_datafiles.get_datafiles(pkg_dir=package))


if __name__ == '__main__':
    packager = Packager()
    packager.run()
