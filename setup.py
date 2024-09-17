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

import sys
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

# If on Windows, add a [build] table for the compiler (only once).
if sys.platform == 'win32':
    s = '\n\n[build]\ncompiler=mingw32\n\n'
    with open('setup.cfg', 'a+', encoding='utf-8') as f:
        pos = f.tell()
        f.seek(0)
        if 'compile' not in f.read():
            f.seek(pos)
            f.write(s)

setup(**setup_args)
