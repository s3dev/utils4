#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:App:       setup.py
:Purpose:   Python library packager.

:Version:   0.2.1
:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Example:
    Create source and wheel distributions::

        $ cd /path/to/package
        $ python setup.py sdist bdist_wheel

    Simple installation::

        $ cd /path/to/package/dist
        $ pip install <pkgname>-<...>.whl

    git installation::

        $ pip install git+file:///<drive>/path/to/package

    github installation::

        $ pip install git+https://github.com/s3dev/<pkgname>

"""

import os
import platform
from setuptools import setup, find_packages
from utils3.get_datafiles import get_datafiles
from utils3 import utils
from utils3._version import __version__


# pylint: disable=too-few-public-methods
class Setup(object):
    """Create a dist package for this library."""

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
    PACKAGES        = find_packages()
    REQUIRES        = ['colorama']
    # ONLY REQUIRE IF WINDOWS
    if 'win' in platform.system().lower():
        REQUIRES.append('win_unicode_console')

    # ADD DATA AND DOCUMENTATION FILES
    DATA_FILES      = get_datafiles(pkg_dir=PACKAGE_ROOT, get_docs=True)
    PACKAGE_DATA    = {'utils3': ['user_interface_config.json']}

    def run(self):
        """Run the setup."""
        setup(name=self.PACKAGE,
              version=self.VERSION,
              platforms=self.PLATFORMS,
              description=self.DESC,
              author=self.AUTHOR,
              author_email=self.AUTHOR_EMAIL,
              maintainer=self.AUTHOR,
              maintainer_email=self.AUTHOR_EMAIL,
              url=self.URL,
              license=self.LICENSE,
              packages=self.PACKAGES,
              install_requires=self.REQUIRES,
              data_files=self.DATA_FILES,
              include_package_data=self.INCL_PKG_DATA,
              classifiers=self.CLASSIFIERS,
              package_data=self.PACKAGE_DATA)


if __name__ == '__main__':
    Setup().run()
