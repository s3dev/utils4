"""------------------------------------------------------------------------------------------------
Program:    utils.py
Purpose:    Central library for standard S3DEV utilities.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > from utils3 import utils as u
            > help(u)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
07.03.18    J. Berendt      1.0.1       Minor code formatting updates.
                                        Print statements changed to proper case.
13.03.18    J. Berendt      1.1.0       Updated the input() function to use six.moves.input()
                                        for Py2/Py3 compatibility.
------------------------------------------------------------------------------------------------"""

# AS THIS IS A UTILITIES PACKAGE, NOT ALL IMPORTS ARE USED DURING
# EXECUTION, SO MOST IMPORTS SIT WITH THE METHOD OR FUNCTION IN WHICH
# THEY ARE USED.

import six

from utils3 import config
from utils3 import reporterror
from utils3 import user_interface
from utils3._version import __version__

# GLOBAL CONSTANTS / CLASS INSTANTIATIONS
_UI = user_interface.UserInterface()


# ----------------------------------------------------------------------
def clean_df(df):
    """
    Return a cleaned pandas dataframe.

    DESIGN:
    Function designed to clean dataframe content.
        - column names: replace a space with an underscore
        - column names: convert to lower case
        - values:       strip whitespace

    Function returns a 'cleaned' copy of the dataframe.

    PARAMETERS:
        - df
          The pandas dataframe for cleaning.

    DEPENDENTS:
        - numpy

    USE:
    > import utils3.utils as u
    > df = u.clean_df(df)
    """

    # EXTERNAL IMPORTS
    import numpy as np

    # CREATE A COPY OF THE DATAFRAME
    df_c = df.copy()

    # CLEAN HEADERS (REPLACE, STRIP WHITESPACE, UPPER CASE)
    df_c.rename(columns=lambda col: col.strip().replace(' ', '_').lower(), inplace=True)

    # STRIP WHITESPACE FROM VALUES
    for col in df_c.columns:
        # TEST FOR NUMBER AND DATETIME TYPES
        if not np.issubdtype(df_c[col], np.datetime64) and not np.issubdtype(df_c[col], np.number):
            # STRIP WHITESPACE
            df_c[col] = df_c[col].str.strip()

    # RETURN CLEANED DATAFRAME
    return df_c


# ----------------------------------------------------------------------
def dbconn_mysql(host=None, user=None, password=None, database=None, port=3306,
                 from_file=False, filename=None):
    """
    Return MySQL database connection and cursor objects.  Prompt for
    missing credentials.

    DESIGN:
    Function designed to create a connection to a MySQL database
    using the provided login details, or directly from a config file.
    If a login detail is not provided, the end-user is prompted; which
    can be used as a security feature.

    Once all credentials are gathered, the connection is tested.  If
    successful, the connection and cursor objects are returned to the
    calling program, as a dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    SOURCE:
    The connection argument keys for a MySQL connection using the
    mysql.connection library, are listed here:
    https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html

    PARAMETERS:
        - host (default=None)
          IP address or machine name of the host or database server
        - user (default=None)
          user name used to authenticate
        - password (default=None)
          just what it says on the tin  :-)
        - database (default=None)
          name of the database to connect
        - port (default=3306)
          the TCP/IP port of the MySQL server; must be an integer
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - user, password, database, host, port
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - mysql-connector (2.1.4)
      Installation: > pip install mysql-connector==2.1.4

    USE: PASSED CONNECTION DETAILS:
    > import utils3.utils as u
    > dbo = u.dbconn_mysql(host, user, password, database)
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils3.utils as u
    > dbo = u.dbconn_mysql(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']
    """

    try:
        # INITIALISE
        creds = dict()
        dbtype = 'mysql'

        # TEST IF CONFIG FILE IS USED
        if from_file:
            # CONFIG KEYS TO CHECK
            db_keys = ['user', 'password', 'database', 'host', 'port']

            # VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            # TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, host=host, user=user, password=password,
                                   database=database, port=port)

        # TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            # MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_mysql_conn(creds=creds)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the MySQL database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_oracle(host=None, user=None, userid=None, password=None,
                  from_file=False, filename=None):
    """
    Return Oracle database connection and cursor objects.  Prompt for
    missing credentials.

    DESIGN:
    Function designed to create a connection to an Oracle database
    using the provided login details, or directly from a config file.
    If a login detail is not provided, the user is prompted; which can
    be used as a security
    feature.

    The connection is tested.  If successful, the connection and
    cursor objects are returned to the calling program, as a
    dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    PARAMETERS:
        - host (default=None)
          database host; or database name
        - user (default=None)
          user name, or schema name
        - userid (default=None)
          same as 'user' parameter (both are not needed)
        - password (default=None)
          just what it says on the tin  :-)
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - host, user, password
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - cx_Oracle

    USE:
    > import utils3.utils as u
    > dbo = u.dbconn_oracle(host='myhost', userid='myuser',
                            password='mypass')
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils3.utils as u
    > dbo = u.dbconn_oracle(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']
    """

    try:
        # INITIALISE
        creds = dict()
        dbtype = 'oracle'

        # TEST IF CONFIG FILE IS USED
        if from_file:
            # CONFIG KEYS TO CHECK
            db_keys = ['host', 'user', 'password']

            # VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            # COMBINE USER AND USERID
            user = user if user is not None else userid

            # TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, host=host, user=user, password=password)

        # TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            # MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_oracle_conn(creds=creds)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the Oracle database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_sql(server=None, database=None, userid=None, user=None,
               password=None, from_file=False, filename=None):
    """
    Return SQL Server database connection and cursor objects.  Prompt
    for missing credentials.

    DESIGN:
    Function designed to create a connection to a SQL Server database
    using the provided login parameters, or directly froma config file.
    If a login detail is not provided, the user is prompted; which can
    be used as a security
    feature.

    The connection is tested.  If successful, the connection and cursor
    objects are returned to the calling program, as a dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    PARAMETERS:
        - server (default=None)
          name of the server on which the database lives
        - database (default=None)
          name of the database to which you're connecting
        - user (default=None)
          just what it says on the tin
        - userid (default=None)
          same as 'user' parameter (both are not needed)
        - password (default=None)
          again, just what it says on the tin  :-)
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - server, database, user, password
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - pyodbc

    USE:
    > import utils3.utils as u
    > dbo = u.dbconn_sql(server, database, user, password)
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils3.utils as u
    > dbo = u.dbconn_sql(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']
    """

    try:
        # INITIALISE
        creds = dict()
        dbtype = 'sql_server'

        # COMBINE USER AND USERID
        user = user if user is not None else userid

        # TEST IF CONFIG FILE IS USED
        if from_file:
            # CONFIG KEYS TO CHECK
            db_keys = ['server', 'database', 'user', 'password']

            # VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            # TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, server=server, database=database,
                                   user=user, password=password)

        # TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            # MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_sql_conn(creds=creds)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the SQL Server database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_sqlite(db_path):
    """
    Return a dictionary containing the connection and cursor objects
    for a SQLite database connection.

    DESIGN:
    Function designed to create and return database connection and
    cursor objects for a SQLite database, using the passed database
    filename.

    conn = [the connection object]
    cur  = [the cursor object]

    PARAMETERS:
        - db_path
        Full path to the SQLite database file.

    DEPENDENCIES:
    - sqlite3
    - reporterror

    USE:
    > import utils3.utils as u
    > dbo = u.dbconn_sqlite(db_path)
    > conn = dbo['conn']
    > cur = dbo['cur']
    """

    # BUILT-IN IMPORTS
    import sqlite3 as sql

    try:
        # CREATE CONNECTION / CURSOR OBJECTS
        connection = sql.connect(db_path)
        cursor = connection.cursor()

        # STORE RESULT IN DICTIONARY
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        # NOTIFICATION
        reporterror.reporterror(err)


# ----------------------------------------------------------------------
def direxists(path, create_path=True):
    """
    Return a boolean value based on if a directory exists.  If
    instructed by the caller, create the directory tree.

    DESIGN:
    Function designed to test if a directory path exists.  If the path
    does not exist, the path can be created; determined by passed the
    value of create_path(boolean).

    This function expands in the standard os.path.exists() function in
    that the path can be created, if it doesn't already exist, by
    passing the create_path parameter as True; which is the default
    action.

    PARAMETERS:
        - path
          the directory you are testing
        - create_path (default=True)

    DEPENDENCIES:
    - os

    USE:
    > import utils3.utils as u
    > u.direxists(path[, create_path])
    """

    # BUILT-IN IMPORTS
    import os

    # INITIALISE VARIABLE
    found = False

    # LOOP
    while True:
        # TEST IF PATH EXISTS
        if os.path.exists(path):
            # FLAG AS FOUND
            found = True
            # EXIT LOOP
            break
        else:
            # TEST IF DIRECTORY PATH SHOULD BE CREATED
            if create_path is True:
                # CREATE PATH
                os.makedirs(path)
            else:
                # DO NOT CREATE > EXIT LOOP
                break

    # RETURN IF DIRECTORY WAS FOUND
    return found


# ----------------------------------------------------------------------
def fileexists(filepath):
    """
    Return a boolean value based on if a file exists.  Notify user
    is not found.

    DESIGN:
    Function designed check if a file exists.  A boolean value is
    returned to the calling program.

    This function expands in the standard os.path.isfile() function in
    that the user is automatically notified if the path does not exist.

    PARAMETERS:
        - filepath
          the file path you are testing

    DEPENDENCIES:
    - os

    USE:
    > import utils3.utils as u
    > if u.fileexists(filepath='/path/to/file.ext'): do stuff ...
    """

    # BUILT-IN IMPORTS
    import os

    # INITIALISE VARIABLE
    found = False

    # TEST IF FILE EXISTS
    if os.path.isfile(filepath):
        # SET FLAG
        found = True
    else:
        # NOTIFY USER
        print('The requested file cannot be found: (%s).\n' % filepath)
        # SET FLAG
        found = False

    # RETURN BOOLEAN TO PROGRAM
    return found


# ----------------------------------------------------------------------
def format_exif_date(datestring, input_format='%Y:%m:%d %H:%M:%S',
                     output_format='%Y%m%d%H%M%S'):
    """
    Return a formatted exif date string.

    DESIGN:
    Function designed to convert the exif date/timestamp
    from 2010:01:31 12:31:18 (or a caller specified) format to a
    format specified by the caller.

    This is useful for storing an exif date as a datetime string.

    PARAMETERS:
    - datestring
    the datetime string to be converted.
    typical exif date format: yyyy:mm:dd hh:mi:ss
    - input_format (default='%Y:%m:%d %H:%M:%S')
    formatting string for the input datetime value.
    - output_format (default='%Y%m%d%H%M%S')
    formatting string for the resulting date time value.

    DEPENDENCIES:
    - datetime

    USE:
    > import utils.utils as u
    > newdate = u.format_exif_date('2010:01:31 12:31:18')
    """

    # BUILT-IN IMPORTS
    from datetime import datetime as dt

    # RETURN FORMATTED STRING
    return dt.strftime(dt.strptime(datestring, input_format), output_format)


# ----------------------------------------------------------------------
def get_os():
    """Return the platform's OS."""

    # BUILT-IN IMPORTS
    import platform

    return platform.system().lower()


# ----------------------------------------------------------------------
def getcolormap(colormap='Blues', n=5, colorscale=False, dtype='hex',
                preview=False, preview_in='mpl'):
    """
    Return a specified matplotlib colour map, as a list or colours.

    DESIGN:
    Function designed to return a list of colour values from a
    matplotlib colormap.  The number of returned colour values can
    range from 1 to 256.

    This is useful when creating a graph which requires gradient
    colour map. (e.g.: a plotly bar chart)

    To print a list of available colour maps:
    > import utils3.utils as u
    > u.listcolormaps()

    PARAMETERS:
        - colormap (default='Blues')
          name of the matplotlib color map
        - n (default=1)
          number of colors to return
        - colorscale (default=False)
          converts the retured colour map into a list of colour scale
          values.  this is useful with Plotly's colorscale parameter.
          returned format: [(0.00, u'#f7fbff'), (0.33, u'#abd0e6'),
                            (0.66, u'#3787c0'), (1.00, u'#08306b')]
        - dtype (default='hex')
          data type to return
        - preview (default=False)
          this option creates a plotly or matplotlib graph displaying
          the colormap.
        - preview_in (default='mpl')
          display method for previewing the graph.
          'mpl' = matplotlib (used for inline preview)
          'plotly' = plotly (use for html display in a web browser)

    DEPENDENCIES:
    - matplotlib

    USE:
    > import utils3.utils as u
    > cmap = u.getcolourmap(colormap='winter',
                            n=50,
                            dtype='hex',
                            preview=True,
                            preview_in='plotly')
    """

    # EXTERNAL IMPORTS
    # RENAME rbg2hex TO AVOID CONFLICT WITH utils.rgb2hex FUNCTION
    from matplotlib import cm
    from matplotlib.colors import rgb2hex as r2h

    # CREATE A COLOR MAP OBJECT (MAP, NUMBER OF VALUES)
    cmap = cm.get_cmap(colormap, n)

    # CONVERT COLORMAP OBJECT INTO LIST OF COLORS
    if dtype.lower() == 'hex':
        # RETURN A LIST OF RGB2HEX CONVERTED COLORS
        colors = [r2h(cmap(i)[:3]) for i in range(cmap.N)]
    else:
        colors = None

    # TEST FOR PREVIEW:
    if colors is not None and preview:
        # MATPLOTLIB
        if preview_in == 'mpl': _prev_mpl(cmap=colors, cmap_name=colormap)
        # PLOTLY
        if preview_in == 'plotly': _prev_plotly(cmap=colors, cmap_name=colormap)

    # TEST FOR COLORSCALE >> RETURN COLOUR MAP OR COLOUR SCALE
    return colors if colorscale is False else _convert_to_colorscale(cmap=colors)


# ----------------------------------------------------------------------
def getdrivername(drivername, returnall=False):
    """
    Return the driver name for an ODBC driver, using a caller provided
    regex pattern.

    DESIGN:
    Helper function designed to get and return the name of an ODBC
    driver.

    The argument can be formatted as a regex expression.  If multiple
    drivers are found, by default, only the first driver in the list is
    returned.
    However, the returnall parameter toggles this action.

    This function has a dependency on pyodbc. Therefore,
    the utils.testimport() function is called before pyodbc it is
    imported. If the pyodbc library is not installed, the user is
    notified.

    PARAMETERS:
        - drivername
          the name of the driver you're looking for. should be
          formatted as regex.
        - returnall (default=False)
          return all drivers found.

    DEPENDENCIES:
    - re
    - pyodbc

    USE:
    > driver = getdrivername(drivername='SQL Server.*')
    """

    # BUILT-IN IMPORTS
    import re

    # TEST FOR LIBRARY BEFORE TRYING TO IMPORT
    if testimport('pyodbc'):

        # EXTERNAL IMPORTS
        import pyodbc

        # TEST IF USER WANTS ALL DRIVERS RETURNED
        if returnall:
            # RETURN ALL
            drivers = [driver for driver in pyodbc.drivers() if re.search(drivername, driver)]
        else:
            # GET THE ODBC DRIVER NAME FOR SQL SERVER
            drivers = [driver for driver in pyodbc.drivers() if re.search(drivername, driver)][0]

        return drivers


# ----------------------------------------------------------------------
def getsitepackages():
    """
    Return the site packages directory, based on platform.

    PURPOSE:
    This function returns the directory path to site-packages based on
    the platform.

    DESIGN:
    The function first uses the local _get_os() function to get the
    platform's base OS.  The OS is then tested and the site-packages
    location is returned using the OS appropriate element from the
    site.getsitepackages() list.

    If the OS is not accounted for, or fails the test, a value of
    'unknown' is returned.

    RATIONALE:
    The need for this function comes out of the observation there are
    many (many!) different ways on stackoverflow (and other sites) to
    get the location to which pip will install a package, and most of
    the answers contradict each other.  Also, the site.getsitepackages()
    function returns a list of two options (in all tested cases); and
    the Linux / Windows paths are in different locations in this list.

    So this function was written to help simplify matters ... hopefully.
    """

    # BUILT-IN IMPORTS
    import site

    # GET PLATFORM
    my_os = get_os()

    # TEST PLATFORM >> GET SITE-PACKAGES DIRECTORY
    if 'win' in my_os:
        sitepkgs_dir = site.getsitepackages()[1]
    elif 'lin' in my_os:
        sitepkgs_dir = site.getsitepackages()[0]
    else:
        sitepkgs_dir = 'unknown'

    return sitepkgs_dir


# ----------------------------------------------------------------------
def json_read(filepath):
    """
    Return JSON file contents as a dictionary.

    DESIGN:
    Function designed to read a JSON file, and return the values as a
    dictionary.

    This utility is useful when reading a json config file for a python
    program.

    PARAMETERS:
        - filepath
          path to the JSON file to read.

    DEPENDENCIES:
    - json

    USE:
    > import utils3.utils as u
    > vals = u.json_read(filepath=/path/to/file.json)
    """

    # BUILT-IN IMPORTS
    import json

    # TEST IF FILE EXISTS
    if fileexists(filepath):

        # OPEN JSON FILE / STORE VALUES TO DICTIONARY
        with open(filepath, 'r') as infile:
            vals = json.load(infile)

        # RETURN DICTIONARY TO PROGRAM
        return vals


# ----------------------------------------------------------------------
def json_write(dictionary, filepath='c:/temp/tempfile.json'):
    """
    Create a JSON file at a specific location based on the contents of
    a caller provided dictionary.

    DESIGN:
    Method designed to write a python dictionary to a JSON file in the
    specified file location.

    If a file is not specified, the default file and location is:
    c:/temp/tempfile.json

    This utility is useful when creating a json config file.

    PARAMETERS:
        - dictionary
          the python dictionary you are converting to a json file.
        - filepath
          the path and filename for the output json file.

    DEPENDENCIES:
    - json

    USE:
    > import utils3.utils as u
    > u.json_write(dictionary=mypy_dict[,
                   filepath='/path/to/output.json'])
    """

    # BUILT-IN IMPORTS
    import json

    # OPEN / WRITE JSON FILE
    with open(filepath, 'w') as outfile:
        json.dump(dictionary, outfile, sort_keys=True)


# ----------------------------------------------------------------------
def listcolormaps():
    """
    Print a list of available matplotlib colour maps.

    PURPOSE:
    A very simple method used to print a list of colour maps available
    in matplotlib.

    DEPENDENCIES:
    - matplotlib

    USE:
    > import utils3.utils as u
    > u.listcolormaps()
    """

    # EXTERNAL IMPORTS
    from matplotlib.pyplot import colormaps

    print(colormaps())


# ----------------------------------------------------------------------
def ping(server, count=1):
    """
    Ping an IP address, server name or web address, and return
    a boolean value based on the result.

    NOTE: Currently, **only Windows is supported**, with a Linux
    update to follow soon.

    DESIGN:
    Using the platform's native 'ping' command (via the subprocess
    package), a server is pinged, and a boolean value is returned to
    the caller to indicate if the server was reached.
    A ping status of 0 = True, and 1 = False.

    If the server name is preceeded by \\ or //, these are stripped out
    using the os.path.basename() function.

    PARAMETERS:
    - server
    This string value can be either an IP address, a server name or a
    web address.
    - count (default=1)
    An integer value indicating the number of ping attempts.
    """

    # BUILT-IN IMPORTS
    import os
    import subprocess

    # INITIALISE
    status = 1
    # GET OS
    my_os = get_os()

    # TEST PLATFORM
    if 'win' in my_os:
        # PING THE SERVER
        status = subprocess.call('ping -n %d %s' % (count, os.path.basename(server)),
                                 stdout=open(os.devnull))
    elif 'lin' in my_os:
        # SET STATUS
        status = 1
        # USER NOTIFICATION
        _UI.print_warning('\nSorry ... this function does not support Linux, yet.\n')

    else:
        # SET STATUS
        status = 1
        # USER NOTIFICATION
        _UI.print_alert('\nSorry, I was unable to identify your OS as either Linux or Windows.\n'
                        'Your OS was identified as: %s\n' % my_os)

    # RETURN BOOLEAN STATUS
    return True if status == 0 else False


# ----------------------------------------------------------------------
def rgb2hex(rgb_string, drop_alpha=False):
    """
    Return a hex string, which was converted from an RGB string.

    DESIGN:
    This function is designed to convert an rgb (or rgba) string to a
    hex string.

    For example: 'rgb(195, 0, 0)' returns #c00000
                 'rgba(65, 125, 50, 0.25)' returns #40417d32

    This is useful as some colour functions return an rgb or rgba
    string, and matplotlib.pyplot only accepts hex strings.

    Regex is used to extract the colour channels from the string.
    Therefore, the 'rgb' or 'rgba' prefix is not required; although
    accepted for standard use.

    The extracted integer values (or float value in the case of alpha),
    are converted to hex and returned as a compiled hex string.

    If an alpha value is present, the alpha value is moved to the first
    byte of the hex string; making the hex string read as #argb.

    PARAMETERS:
        - rgb_string
          This is the rgb or rgba string to convert.
        - drop_alpha (default=False)
          'True' will drop the alpha value from the hex string.
          This is useful for colour maps that automatically return an
          alpha channel, yet the [plotting program] does not accept
          alpha values.

    DEPENDENCIES:
    - re

    USE:
    > import utils3.utils as u
    > clr = u.rgb2hex('rgb(195, 0, 0)')
    """

    # BUILT-IN IMPORTS
    import re

    try:
        # MATCH RGB CHANNELS, AND SEVERAL VARIATIONS OF (INCL OPTIONAL) ALPHA
        # CASE WILL BE IGNORED
        pattern = r'([0-9]{1,3},\s*[0-9]{1,3},\s*[0-9]{1,3}(,\s[0,1]{0,}\.*[0-9]{0,})?)'
        exp = re.compile(pattern, flags=re.IGNORECASE)

        # EXTRACT COLOUR CHANNEL VALUES FROM PASSED STRING
        vals = exp.search(rgb_string).groups()[0].split(',')
        # REMOVE COMMAS FROM EACH STRING & TRIM WHITESPACE
        vals = [val.replace(',', '').strip() for val in vals]

        # TEST IF ALPHA SHOULD BE STRIPPED
        if drop_alpha is True and len(vals) == 4: vals = vals[:3]

        # TEST IF ALPHA CHANNEL PROVIDED
        if len(vals) == 4:
            # TEST IF ALPHA CHANNEL IN FLOAT >> CONVERT TO INTEGER (BETWEEN 0 AND 255)
            vals[3] = int(round(float(vals[3]) * 255, 0)) if 0 <= float(vals[3]) <= 1 else vals[3]

        # CONVERT VALUES FROM STRING TO INT
        ints = [int(i) for i in vals]

        # TEST IF ALPHA CHANNEL PROVIDED
        if len(ints) == 4:
            # MOVE ALPHA CHANNEL TO BEGINNING OF LIST
            ints.insert(0, ints[3])
            # SPLIT CHANELS
            r, g, b, a = [i for i in ints[:4]]
            # CONVERT TO HEX STRING
            xhex = '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b, a)

        # NO ALPHA CHANNEL
        elif len(ints) == 3:
            # SPLIT CHANELS
            r, g, b = [i for i in ints]
            # CONVERT TO HEX STRING
            xhex = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        else:
            # NOTIFY USER OF INCORRECT FORMAT
            raise ValueError('The quantity of integer values to convert must be 3 or 4 values.\n\n'
                             'The colour channel list musts be in this format: '
                             '(r, g, b) or (r, g, b, a) to include the alpha channel.')

        # RETURN CONVERTED HEX VALUE AS STRING
        return str(xhex)

    except Exception as err:
        # NOTIFICATION
        reporterror.reporterror(err)


# ----------------------------------------------------------------------
def testimport(module_name):
    """
    Return a boolean value based on if a Python module was found.

    DESIGN:
    This is a small helper function designed to test if a
    module/library is installed before trying to import it.

    This can be useful when a method requires an 'obscure' library, and
    importing on a deployment environment where the library is not
    installed, could have adverse effects.

    If the library is not intalled, the user is notified.

    PARAMETERS:
        - module_name
          the name of the module you're testing is installed.

    DEPENDENCIES:
    - imp

    USE:
    > import utils3.utils as u
    > if u.testimport('mymodule'): import mymodule
    """

    # BUILT-IN IMPORTS
    import imp

    # INITIALISE
    found = False

    try:
        # TRY TO IMPORT MODULE
        imp.find_module(module_name)
        found = True
    except ImportError:
        # MODULE NOT FOUND
        found = False
        print('\nSorry ... the (%s) library/module is not installed.' % (module_name))

    return found


# ----------------------------------------------------------------------
def unidecode(string):
    """
    Return a unicode decoded string.

    DESIGN:
    Method designed to test a passed string for being unicode type,
    then return a decoded string value.

    If the passed string is not unicode, the original value is
    returned.

    PARAMETERS:
        - string
          the unicode string you wish to test/decode.

    DEPENDENCIES:
    - unidecode

    USE:
    > import utils3.utils as u
    > s = u.unidecode(string)
    """

    # EXTERNAL IMPORTS
    # RENAME unidecode TO AVOID CONFLICT WITH utils.unidecode FUNCTION
    from unidecode import unidecode as uni

    # INITIALISE VARIABLE
    decoded = None

    # TEST PASSED VALUE AS BEING UNICODE > STORE DECODED (OR ORIGINAL) VALUE
    decoded = uni(string) if isinstance(string) else string

    # RETURN VALUE
    return decoded


# ----------------------------------------------------------------------
def _dbconn_mysql_conn(creds):
    """
    Return a dictionary containing the connection and cursor objects
    for a MySQL database connection.

    PURPOSE:
    This function is used to make a connection to a MySQL database.

    DESIGN:
    The passed credential dictionary is passed directly into the
    mysql.connect function as a set of **kwargs.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    """

    # EXTERNAL IMPORTS
    import mysql.connector as sql

    try:
        # CREATE CONNECTION / CURSOR OBJECTS
        connection = sql.connect(**creds)
        cursor = connection.cursor()

        # RETURN THE CONN/CUR OBJECTS IN A DICT
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)


# ----------------------------------------------------------------------
def _dbconn_oracle_conn(creds):
    """
    Return a dictionary containing the connection and cursor objects
    for an Oracle database connection.

    PURPOSE:
    This function is used to make a connection to an Oracle database.

    DESIGN:
    Using a passed credential dictionary, an Oracle connection string
    is built and used for connection.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    """

    # EXTERNAL IMPORTS
    import cx_Oracle

    try:
        # BUILD CONNECTION STRING
        connstring = '%s/%s@%s' % (creds['user'], creds['password'], creds['host'])

        # MAKE THE CONNECTION >> GET CURSOR OBJECT
        connection = cx_Oracle.connect(connstring)
        cursor = connection.cursor()

        # RETURN THE CONN/CUR OBJECTS IN A DICT
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)


# ----------------------------------------------------------------------
def _dbconn_sql_conn(creds):
    """
    Return a dictionary containing the connection and cursor objects
    for a SQL Server database connection.

    PURPOSE:
    This function is used to make a connection to a SQL Server database.

    DESIGN:
    The database credentials are passed into the pyodbc library, which
    searches for the SQL Server driver, via the getdrivername()
    function.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    """

    # EXTERNAL IMPORTS
    import pyodbc

    try:
        # BUILD CONNECTION STRING >> CONNECT
        connection = pyodbc.connect('Driver={%s};'
                                    'Server=%s;'
                                    'Database=%s;'
                                    'UID=%s;'
                                    'PWD=%s;' %
                                    (getdrivername('SQL Server.*'),
                                     creds['server'],
                                     creds['database'],
                                     creds['user'],
                                     creds['password']))

        # CREATE CURSOR OBJECT
        cursor = connection.cursor()

        # STORE RESULT IN DICTIONARY
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)



# ----------------------------------------------------------------------
def _dbconn_fields(dbtype, fields, filename):
    """
    Return a dictionary of database login credentials, based on a
    fields from a JSON config file.

    PURPOSE:
    This is a general-purpose function used to extract database
    credentials from a passed JSON config file.

    DESIGN:
    Using the passed file, the config key/values are loaded into a
    dictionary which is iterated, testing if the expected fields are
    present.  If an expected field is not present, the user is prompted
    for the value.

    The completed credential dictionary is then returned.
    """

    try:
        # INITIALISE
        creds = dict()

        # LOAD CONNECTION DETAILS FROM CONFIG FILE
        conf = config.loadconfig(filename=filename)

        # LOOP THROUGH EXPECTED KEYS
        for key in fields:
            # TEST KEY EXISTS IN CONFIG FILE
            if conf.has_key(key):
                # ADD EXISTING VALUE TO CREDENTIAL DICT (USED FOR CONNECTION)
                creds[key] = conf[key]
            else:
                # PROMPT FOR VALUE >> ADD TO CREDENTIAL DICT
                creds[key] = six.moves.input('Please enter the %s %s: ' % (dbtype, key))

        # RETURN DICTIONARY OF CREDENTIALS
        return creds

    except Exception as err:
        # USER NOTIFICATION
        _UI.print_alert('\nAn error occurred while checking the database credentials in the '
                        'config file.\nFilename used: %s' % filename)
        _UI.print_error(err)
        return None


# ----------------------------------------------------------------------
def _dbconn_params(dbtype, **params):
    """
    Return a dictionary of database login credentials, based on
    the parameters provided by the caller.

    PURPOSE:
    This is a general-purpose function used to test if the provided
    database credential parameters have been populated.

    DESIGN:
    This function iterates over the passed credential fields (passed as
    **kwargs), and tests each field for a None value.  If a None value
    is found, the user is prompted for the credential.

    The completed credential dictionary is then returned.
    """

    try:
        # LOOP THROUGH KEYS AND GET MISSING VALUES
        for key, _ in params.items():
            # TEST VALUE
            if params[key] is None:
                # PROMPT USER FOR VALUE
                params[key] = six.moves.input('Please enter the %s for the %s connection: ' % (key, dbtype))

        # RETURN COMPLETED DICTIONARY
        return params

    except Exception as err:
        # USER NOTIFICATION
        _UI.print_alert('\nAn error occurred while checking the passed database credentials.')
        _UI.print_error(err)
        return None


# ----------------------------------------------------------------------
def _convert_to_colorscale(cmap):
    """
    Return a colour scale list, as converted from a colour map.

    PURPOSE:
    This is a helper function used to convert a colour map into a
    colour scale list, as used by the Plotly colorscale parameter.

    DESIGN:
    Returned format: [(0.00, u'#f7fbff'), (0.33, u'#abd0e6'),
                      (0.66, u'#3787c0'), (1.00, u'#08306b')]

    DEPENDENCIES:
    - numpy
    """

    # EXTERNAL IMPORTS
    import numpy as np

    return [i for i in zip(np.linspace(0, 1, num=len(cmap)), cmap)]


# ----------------------------------------------------------------------
def _prev_mpl(cmap, cmap_name):
    """
    Preview a colour map using matplotlib.

    DESIGN:
    This method is designed to be called form the getcolormap()
    function, as a means of displaying / previewing the colour map
    chosen, using the matplotlib plotting library.

    ADVANTAGE:
    This method displays the colour map preview directly within the
    [Sypder] IDE, Jupyter Notebook.

    PARAMETERS:
    - cmap
      The colour map you want to preview.  This must be a python list of
      rgb/rgba/hex values.
    - cmap_name
      The name of the matplotlib colour map.  (e.g.: OrRd, winter, etc.)
      This name is only used to display the colour map name in the
      graph title.

    DEPENDENCIES:
    - matplotlib
    """

    # EXTERNAL IMPORTS
    import matplotlib.pyplot as plt

    # CREATE GRAPH DATA
    n = len(cmap)
    x = range(0, n)
    y = [10]*n

    # CREATE IMAGE
    plt.figure(facecolor='black')
    plt.bar(x, y, width=15, linewidth=0, color=cmap)
    plt.title('COLOUR MAP NAME: %s' % cmap_name, color='w', size=12)
    plt.xlim(0, n)
    plt.ylim(0, 10)
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off')
    plt.xticks(color='w', size=12)
    # TURN OFF BORDER
    for spine in plt.gca().spines.values(): spine.set_visible(False)
    # DISPLAY GRAPH
    plt.show()


# ----------------------------------------------------------------------
def _prev_plotly(cmap, cmap_name, out_file='c:/temp/cmap_graph.html'):
    """
    Preview a colour map (bar graph) using Plotly.

    DESIGN:
    This method is designed to be called form the getcolormap()
    function, as a means of displaying / previewing the colour map
    chosen, using the plotly library.

    ADVANTAGE:
    This method displays the hex/rgb/rgba colour code value for each
    bar as hovertext.

    PARAMETERS:
    - cmap
      The colour map you want to preview.  This must be a python list of
      rgb/rgba/hex values.
    - cmap_name
      The name of the matplotlib colour map.  (e.g.: OrRd, winter, etc.)
      This name is only used to display the colour map name in the
      graph title.
    - out_file (default='c:/temp/cmap_graph.html')
      File path/name for the html graph output; if you wish to save
      the file.

    DEPENDENCIES:
    - plotly >= 2.0.6
    """

    # TEST IF PLOTLY HAS BEEN INSTALLED
    if testimport('plotly'):

        # EXTERNAL IMPORTS
        from plotly.offline import plot
        import plotly.graph_objs as go

        # CREATE GRAPH DATA
        n = len(cmap)
        x = range(1, n+1)
        y = [10]*n
        grey = 'rgb(165, 165, 165)'

        # CREATE LAYOUT
        layout = go.Layout(title='COLOUR MAP NAME: %s' % (cmap_name), titlefont=dict(color=grey, size=20))
        # CREATE BAR GRAPH
        bar1 = go.Bar(x=x, y=y, text=cmap, marker=dict(color=cmap))

        # EDIT AXES
        layout['xaxis'].update(zeroline=False, showgrid=False, tickfont=dict(color=grey))
        layout['yaxis'].update(zeroline=False, showgrid=False, showticklabels=False)

        # COMPILE AND PLOT
        fig = go.Figure(data=[bar1], layout=layout)
        plot(fig, filename=out_file, show_link=False)


# ----------------------------------------------------------------------
def __test():
    """Print a test statement.  Used for testing only."""

    print('This is only a test.')
