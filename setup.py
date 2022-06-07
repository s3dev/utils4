#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:App:       setup.py
:Purpose:   Python library packager.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     support@s3dev.uk

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
# pylint: disable=invalid-name

import os
import platform
import shutil
from glob import glob
from setuptools import setup, Extension, find_packages
from utils4._version import __version__


class Setup:
    """Create a dist package for this library."""

    PACKAGE         = 'utils4'
    VERSION         = __version__
    PLATFORMS       = 'Python 3.6+'
    DESC            = 'Bespoke general utilities package for Python 3.6+.'
    AUTHOR          = 'J. Berendt'
    AUTHOR_EMAIL    = 'support@s3dev.uk'
    URL             = 'https://github.com/s3dev/utils4'
    LICENSE         = 'MIT'
    ROOT            = os.path.realpath(os.path.dirname(__file__))
    PACKAGE_ROOT    = os.path.join(ROOT, PACKAGE)
    DIST            = os.path.join(ROOT, 'dist')
    INCL_PKG_DATA   = False
    MIN_PYTHON      = '>=3.6'
    CLASSIFIERS     = ['Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Programming Language :: Python :: 3.9',
                       'Programming Language :: Python :: 3.10',
                       'License :: OSI Approved :: MIT License',
                       'Development Status :: 4 - Beta',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX :: Linux',
                       'Topic :: Software Development',
                       'Topic :: Software Development :: Libraries',
                       'Topic :: Utilities']

    # PACKAGE REQUIREMENTS
    PACKAGES        = find_packages()
    REQUIRES        = []
    # ONLY REQUIRE IF WINDOWS
    if 'win' in platform.system().lower():
        REQUIRES.extend(['colorama'])

    # ADD DATA AND DOCUMENTATION FILES (FOR WHEEL FILE)
    DATA_FILES      = []
    PACKAGE_DATA    = {}

    # Add C extensions.
    MODULES = [Extension('mathfunc',
                         sources=['./utils4/mathfuncmodule.c', './utils4/libs/_mathfunc.c'],
                         language='c')]

    def run(self):
        """Run the setup."""
        setup(name=self.PACKAGE,
              version=self.VERSION,
              platforms=self.PLATFORMS,
              python_requires=self.MIN_PYTHON,
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
              package_data=self.PACKAGE_DATA,
              ext_modules=self.MODULES,
              options={'build': {'build_lib': './build'},
                       'build_ext': {'build_lib': './build/utils4'}})

    def create_latest_source_dist(self):
        """Copy the source dist .tar.gz file, and rename using 'latest'."""
        sources = glob(os.path.join(self.DIST, f'*{__version__}*.tar.gz'))
        for src in sources:
            path, fn = os.path.split(src)
            dst = os.path.join(path, fn.replace(f'{__version__}', 'latest'))
            print(f'\nCreating \'latest\' source dists:\n- {src}\n--> {dst}\n')
            # Allow file to be overwritten.
            if os.path.exists(dst):
                os.remove(path=dst)
            shutil.copy(src=src, dst=dst)

    def create_latest_wheel(self):
        """Copy the wheel file, and rename using 'latest'."""
        wheels = glob(os.path.join(self.DIST, f'*{__version__}*.whl'))
        for src in wheels:
            path, fn = os.path.split(src)
            dst = os.path.join(path, fn.replace(f'{__version__}', 'latest'))
            print(f'\nCreating \'latest\' wheel:\n- {src}\n--> {dst}\n')
            # Allow file to be overwritten.
            if os.path.exists(dst):
                os.remove(path=dst)
            shutil.copy(src=src, dst=dst)


if __name__ == '__main__':
    _setup = Setup()
    _setup.run()
    _setup.create_latest_wheel()
    _setup.create_latest_source_dist()
