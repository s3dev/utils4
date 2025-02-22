
# A general utilities package for Python 3.7+

[![PyPI - Version](https://img.shields.io/pypi/v/utils4?style=flat-square)](https://pypi.org/project/utils4)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/utils4?style=flat-square)](https://pypi.org/project/utils4)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utils4?style=flat-square)](https://pypi.org/project/utils4)
[![PyPI - Status](https://img.shields.io/pypi/status/utils4?style=flat-square)](https://pypi.org/project/utils4)
[![Static Badge](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](https://pypi.org/project/utils4)
[![Static Badge](https://img.shields.io/badge/code_coverage-100%25-brightgreen?style=flat-square)](https://pypi.org/project/utils4)
[![Static Badge](https://img.shields.io/badge/pylint_analysis-100%25-brightgreen?style=flat-square)](https://pypi.org/project/utils4)
[![Documentation Status](https://readthedocs.org/projects/utils4/badge/?version=latest&style=flat-square)](https://utils4.readthedocs.io/en/latest/)
[![PyPI - License](https://img.shields.io/pypi/l/utils4?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/utils4?style=flat-square)](https://pypi.org/project/utils4)

The ``utils4`` project is a CPython and C library which contains generalised, utility-based functions, designed to be an underlying library across your various Python 3.7+ projects.


## Installation
The easiest way to install ``utils4`` is using `pip` *after* activating your virtual environment:

```
pip install utils4
```

## Toolset
Listed below are *some* of the project's commonly used tools and utilities. Some of these items are utilities unto themselves, while others are simple convenience wrappers around existing libraries, just brought together for convenience.

- Colour maps
- Converters (e.g. binary, hexadecimal, ASCII and integer)
- Cryptographic and hashing functions
- Error reporting
- General maths-based functionality (e.g. for solving [Project Euler](https://projecteuler.net/) problems)
- General utility functions
- Logging
- Progress bar
- Terminal colour handling
- Terminal user interface styling 
- Wait ticker / spinner
- etc.


## Using the Library
The [documentation suite](https://utils4.readthedocs.io/en/latest/index.html) contains usage examples and detailed explanation for each of the library's importable modules. Please refer to the [Library API Documentation](https://utils4.readthedocs.io/en/latest/library.html#library-api) section of the documentation.


## Additional Information
As the library contains some C components, building on Windows may prove tricky.  To help address this, we've pre-compiled some `win_amd64` wheels for you. These wheels are available on [GitHub's Releases page](https://github.com/s3dev/utils4/releases), for each release.

