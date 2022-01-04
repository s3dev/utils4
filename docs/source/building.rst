
.. _building-from-source:

==========================================
Building utils4 from a Source Distribution
==========================================

As this library contains C extensions, you may need to build the code from
source, to accommodate your specific architecture or OS.

.. note:: **Windows users:**

    If building for Windows, you will need a C-compiler installed.

    For example, the *MinGW* development environment is an easy to install
    option which provides this functionality for Windows, a link is 
    provided below.

The good people at `winlibs`_ have put together 7-Zip and Zip archives 
for a number of *standalone* GCC and MinGW-w64 builds. Once the selected
build is downloaded, refer to the *Usage* section for installation and
usage details.


Building utils4 from source
---------------------------
The steps below demonstrate building ``utils4`` from the *latest* source 
distribution.

#. Download the source distribution from the `S3DEV archive`_.
#. Copy the source distribution file (``utils4-latest.tar.gz``) to your 
   local PC.
#. Navigate to the directory into which the source was just copied.

#. Extract the source [#]_::

    $ tar -zxvf utils4-latest.tar.gz

#. Navigate into the extracted source directory::

    $ cd ./utils4-latest

#. **Unix-like** - Option A: Build the distribution from source::

    $ python ./setup.py build

#. **Unix-like** - Option B: Build a wheel from source::

    $ python ./setup.py bdist_wheel

#. **Unix-like** - Option C: Install directly from source::

    $ pip install .

#. **Windows**: Build the distribution from source::

    $ python setup.py build --compiler=mingw32  # <-- specify the compiler to be used

#. **Windows** - Option A: Build a wheel from the build::

    # Reminder: The a .\build directory must exist.
    $ python setup.py bdist_wheel

#. **Windows** - Option B: Install from the build::

    # Reminder: The a .\build directory must exist.
    $ pip install .

#. Install the newly created wheel as any other::

    $ cd ./dist
    $ pip install utils4-latest-<architecture>.whl


Questions or Issues
-------------------
If you have any issues or questions with your installation, please refer
to the :ref:`troubleshooting` section, or feel free to 
:ref:`contact us <contact-us>`.


.. rubric:: Footnotes

.. [#] If using Windows, `7-zip`_ can be used to extract ``tar.gz`` files.

.. _7-zip: https://www.7-zip.org/
.. _S3DEV archive: https://s3dev.uk/downloads
.. _winlibs: https://winlibs.com

|lastupdated|

