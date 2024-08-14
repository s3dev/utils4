============================
utils4 Library Documentation
============================

.. contents:: Page Contents
    :local:
    :depth: 1

Overview
========
The ``utils4`` library is a CPython and C project which contains 
generalised, utility-based functions, designed to be an underlying
libary across your various Python 3.7+ projects.

``utils4`` is a complete overhaul of the ``utils3`` code base, which now
features a streamlined code base, complete documentation and a full test 
suite as part of the source distribution.

.. note:: 
    Some out-of-date modules and methods have been *removed* from 
    ``utils4``. If you find a method is missing, please continue to use 
    the latest release of ``utils3`` (v0.15.1) for this functionality.
        
If you have any questions that are not covered by this documentation, or
if you spot any bugs, issues or have any recommendations, please feel free
to :ref:`contact us <contact-us>`.


.. _using-the-library:

Using the Library
=================
This documentation suite contains detailed explanation and example usage 
for each of the library's importable modules. For detailed documentation, 
usage examples and links the source code itself, please refer to the 
:ref:`library-api` page.

If there is a specific module or method which you cannot find, a 
**search** field is built into the navigation bar to the left.


Installation
============
The easiest way to install ``utils4`` is using ``pip`` *after* activating
your virtual environment::
    
    pip install utils4


.. _building-a-wheel:

Building a Wheel File
---------------------

.. important:: 
    If using a virtual environment, be sure to 
    *activate the environment first*.

As the library contains some C components, building on Windows may prove 
tricky. To help address this, we've pre-compiled some of the more popular 
wheels for you. These wheels are available in `GitHub Releases`_.

If a wheel is not available for your architecture, a wheel can be built
from source, *if* the appropriate C build tools are installed on your 
system.

#. Download the latest source distribution from `PyPI`_.
#. Unpack the archive and navigate into the new unpacked directory.
#. Run the following command from the terminal, after activating the 
   appropriate virtual environment::

       python -m build . --wheel --no-isolation

This will build a wheel and place it in the local ``dist`` directory for 
installation.


List of available wheel files
+++++++++++++++++++++++++++++
We will create *some* wheel files, with each release, for the platforms and 
architectures listed below, which can be downloaded from `GitHub Releases`_. 
If we've just released and you don't see a wheel file there, please check 
back the following day as we may still be working through the builds. 
However, if you require something different than what we provide, the 
source distributions can also be downloaded from `PyPI`_.

.. csv-table:: Available Wheels
    :file:  ./_static/tbl/avail-wheels.csv 
    :header-rows: 1
    :stub-columns: 1
    :width: 100%


Questions or Issues
-------------------
If you have any issues or questions with your installation, please refer
to the :ref:`troubleshooting` section, or feel free to 
:ref:`contact us <contact-us>`.


.. _troubleshooting:

Troubleshooting
===============
No guidance at this time.


Documentation Contents
======================
.. toctree::
    :maxdepth: 1

    library
    changelog
    contact


Indices and Tables
==================
* :ref:`genindex`
* :ref:`modindex`


.. rubric:: Footnotes

.. _PyPI: https://pypi.org/project/utils4/#files
.. _GitHub: https://github.com/s3dev/utils4/
.. _GitHub Releases: https://github.com/s3dev/utils4/releases
.. _winlibs: https://winlibs.com


|lastupdated|

