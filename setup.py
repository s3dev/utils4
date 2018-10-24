'''------------------------------------------------------------------------------------------------
Program:    setup.py
Purpose:    Setup packager.

Comments:
            Create source and wheel distributions:
            > cd /path/to/package
            > python setup.py sdist bdist_wheel

            Simple installation:
            > cd /path/to/package/dist
            > pip install utils3-<...>.whl --no-deps

            git installation:
            > pip install git+file:///<drive>:/path/to/package --no-deps

            github installation:
            > pip install git+https://github.com/s3dev/utils3

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
12.06.18    J. Berendt      0.1.0       Written to replace the current class setup file for
                                        utils3 v0.5.0.
                                        Added Sphinx documentation.
------------------------------------------------------------------------------------------------'''

import os
from setuptools import setup, find_packages
from utils3.get_datafiles import get_datafiles
from utils3 import utils
from utils3._version import __version__

# -------------------------------------------------------------------------
# PACKAGE CONSTANTS (EDIT THESE)
PACKAGE         = 'utils3'
VERSION         = __version__
PLATFORMS       = 'Python 3.5'
DESC            = 'Bespoke general utilities package for Python 3.5.'
AUTHOR          = 'J. Berendt'
AUTHOR_EMAIL    = 'support@73rdstreetdevelopment.co.uk'
URL             = 'https://github.com/s3dev/utils3'
LICENSE         = 'MIT'
ROOT            = os.path.realpath(os.path.dirname(__file__))
PACKAGE_ROOT    = os.path.join(ROOT, PACKAGE)
SITE_PKGS       = os.path.join(utils.getsitepackages(), PACKAGE)
INCL_PKG_DATA   = False
CLASSIFIERS     = ['Programming Language :: Python :: 3.5',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities']

# PACKAGE REQUIREMENTS
REQUIRES        = ['colorama',
                   'cx_Oracle',
                   'matplotlib',
                   'mysql-connector==2.1.4',
                   'numpy',
                   'pyodbc',
                   'plotly',
                   'unidecode',
                   'win_unicode_console']

PACKAGES        = find_packages()

# ADD DATA AND DOCUMENTATION FILES
DATA_FILES      = get_datafiles(pkg_dir=PACKAGE_ROOT, get_docs=True)
PACKAGE_DATA    = {'utils3': ['user_interface_config.json']}

# -----------------------------------------------------------------------
# SETUP PARAMETERS (DO NOT EDIT THESE)
setup(name=PACKAGE,
      version=VERSION,
      platforms=PLATFORMS,
      description=DESC,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      packages=PACKAGES,
      install_requires=REQUIRES,
      data_files=DATA_FILES,
      include_package_data=INCL_PKG_DATA,
      classifiers=CLASSIFIERS,
      package_data=PACKAGE_DATA)