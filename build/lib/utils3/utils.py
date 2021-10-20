# -*- coding: utf-8 -*-
"""
:Purpose:   Central library for standard S3DEV utilities.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Example:
    View the module help::

        import utils3.utils as u

        help(u)

    Get the package version::

        import utils3.utils as u

        u.__version__

"""
# For Linux checks.
# pylint: disable=import-error
# pylint: disable=import-outside-toplevel

# AS THIS IS A UTILITIES PACKAGE, NOT ALL IMPORTS ARE USED DURING
# EXECUTION, SO MOST IMPORTS SIT WITH THE METHOD OR FUNCTION IN WHICH
# THEY ARE USED.

import six
from utils3 import config
from utils3 import reporterror
from utils3 import user_interface
from utils3._version import __version__

# PRIVATE GLOBAL CLASS INSTANTIATIONS
_UI = user_interface.UserInterface()

# ----------------------------------------------------------------------
def clean_df(df):
    """Return a cleaned Pandas DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be cleaned.

    :Design:
        This function performs the following cleaning tasks:

            - column names: replace a space with an underscore
            - column names: convert to lower case
            - values:       strip whitespace

    :Example:
        ::

            import utils3.utils as u
            df = u.clean_df(df)

    Returns:
        A 'cleaned' copy of the dataframe.

    """
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
    # pylint: disable=line-too-long
    """Return MySQL database connection and cursor objects.

    Warning:
        This function **should not be interacted with directly**.
        Rather, use the parent class: :class:`~database.MySQL`.

        **Refer to the use example in the class.**

    Args:
        host (str): IP address or machine name of the host or database
            server.
        user (str): User name used to authenticate.
        password (str): Just what it says on the tin.  :-)
        database (str): Name of the database to connect.
        port (int): The TCP/IP port of the MySQL server; must be an
            integer.
        from_file (bool): Boolean flag instructing the function to use
            the provided config (JSON) file for connection details.

                - **Valid keys:** user, password, database, host, port

        filename (str): Full file path to the JSON file containing the
            connection details.

    Note:
        To prompt for login details, leave the argument(s) blank.

    :Design:
        This function is designed to to create a connection to a MySQL
        database using either the provided login details, or directly
        from a config file.  If a login detail is not provided, the
        end-user is prompted; which can be used as a security feature.

        Once all credentials are gathered, the connection is tested.  If
        successful, the connection and cursor objects are returned to the
        calling program, as a dictionary::

            {conn:<the connection object>,
             cur:<the cursor object>}

    :Dependencies:
        - mysql-connector (2.1.4)

        Installation::

            pip install mysql-connector==2.1.4

    :Example 1:
        To connect using **passed connection details**::

            import utils3.utils as u
            dbo = u.dbconn_mysql(host, user, password, database)
            conn = dbo['conn']
            cur = dbo['cur']

    :Example 2:
        To connect using **a config file**::

            import utils3.utils as u
            dbo = u.dbconn_mysql(from_file=True, filename='db_config.json')
            conn = dbo['conn']
            cur = dbo['cur']

    :Source:
        Refer here for the `mysql.connection` `argument keys`_.

    .. _argument keys: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html


    """
    try:
        # INITIALISE
        creds = dict()
        dbtype = 'mysql'
        conn = None

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
            conn = _dbconn_mysql_conn(creds=creds)

        return conn

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the MySQL database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_oracle(host=None, user=None, userid=None, password=None,
                  from_file=False, filename=None):
    """Return Oracle database connection and cursor objects.

    Warning:
        This function **should not be interacted with directly**.
        Rather, use the parent class: :class:`~database.Oracle`.

        **Refer to the use example in the class.**

    Args:
        host (str): Database host; or database name.
        user (str): User name, or schema name.
        userid (str): Same as ``user`` parameter.  (Both are not
               required, but included for backwards-compatibility)
        password (str): Just what it says on the tin.  :-)
        from_file (bool): Boolean flag instructing the function to use
            the provided config (JSON) file for connection details.

                - **Valid keys:** host, user, password

        filename (str): Full file path to the JSON file containing the
            connection details

    Note:
        To prompt for login details, leave the argument(s) blank.

    :Design:
        Function designed to create a connection to an Oracle database
        using either the provided login details, or directly from a
        config file. If a login detail is not provided, the user is
        prompted; which can be used as a security feature.

        The connection is tested.  If successful, the connection and
        cursor objects are returned to the calling program, as a
        dictionary::

            {conn:<the connection object>,
             cur:<the cursor object>}

    :Dependencies:
        - cx_Oracle

    :Example 1:
        To connect using **passed connection details**::

            import utils3.utils as u
            dbo = u.dbconn_oracle(host='myhost', userid='myuser',
                                  password='mypass')
            conn = dbo['conn']
            cur = dbo['cur']

    :Example 2:
        To connect using **a config file**::

            import utils3.utils as u
            dbo = u.dbconn_oracle(from_file=True, filename='db_config.json')
            conn = dbo['conn']
            cur = dbo['cur']

    """
    try:
        # INITIALISE
        creds = dict()
        dbtype = 'oracle'
        conn = None

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
            conn = _dbconn_oracle_conn(creds=creds)

        return conn

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the Oracle database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_sql(server=None, database=None, userid=None, user=None,
               password=None, from_file=False, filename=None):
    """Return SQL Server database connection and cursor objects.

    Warning:
        This function **should not be interacted with directly**.
        Rather, use the parent class: :class:`~database.SQLServer`.

        **Refer to the use example in the class.**

    Args:
        server (str): Name of the server on which the database lives.
        database (str): Name of the database to which you're connecting.
        user (str): User name used to authenticate.
        userid (str): Same as ``user`` parameter.  (Both are not
               required, but included for backwards-compatibility)
        password (str): Just what it says on the tin.  :-)
        from_file (bool): Boolean flag instructing the function to use
            the provided config (JSON) file for connection details.

                - **Valid keys:** server, database, user, password

        filename (str): Full file path to the JSON file containing the
            connection details.

    Note:
        To prompt for login details, leave the argument(s) blank.

    :Design:
        Function designed to create a connection to a SQL Server database
        using the either provided login parameters, or directly from a
        config file. If a login detail is not provided, the user is
        prompted; which can be used as a security feature.

        The connection is tested.  If successful, the connection and
        cursor objects are returned to the calling program, as a
        dictionary::

            {conn:<the connection object>,
             cur:<the cursor object>}

    :Dependencies:
        - pyodbc

    :Example 1:
        To connect using **passed connection details**::

            import utils3.utils as u
            dbo = u.dbconn_sql(server, database, user, password)
            conn = dbo['conn']
            cur = dbo['cur']

    :Example 1:
        To connect using **a config file**::

            import utils3.utils as u
            dbo = u.dbconn_sql(from_file=True, filename='db_config.json')
            conn = dbo['conn']
            cur = dbo['cur']

    """
    try:
        # INITIALISE
        creds = dict()
        dbtype = 'sql_server'
        conn = None

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
            conn = _dbconn_sql_conn(creds=creds)

        return conn

    except Exception as err:
        # ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the SQL Server database.')
        _UI.print_error(err)


# ----------------------------------------------------------------------
def dbconn_sqlite(db_path):
    """Return SQLite database connection and cursor objects.

    Warning:
        This function **should not be interacted with directly**.
        Rather, use the parent class: :class:`~database.SQLite`.

        **Refer to the use example in the class.**

    :Design:
        Function designed to create and return database connection and
        cursor objects for a SQLite database, using the passed database
        filename::

            {conn:<the connection object>,
             cur:<the cursor object>}

    Args:
        db_path (str): Full file path to the SQLite database file.

    :Dependencies:
        - sqlite3

    :Example:
        To connect::

            import utils3.utils as u
            dbo = u.dbconn_sqlite(db_path)
            conn = dbo['conn']
            cur = dbo['cur']

    """
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
def direxists(path, create_path=True) -> bool:
    """Test if a directory exists.  If not, create it, if instructed.

    Args:
        path (str): The directory path to be tested.
        create_path (bool): Create the path if it doesn't exist.

    :Design:
        Function designed to test if a directory path exists.  If the
        path does not exist, the path can be created; as determined by
        the ``create_path`` parameter.

        This function expands in the standard ``os.path.exists()``
        function in that the path can be created if it doesn't already
        exist, by passing the ``create_path`` parameter as ``True``;
        which is the default action.

    :Example:
        ::

            import utils3.utils as u
            u.direxists(path='/my/path/to_create', create_path=True)

    Returns:
        True if the directory exists, otherwise False.

    """
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
def fileexists(filepath) -> bool:
    """Test if a file exists.  If not, notify the user.

    Args:
        filepath (str): Full file path to test.

    :Design:
        Function designed check if a file exists.  A boolean value is
        returned to the calling program.

        This function expands in the standard ``os.path.isfile()``
        function in that the user is notified if the path does not
        exist.

    :Example:
        ::

            import utils3.utils as u
            if u.fileexists(filepath='/path/to/file.ext'):
                do stuff ...
            else:
                dont do stuff

    Returns:
        True if the file exists, otherwise False.

    """
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
                     output_format='%Y%m%d%H%M%S') -> str:
    """Format an exif timestamp.

    Args:
        datestring (str): The datetime string to be formatted.
            A typical exif date format is: yyyy:mm:dd hh:mi:ss
        input_format (str): Format mask for the value passed to the
            ``datetime`` parameter
        output_format (str): Convert to this format.

    :Design:
        Function designed to convert the exif date/timestamp
        from 2010:01:31 12:31:18 (or a caller specified) format to a
        format specified by the caller.

        This is useful for storing an exif date as a datetime string.

    :Example:
        ::

            import utils3.utils as u
            newdate = u.format_exif_date('2010:01:31 12:31:18')

    Returns:
        A formatted datetime string.

    """
    from datetime import datetime as dt

    # RETURN FORMATTED STRING
    return dt.strftime(dt.strptime(datestring, input_format), output_format)


# ----------------------------------------------------------------------
def get_os() -> str:
    """Get the platform's general OS.

    :Example:
        ::

            import utils3.utils as u
            my_os = u.get_os()

    Returns:
        A string of the platform's general OS.

    """
    import platform

    return platform.system().lower()


# ----------------------------------------------------------------------
def getcolormap(colormap='Blues', n=5, colorscale=False, dtype='hex',
                preview=False, preview_in='mpl'):
    """Return a specified matplotlib colour map, as a list or colours.

    Args:
        colormap (str): Name of the matplotlib color map.
        n (int): Number of colors to return.
        colorscale (bool): Convert the returned colour map into a list
            of colour scale values.  This is useful with Plotly's
            colorscale parameter.  Returned format::

                [(0.00, u'#f7fbff'), (0.33, u'#abd0e6'),
                 (0.66, u'#3787c0'), (1.00, u'#08306b')]

        dtype (str): Data type to return.

            Note:
                Current only "hex" is supported.

        preview (bool): This option creates a plotly or matplotlib
            graph displaying the colormap.
        preview_in (str): Display method for previewing the graph.

            * 'mpl' = matplotlib (used for inline preview)
            * 'plotly' = plotly (use for html display in a web browser)

    :Design:
        Function designed to return a list of colour values from a
        matplotlib colormap.  The number of returned colour values can
        range from 1 to 256.

        This is useful when creating a graph which requires gradient
        colour map. (e.g.: a plotly bar chart)

        To print a list of available colour maps::

            import utils3.utils as u
            u.listcolormaps()

    :Dependencies:
        - matplotlib

    :Example:
        ::

            > import utils3.utils as u
            > cmap = u.getcolourmap(colormap='winter',
                                    n=50,
                                    dtype='hex',
                                    preview=True,
                                    preview_in='plotly')

    Returns:
        A list of colours.

    """
    # RENAME rbg2hex TO AVOID CONFLICT WITH utils.rgb2hex FUNCTION
    from matplotlib import cm
    from matplotlib.colors import rgb2hex as r2h

    # DEPRECATION NOTICE
    print('\nDeprecation Warning: This function has been deprecated and '
          'will be removed in future versions.\nFor colourmap access, '
          'refer to the ``utils3.cmaps`` module.')

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
    result = colors if colorscale is False else _convert_to_colorscale(cmap=colors)

    return result


# ----------------------------------------------------------------------
def getdrivername(drivername, returnall=False) -> list:
    """Return a list of ODBC driver names, matching the regex pattern.

    Args:
        drivername (str): A **regex pattern** for the ODBC driver you're
            searching.
        returnall (bool): Return **all** drivers found.  By default,
            only the first hit is returned.

    :Design:
        This is a helper function designed to get and return the name
        of an ODBC driver.

        The ``drivername`` parameter should be formatted as a regex
        pattern. If multiple drivers are found, by default, only the
        first driver in the list is returned.  However, the
        ``returnall`` parameter adjusts this action.

        This function has a dependency on ``pyodbc``. Therefore,
        the :func:`~utils.testimport()` function is called before
        ``pyodbc`` is imported. If the ``pyodbc`` library is not
        installed, the user is notified.

    :Dependencies:
        - pyodbc

    :Example:
        ::

            import utils3.utils as u
            driver = u.getdrivername(drivername='SQL Server.*')

    Returns:
        A list of ODBC drivers.

    """
    import re

    # INITIALISE
    drivers = []

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
def getsitepackages() -> str:
    """Return the site packages directory, based on platform.

    :Purpose:
        This function returns the directory path to site-packages
        based on the platform.

    :Design:
        The function first uses the local :func:`~utils.get_os()`
        function to get the platform's base OS.  The OS is then tested
        and the site-packages location is returned using the OS
        appropriate element from the ``site.getsitepackages()`` list.

        If the OS is not accounted for, or fails the test, a value of
        'unknown' is returned.

    :Rationale:
        The need for this function comes out of the observation there
        are many (many!) different ways on stackoverflow (and other
        sites) to get the location to which ``pip`` will install a
        package, and many of the answers contradict each other.  Also,
        the ``site.getsitepackages()`` function returns a list of two
        options (in all tested cases); and the Linux / Windows paths
        are in different locations in this list.

        So this function was written to help simplify matters ...
        hopefully.

    :Example:
        ::

            import utils3.utils as u
            my_sitepkgs = u.getsitepackages()

    Returns:
        The path to the ``site-packages`` directory.

    """
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
def json_read(filepath) -> dict:
    """Return JSON file contents as a dictionary.

    Args:
        filepath (str): Full file path to the JSON file to read.

    :Design:
        Function designed to read a JSON file, and return the values
        as a dictionary.

        This utility is useful when reading a JSON config file for a
        Python program.

    :Example:
        ::

            import utils3.utils as u
            vals = u.json_read(filepath=/path/to/file.json)

    Returns:
        A dictionary containing the JSON file's key/value pairs.

    """
    import json

    # INITIALISE
    vals = {}

    # TEST IF FILE EXISTS
    if fileexists(filepath):
        # OPEN JSON FILE / STORE VALUES TO DICTIONARY
        with open(filepath, 'r') as infile:
            vals = json.load(infile)

    # RETURN DICTIONARY OF RESULT
    return vals


# ----------------------------------------------------------------------
def json_write(dictionary, filepath='c:/temp/tempfile.json'):
    """Create a JSON file at a given file path.

    Args:
        dictionary (dict): The Python dictionary you are converting to
            a JSON file.
        filepath (str): Full file path to store the JSON file.

    :Design:
        Method designed to write a Python dictionary to a JSON file in
        the specified file location.  If a file location is not
        specified, the default file and location is used.

        This utility is useful when creating a JSON config file.

    :Example:
        ::

            import utils3.utils as u
            u.json_write(dictionary=my_dict, filepath='/path/to/output.json')

    """
    import json

    # OPEN / WRITE JSON FILE
    with open(filepath, 'w') as outfile:
        json.dump(dictionary, outfile, sort_keys=True)


# ----------------------------------------------------------------------
def listcolormaps():
    """Print a list of available matplotlib colour maps.

    :Purpose:
        A very simple method used to print a list of colour maps
        available in matplotlib.

    :Dependencies:
        - matplotlib

    :Example:
        ::

            import utils3.utils as u
            u.listcolormaps()

    """
    from matplotlib.pyplot import colormaps

    print(colormaps())

    # DEPRECATION NOTICE
    print('\nDeprecation Warning: This function has been deprecated and '
          'will be removed in future versions.\nFor colourmap access, '
          'refer to the ``utils3.cmaps`` module.')


# ----------------------------------------------------------------------
def ping(server, count=1) -> bool:
    r"""Ping an IP address, server or web address.

    Args:
        server (str): Either an IP address, a server name or a web
            address.
        count (int): The number of ping attempts.

    Note:
        Currently, **only Windows is supported**, with a Linux update
        to follow.

    :Design:
        Using the platform's native 'ping' command (via the
        ``subprocess`` package), a server is pinged, and a boolean
        value is returned to the caller to indicate if the ping was
        successful.

        A ping status of ``0 = True``, and ``1 = False``.

        If the server name is preceeded by ``\\`` or ``//``, these are
        stripped out using the ``os.path.basename()`` function.

    Returns:
        True if the ping was successful, otherwise False.

    """
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
def rgb2hex(rgb_string, drop_alpha=False) -> str:
    """Convert an RGB string to HEX.

    Args:
        rgb_string (str): This is the RGB or RGBA string to convert.
        drop_alpha (bool): ``True`` will **drop the alpha value** from
            the HEX string.  This is useful for colour maps that
            automatically return an alpha channel, yet the
            plotting program does not accept alpha values.

    :Design:
        This function is designed to convert an RGB (or RGBA) string to
        a HEX string.

        For example: 'rgb(195, 0, 0)' returns #c30000
                     'rgba(65, 125, 50, 0.25)' returns #40417d32

        This is useful as some colour functions return an RGB or RGBA
        string, and ``matplotlib.pyplot`` **only accepts HEX strings**.

        Regex is used to extract the colour channels from the string.
        Therefore, the 'rgb' or 'rgba' prefix **is not required**;
        although accepted for standard use.

        The extracted integer values (or float value in the case of
        alpha), are converted to HEX and returned as a compiled HEX
        string.

        If an alpha value is present, the alpha value is moved to the
        first byte of the HEX string; making the HEX string read as
        #argb.

    :Example:
        ::

            import utils3.utils as u
            clr = u.rgb2hex('rgb(195, 0, 0)')

    Returns:
        A HEX string; i.e. ``#c30000``.

    """
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
def testimport(module_name) -> bool:
    """Test if a Python library is installed.

    For example, the :func:`~utils.getdrivername` function uses this
    function before attempting to import the ``pyodbc`` library.

    Args:
        module_name (str): The name of the module to be found.

    :Design:
        This is a small helper function designed to test if a library
        is installed before trying to import it.

        If the library is not intalled, the user is notified.

    :Dependencies:

        * importlib

    :Example:
        ::

            import utils3.utils as u
            if u.testimport('mymodule'): import mymodule

    Returns:
        True if the library was found, otherwise False.

    """
    import importlib

    try:
        result = importlib.util.find_spec(module_name)
        found = result is not None
        if not found:
            print('\nSorry ... the (%s) library/module is not installed.' % (module_name))
    except ImportError as err:
        found = False
        print('ImportError: %s' % (err))
    return found


# ----------------------------------------------------------------------
def unidecode(string) -> str:
    """Attempt to convert a Unicode object into an ASCII string.

    Args:
        string (str): The string to be decoded.

    :Design:
        This function is a light wrapper around the
        ``unidecode.unidecode`` function.

        **Per the** ``unicode`` **docstring:**

        "Transliterate an Unicode object into an ASCII string.

        >>> unidecode(u"北亰")
        "Bei Jing "

        This function first tries to convert the string using ASCII
        codec. If it fails (because of non-ASCII characters), it falls
        back to transliteration using the character tables.

        This is approx. five times faster if the string only contains
        ASCII characters, but slightly slower than using unidecode
        directly if non-ASCII chars are present."

    :Dependencies:

        * unidecode

    :Example:
        ::

            import utils3.utils as u
            s = u.unidecode(string)

    Returns:
        If the passed ``string`` value is a str data type, the decoded
        string is returned, otherwise the original value is returned.

    """
    # EXTERNAL IMPORTS
    # RENAME unidecode TO AVOID CONFLICT WITH utils.unidecode FUNCTION
    from unidecode import unidecode as uni

    # INITIALISE VARIABLE
    decoded = None
    # TEST PASSED VALUE AS BEING A STRING >> STORE DECODED (OR ORIGINAL) VALUE
    decoded = uni(string) if isinstance(string, str) else string

    # RETURN VALUE
    return decoded


# ----------------------------------------------------------------------
def _dbconn_mysql_conn(creds):
    r"""Create the MySQL connection and cursor objects.

    Args:
        creds (dict): Database connection credentials.

    :Design:
        The ``creds`` dictionary argument is passed directly to the
        ``mysql.connector.connect`` function as a set of \*\*kwargs.

    Note:
        This is the connection handler and error trapper for the
        :class:`~database.MySQL` database connection class.

    Returns:
        Upon successful connection, the function returns the database
        connection and cursor objects, wrapped in a dictionary.

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
    """Create the Oracle database connection and cursor objects.

    Args:
        creds (dict): Database connection credentials.

    :Design:
        The ``creds`` dictionary argument is parsed into a connection
        string and passed into the ``cx_Oracle.connect`` function.
        Then, the returned connection and cursor objects are wrapped
        into a dictionary and returned.

    Note:
        This is the connection handler and error trapper for the
        :class:`~database.Oracle` database connection class.

    Returns:
        Upon successful connection, the function returns the database
        connection and cursor objects, wrapped in a dictionary.

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
    """Create the SQL Server database connection and cursor objects.

    Args:
        creds (dict): Database connection credentials.

    :Design:
        When building the connection string, the
        :func:`utils.getdrivername` function is used to get the name of
        the odbc driver.  Then, the ``creds`` dictionary argument is
        parsed into a connection string (including the found driver
        name) and passed into the ``pyodbc.connect`` function.

    Note:
        This is the connection handler and error trapper for the
        :class:`~database.SQLServer` database connection class.

    Returns:
        Upon successful connection, the function returns the database
        connection and cursor objects, wrapped in a dictionary.

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
    """Extract database credentials from a JSON file, prompt for
    missing values.

    Args:
        dbtype (str): Type of the database being connected.
        fields (list): List of credentials to test.
            For example::

                ['server', 'user', 'password', 'port']

        filename (str): Full file path to the credentials JSON file.

    :Design:
        Using the passed file, the config key/value pairs are loaded
        into a dictionary where a test is made to determine if the
        expected fields (as defined by the ``fields`` argument) is
        present.  If an expected field is missing, the user is prompted
        for the value.

    Note:
        This function handles the **credential file parsing** and
        **credential prompting** for the following classes:

            * :class:`~database.MySQL`
            * :class:`~database.Oracle`
            * :class:`~database.SQLServer`

    Returns:
        A completed credential dictionary.

    """
    try:
        # INITIALISE
        creds = dict()
        # LOAD CONNECTION DETAILS FROM CONFIG FILE
        conf = config.loadconfig(filename=filename)
        # LOOP THROUGH EXPECTED KEYS
        for key in fields:
            # TEST KEY EXISTS IN CONFIG FILE
            if key in conf:
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
    r"""Build a dictionary of database login credentials, prompt for
    missing values.

    Args:
        dbtype (str): Type of the database being connected.
        **params (dict): Key/value pairs for connection credentials.

    :Design:
        This function tests each passed credential field
        (passed as \*\*kwargs), if any keys are missing a value, the user
        is prompted for the credential.

    Note:
        This function handles the **credential prompting** for the
        following classes:

            * :class:`~database.MySQL`
            * :class:`~database.Oracle`
            * :class:`~database.SQLServer`

    Returns:
        A completed credential dictionary.

    """
    try:
        # LOOP THROUGH KEYS AND GET MISSING VALUES
        for key, _ in params.items():
            # TEST VALUE
            if params[key] is None:
                # PROMPT USER FOR VALUE
                params[key] = six.moves.input('Please enter the %s for the %s connection: ' %
                                              (key, dbtype))
        # RETURN COMPLETED DICTIONARY
        return params
    except Exception as err:
        # USER NOTIFICATION
        _UI.print_alert('\nAn error occurred while checking the passed database credentials.')
        _UI.print_error(err)
        return None


# ----------------------------------------------------------------------
def _convert_to_colorscale(cmap) -> list:
    """Convert a matplotlib colourmap to a colourscale list.

    This is a helper function used to convert a colourmap into a
    colourscale list, as used by Plotly's colorscale parameter.

    A colourscale list is a list of tuples where the first index of the
    tuple is a value between 0 and 1 (inclusive), showing the order of
    the colour in sequence, and the second index is the colour value,
    as shown below::

        [(0.00, u'#f7fbff'),
         (0.33, u'#abd0e6'),
         (0.66, u'#3787c0'),
         (1.00, u'#08306b')]

    Args:
        cmap (matplotlib.colors.LinearSegmentedColormap): A matplotlib
            colourmap.

    :Help:
        The ``cmap`` object may be generated this way::

            from matplotlib import cm
            cmap = cm.get_cmap('Blues', 5)

    :Dependencies:

        * numpy

    Returns:
        A list of colourscale tuples for the given colour map.

    """
    # EXTERNAL IMPORTS
    import numpy as np

    return [i for i in zip(np.linspace(0, 1, num=len(cmap)), cmap)]


# ----------------------------------------------------------------------
def _prev_mpl(cmap, cmap_name):
    """Preview a colourmap using matplotlib.

    Args:
        cmap (list): The colour map you want to preview.  This must be
            a Python list of rgb/rgba/hex values.
        cmap_name (str): The name of the matplotlib colour map.
            For example: (Blues, OrRd, winter, etc.)  This name is only
            used to **display** the colour map name in the graph title.

    :Design:
        This helper method is designed to be called from the
        :func:`~utils.getcolormap` function, as a means of
        displaying / previewing the colour map chosen, using the
        ``matplotlib`` plotting library.

    :Advantage:
        This method allows you to **preview the colourmap directly
        within the IDE**; e.g.: Spyder, Jupyter Notebook, etc.

    :Dependencies:

        * matplotlib

    """
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
    """Preview a colourmap, as a bar graph, in Plotly.

    Args:
        cmap (list): The colour map you want to preview.  This must be
            a Python list of rgb/rgba/hex values.
        cmap_name (str): The name of the matplotlib colour map.
            For example: (Blues, OrRd, winter, etc.)  This name is only
            used to **display** the colour map name in the graph title.
        out_file (str): Full file path to the output HTML file.

    :Design:
        This helper method is designed to be called from the
        :func:`~utils.getcolormap` function, as a means of
        displaying / previewing the colour map chosen, using the
        ``plotly`` plotting library.

    :Advantage:
        This method **displays the hex/rgb/rgba colour code** value
        for each bar as hovertext.

    :Dependencies:

        * plotly >= 2.0.6

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
