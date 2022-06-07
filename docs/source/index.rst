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
libary across your various Python 3.6+ projects.

``utils4`` is a complete overhaul of the ``utils3`` code base, which now
features a streamlined code base, complete documentation and a full test 
suite as part of the source distribution.

.. note:: 
    Some out of date modules and methods have been *removed* from 
    ``utils4``. If you find a method is missing, please continue to use 
    the latest release of ``utils3`` (v0.15.1) for this functionality.
        
If you have any questions that are not covered by this documentation, or
if you spot any bugs, issues or have any recommendations, please feel free
to :ref:`contact us <contact-us>`.


.. _using-the-library:

Using the Library
=================
This documentation suite contains detailed explanation and example usage 
for each of the library's importable modules.

For detailed documentation, usage examples and links the source code 
itself, please refer to the :ref:`library-api` page.

If there is a specific module or method which you cannot find, a 
**search** field is built into the navigation bar to the left.


Installation
============
The easiest way to install ``utils4`` into your local Python instance,
is to :ref:`install the latest wheel file <installing-from-wheel>`. The 
wheel files can be downloaded from the `S3DEV archive`_.

Example for downloading the latest wheel::
    
    $ wget https://s3dev.uk/downloads/utils4-latest-<architecture>.whl


.. _installing-from-wheel:

Installing from a Wheel File
----------------------------

.. important:: 
    If using a virtual environment, be sure to 
    *activate the environment first*.

Install from a wheel file::

    $ pip install utils4-x.x.x-<architecture>.whl


List of available wheel files
+++++++++++++++++++++++++++++
We will create a wheel file, with each release, for the platforms and 
architectures listed below, which can be downloaded from the 
`S3DEV archive`_. However, if you require something different, the source
distributions can also be downloaded from the archive. Then, please refer 
to the guidance on 
:ref:`building and creating a wheel file from source <building-from-source>`.

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

.. _S3DEV archive: https://s3dev.uk/downloads/utils4
.. _winlibs: https://winlibs.com

|lastupdated|

