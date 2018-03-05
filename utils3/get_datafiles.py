"""------------------------------------------------------------------------------------------------
Program:    get_datafiles
Platform:   Windows / Linux

Purpose:    This module is designed to provide a list of data files to the calling setup.py file.

Developer:  J. Berendt
            With principal code concept adopted from matplotlib.get_datafiles()
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > import utils3.get_datafiles as gdf
            > data_files = gdf.get_datafiles(pkg_dir='myprog/package', exts=['.json', '.sql'])

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    0.0.1       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
------------------------------------------------------------------------------------------------"""

# BUILT-IN IMPORTS
import os

# SELF-DEPENDENT IMPORTS
import utils3.utils as utils

# ALLOW A LIST AS DEFAULT METHOD PARAMETER
# pylint: disable=dangerous-default-value


# ----------------------------------------------------------------------
# FUNCTION RETURNS A PY2EXE LIST OF DATA FILES USED BY THIS PACKAGE
def get_datafiles(pkg_dir, exts=['.json', '.sql', '.txt'],
                  get_readme_files=True, readme_exts=['.html', '.md'],
                  get_license=True, license_name='LICENSE',
                  p2e=False):

    """
    PURPOSE:
    This function is designed to be called by another program's setup.py
    file and will return a list of data files used by that program.

    The concept and principal design were adopted from matplotlib's
    get_py2exe_datafiles() function.

    RESULTS FORMAT:
        return = [('destination_dir', ['/path/to/file.ext', '...'])]

    DESIGN:
    The calling program (setup.py file) will pass its program's root
    directory and a list of desired file extensions.  The function then
    performs a directory walk and picks out the full path to each
    desired file.

    The results are returned as a list of tuples, which include the
    destination directory and the full path to each file.

    If the p2e (py2exe) flag is False, the platform's site-packages
    directory is prepended to the destination path, so the data files
    are installed to the package's site-package directory.  Otherwise,
    the package directory structure is used, with the package root
    being root.

    PARAMETERS:
    - pkg_dir
    The root directory to begin the search.  Typically this your main
    package directory.
    Tip: In your setup.py file, you can use
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'pkg') to
    get the package's directory path.
    - exts (default=['.json', '.sql', '.txt'])
    A list of file extensions used as a filter when collecting data
    files.
    - get_readme_files (default=True)
    Include the package's README file(s).
    - readme_exts (default=['.html', '.md'])
    A list of file extensions used as a filter when collecting README
    files.
    - get_license (default=True)
    Include the package's LICENSE file.
    - license_name (default='LICENSE')
    Name of the LICENSE file to be included.
    - p2e (default=False)
    This flag indicates to the function whether this is a py2exe
    installation, or not.
    p2e=True means the destination path is left as derived by the
    function.
    p2e=False means the platform's site-packages directory is prepended
    to the destination path.

    USE:
    > from utils3.get_datafiles import get_datafiles
    > data_files = get_datafiles(pkg_dir='myprog/package',
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


# ----------------------------------------------------------------------
# FUNCTION USED TO GET THE README FILES(S)
def _get_readmefiles(pkg_dir, readme_exts=['.html', '.md'], p2e=False):

    """
    PURPOSE:
    This private function is called by the main get_datafiles() files
    and is used to add the README file(s) to the returned list of
    data_files.

    This function starts the directory walk at the level *above* the
    provided package directory; as this is often where the README and
    LICENSE files live.
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


# ----------------------------------------------------------------------
# FUNCTION USED TO GET THE LICENSE FILE
def _get_license(pkg_dir, license_name='LICENSE', p2e=False):

    """
    PURPOSE:
    This private function is called by the main get_datafiles() files
    and is used to add the LICENSE file to the returned list of
    data_files.

    This function starts the directory walk at the level *above* the
    provided package directory; as this is often where the README and
    LICENSE files live.
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


# ----------------------------------------------------------------------
# HELPER FUNCTION TO TEST AND ADD A DOT TO THE BEGINNING OF AN EXTENSION
def _add_dot(ext_list):

    """
    PURPOSE:
    This private function is used to add a dot ('.') to the beginning
    of each file extension in an *_exts list; if a dot is not already
    present.
    """

    # LOOP THROUGH EXTENSIONS
    for idx, ext in enumerate(ext_list):
        # TEST FOR DOT (.ext) >> IF NOT, ADD IT AND UPDATE LIST
        if not ext.startswith('.'): ext_list[idx] = '.%s' % ext

    # RETURN MODIFIED EXTENSION LIST
    return ext_list
