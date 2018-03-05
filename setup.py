'''------------------------------------------------------------------------------------------------
Program:    setup.py
Purpose:    Setup packager for utils.

Dependents: distutils
            setuptools

Comments:

            Installation:
            > cd /path/to/package_x.x.x
            > pip install . --no-deps

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
------------------------------------------------------------------------------------------------'''

# BUILT-IN IMPORTS
import os

# EXTERNAL IMPORTS
from setuptools import setup, find_packages

# SELF-DEPENDENT IMPORTS
from utils3.get_datafiles import get_datafiles
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
              url='https://github.com/s3dev/utils',
              license='MIT',
              packages=find_packages(),
              install_requires=['numpy',
                                'cx_Oracle',
                                'unidecode',
                                'matplotlib',
                                'pyodbc',
                                'plotly',
                                'mysql-connector==2.1.4',
                                'colorama'],
              data_files=get_datafiles(pkg_dir=package))


if __name__ == '__main__':
    packager = Packager()
    packager.run()
