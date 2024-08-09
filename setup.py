#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   Build the C-extensions for ``utils4``.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  This script is run *automatically* by ``build`` as an
            extension of pyproject.toml, and does not require any direct
            interaction.

"""

from setuptools import setup, Extension

# Add C extensions.
# https://stackoverflow.com/a/66479252/6340496
setup_args = {'ext_modules': [Extension('utils4.mathfunc',
                                        sources=['utils4/mathfuncmodule.c',
                                                 'utils4/libs/_mathfunc.c'],
                                        include_dirs=['utils4',
                                                      'utils4/libs'],
                                        py_limited_api=True,
                                        language='c')]}

setup(**setup_args)
