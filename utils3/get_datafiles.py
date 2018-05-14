# -*- coding: utf-8 -*-
"""
:Purpose:   This module is designed to provide a list of the required
            data files for project packaging to the calling
            ``setup.py`` file.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  The principal code concept was adopted from
            ``matplotlib.get_py2exe_datafiles()``.

:Example:
    To collect the data files for your project, use this in your
    ``setup.py`` file::

        from utils3.get_datafiles import get_datafiles

        data_files = get_datafiles(pkg_dir='myprog/package',
                                   exts=['.json', '.sql'],
                                   p2e=False)

"""

import os
import utils3.utils as utils

# ALLOW A LIST AS DEFAULT METHOD PARAMETER
# pylint: disable=dangerous-default-value
def get_datafiles(pkg_dir, exts=['.json', '.sql', '.txt'],
                  get_readme_files=True, readme_exts=['.html', '.md'],
                  get_license=True, license_name='LICENSE',
                  p2e=False):
    """Gather and return a list of project data files.

    This function is designed to be called by your project's
    ``setup.py`` file and will return a list of data files used by
    that project.

    The concept and principal design were adopted from matplotlib's
    ``get_py2exe_datafiles()`` function.

    Args:
        pkg_dir (str): The project's root directory to begin the search.
            Typically this your main package directory.

            - **Tip**: To get your package's full path, you can use this
              in your ``setup.py`` file::

                  pkg_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                         <pkg_dir_name>)

        exts (list): A list of file extensions used as a filter when
            collecting data files.
        get_readme_files (bool): Include the package's README file(s).
        readme_exts (list): A list of file extensions used as a filter
            when collecting README files.
        get_license (bool): Include the package's LICENSE file.
        license_name (str): Name of the LICENSE file to be included.
        p2e (bool): This package will be a py2exe installation.

            * ``p2e=True`` means the destination path is left as derived
              by the function
            * ``p2e=False`` means the environment's ``site-packages``
              directory will be prepended to the data files' destination
              path

    :Design:
        Your project's ``setup.py`` file will pass its project's
        root directory and a list of desired file extensions.  This
        function then performs a directory walk and picks out the full
        path to each desired file.  The results are returned as a list
        of tuples, which include the destination directory and the full
        path to each file.

        | The output format is shown here:
        | ``result = [('destination_dir', ['/path/to/file.ext', '...'])]``

        If the ``p2e`` (py2exe) flag is ``False``, the platform /
        environment's site-packages directory is prepended to the
        destination path, so the data files are installed to the
        site-package directory.  Otherwise, the package directory
        structure is used, with the package root being root.

    :Example:
        To use this function in your ``setup.py`` file::

            from utils3.get_datafiles import get_datafiles

            data_files = get_datafiles(pkg_dir='myprog/package',
                                       exts=['.json', '.sql'],
                                       p2e=False)

    """
    # INITIALISE
    result = {}

    # GET TAIL DIRECTORY (PACKAGE DIR NAME)
    tail = os.path.split(pkg_dir)[1]

    # WALK DIRECTORY TREE AND GET ALL FILES
    for root, _, files in os.walk(pkg_dir):
        # BUILD LIST OF FILES MEETING THE EXTENSION CRITERIA
        files = [os.path.realpath(os.path.join(root, fname)) for fname in files
                 if os.path.splitext(fname)[1] in _add_dot(exts)]
        # GET INDEX OF THE TAIL DIRECTORY FROM ROOT STRING
        # IF PY2EXE, ALSO REMOVE THE TAIL
        idx = root.rfind(tail) if p2e is False else root.rfind(tail) + len(tail) + 1
        # SLICE TO GET DEST DIR (AND SUB DIRS)
        root = root[idx:]
        # TEST IF PY2EXE INSTALLATION >> IF NOT, PREPEND SITE-PACKAGES DIR
        if p2e is False:
            root = os.path.join(utils.getsitepackages(), root)
        # TEST IF FILES TO BE ADDED >> ADD FILES TO DICT WITH DEST DIR AS THE KEY
        if len(files) > 0: result[root] = files

    # CONVERT TO LIST
    data_files = list(result.items())

    # TEST FOR README DIRECTIVE
    if get_readme_files:
        # APPEND README FILE(S)
        data_files = data_files + _get_readmefiles(pkg_dir=pkg_dir,
                                                   readme_exts=readme_exts, p2e=p2e)

    # TEST FOR LICENSE DIRECTIVE
    if get_license:
        # APPEND LICENSE FILE
        data_files = data_files + _get_license(pkg_dir=pkg_dir,
                                               license_name=license_name, p2e=p2e)

    # RETURN THE COMPILED LIST OF DATA FILES
    return data_files


def _get_readmefiles(pkg_dir, readme_exts=['.html', '.md'], p2e=False):
    """Get the README files.

    This private function is called by the main
    :func:`~get_datafiles.get_datafiles` function and is used to add
    the README file(s) to the returned list of data files.

    Args:
        pkg_dir (str):
        readme_exts (list):
        p2e (bool):

    **For argument descriptions**, refer to the docstring for
    :func:`~get_datafiles.get_datafiles`.

    :Design:
        This function starts the directory walk at the level **above**
        the provided package directory; as this is often where the
        README and LICENSE files live.

    Note:
        Although this function is designed to get the README files with
        a given extension, **there is no validation on the file name**,
        only on the extension.

        In otherwords, if there is a file named ``FOO.html``, it will be
        picked up if .html is in the ``readme_exts`` list.

    """
    # INITIALISE
    result = {}

    # GET TAIL DIRECTORY (PACKAGE DIR NAME)
    tail = os.path.split(pkg_dir)[1]

    # WALK DIRECTORY TREE AND GET ALL FILES
    for root, _, files in os.walk(os.path.dirname(pkg_dir)):
        # BUILD LIST OF FILES MEETING THE EXTENSION CRITERIA
        files = [os.path.realpath(os.path.join(root, fname)) for fname in files
                 if os.path.splitext(fname)[1] in _add_dot(readme_exts)]
        # IF PY2EXE, SET ROOT TO '', ELSE PREPEND SITE-PACKAGES
        root = os.path.join(utils.getsitepackages(), tail) if p2e is False else ''
        # TEST IF FILES TO BE ADDED >> ADD FILES TO DICT WITH DEST DIR AS THE KEY
        if len(files) > 0: result[root] = files

    # CONVERT DICT TO LIST OF TUPLES
    return list(result.items())


def _get_license(pkg_dir, license_name='LICENSE', p2e=False):
    """Get the LICENSE file.

    This private function is called by the main
    :func:`~get_datafiles.get_datafiles` function and is used to add
    the LICENSE file to the returned list of data files.

    Args:
        pkg_dir (str):
        license_name (str):
        p2e (bool):

    **For argument descriptions**, refer to the docstring for
    :func:`~get_datafiles.get_datafiles`.

    :Design:
        This function starts the directory walk at the level **above**
        the provided package directory; as this is often where the
        README and LICENSE files live.

    """
    # INITIALISE
    result = {}

    # GET TAIL DIRECTORY (PACKAGE DIR NAME)
    tail = os.path.split(pkg_dir)[1]

    # WALK DIRECTORY TREE AND GET ALL FILES
    for root, _, files in os.walk(os.path.dirname(pkg_dir)):
        # BUILD LIST OF FILES MEETING THE EXTENSION CRITERIA
        files = [os.path.realpath(os.path.join(root, fname)) for fname in files
                 if fname == license_name]
        # IF PY2EXE, SET ROOT TO '', ELSE PREPEND SITE-PACKAGES
        root = os.path.join(utils.getsitepackages(), tail) if p2e is False else ''
        # TEST IF FILES TO BE ADDED >> ADD FILES TO DICT WITH DEST DIR AS THE KEY
        if len(files) > 0: result[root] = files

    # CONVERT DICT TO LIST OF TUPLES
    return list(result.items())


def _add_dot(ext_list):
    """Add a dot (.) to the beginning of each extension in a list.

    Args:
        ext_list (list): A list of file extensions.

    Returns:
        A list of extensions, with a dot prepended to each extension,
        if it doesn't already exist.

    """
    # LOOP THROUGH EXTENSIONS
    for idx, ext in enumerate(ext_list):
        # TEST FOR DOT (.ext) >> IF NOT, ADD IT AND UPDATE LIST
        if not ext.startswith('.'): ext_list[idx] = '.%s' % ext
    # RETURN MODIFIED EXTENSION LIST
    return ext_list
