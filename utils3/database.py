# -*- coding: utf-8 -*-
"""
:Purpose:   This class module provides a lightweight wrapper around
            various database providers, to help make connecting to and
            interfacing with the databases easier.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@73rdstreetdevelopment.co.uk

:Comments:  n/a

:Example:
            Example for how to connect to an Oracle database.  The other
            database connections follow similar logic::

                from utils3 import database

                ora = database.Oracle(host='my_host', user='my_user',
                                      passowrd='my_pass')
                ora.connect()
                ora.connected
                > True

"""


import os
from utils3 import utils
from utils3 import user_interface as ui

# ALLOW ANY NUMBER OF PUBLIC METHODS
# pylint: disable=too-few-public-methods
# ALLOW ANY NUMBER OF INSTANCE ATTRIBUTES
# pylint: disable=too-many-instance-attributes

class Database(object):
    """
    The Database super-class is used to hold general properties or
    functions used by the more specific sub-classes.  In general, you
    shouldn't need to call this super-class externally.

    """
    def __init__(self):
        """Class initialiser."""
        self.conn       = None
        self.cur        = None
        self.connected  = False
        self._ui        = ui.UserInterface()

    def disconnect(self):
        """
        Disconnect a database connection, and change the .connected
        property to False.

        """
        # TEST FOR CONNECTION
        if self.connection_active():
            # CLOSE THE DATABASE CONNECTION
            self.conn.close()
            self.connected = False

    def connection_active(self) -> bool:
        """
        General database connection test.

        Note:
            This should be used before performing operations which
            require an active connection.

        Returns:
            True if there is an active connection, otherwise False.

        """
        success = False
        if self.connected:
            success = True
        else:
            self._ui.print_warning('\nThe database must be connected first.')
        return success

    def _table_exists(self, sql) -> bool:
        """
        Test if a table exists, using the provided script.

        Args:
            sql (str): Database specific SQL command to check if a
                table exists.

        Returns:
            True if the table exists, otherwise False.

        """
        try:
            # RUN QUERY >> CONVERT RESULT TO BOOLEAN
            return bool(self.cur.execute(sql).fetchall()[0][0])

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_error(err)

    @staticmethod
    def _parse_script(script_string) -> list:
        r"""
        Parse the passed ``script_string`` and return a list of SQL
        statements to be executed individually.

        Args:
            script_string (str): The string value of the script to be
                parsed.

        :Design:
            The design is very simple in that a list of statements is
            created and returned using a split() function on the ';'
            character.

            Additionally, parsed statements containing *only* the
            newline character (\\n) are removed.  Also, the newline
            character is removed from a line starting with the newline
            character.

        Returns:
            A list of SQL commands to be run individually.

        """
        # PARSE THE SCRIPT INTO INDIVIDUAL STATEMENTS
        cmds = [line for line in script_string.split(';')]

        # LOOP THROUGH EACH STATEMENT
        for idx, cmd in enumerate(cmds):
            # TEST FOR NEWLINE CHAR LINES >> REMOVE THEM
            if cmd == '\n':
                cmds.pop(idx)
            # TEST FOR STATEMENTS STARTWITH WITH A NEWLINE CHARACTER
            elif cmd.startswith('\n'):
                # SLICE TO REMOVE THE STARTING NEWLINE CHARACTER
                cmds[idx] = cmd[1:]

        # RETURN THE CLEANED LIST OF STATEMENTS
        return cmds


# ----------------------------------------------------------------------
class MySQL(Database):
    """
    This class is a lightweight wrapper for ``mysql-connector``, and
    used to handle database objects for MySQL.

    Args:
        host (str): IP address or machine name of the host or database
            server.
        database (str): The name of the database to be connected.
        user (str): Login username
        password (str): Login password
        port (int): The TCP/IP port of the MySQL server; must be an
            integer.
        from_file (bool): Load the database credentials directly from a
            config file.
            (Valid keys: host, database, port, user, password)
        filename (str): Full path to the file holding the database
            credentials.  Required if ``from_file`` is True.

    :Dependencies:
        * mysql-connector (2.1.4)

            * Installation: ``pip install mysql-connector==2.1.4``

    :Example:
        To connect to a **MySQL** database::

            from utils3.database import MySQL

            # LOAD CREDENTIALS
            sql = MySQL(host='my_host', database='my_db',
                        user='my_user', password='my_pass')

            # CONNECT TO THE DB
            sql.connect()
            # CHECK CONNECTION WAS SUCCESSFUL
            sql.connected
            > True

    """
    def __init__(self, host=None, database=None, user=None,
                 password=None, port=3306, from_file=False,
                 filename=None):
        """Class initialiser."""
        # INHERIT SUPER-CLASS PROPERTIES
        super(MySQL, self).__init__()
        # INITIALISE
        self._host      = host
        self._database  = database
        self._user      = user
        self._password  = password
        self._port      = port
        self._from_file = from_file
        self._filename  = filename

    def connect(self):
        """
        Create a database connection and update class attributes
        accordingly.

        :Design:
            Function designed to create a connection to a MySQL database
            using the provided login parameters, or directly from a
            config file. If a login detail is not provided, the user is
            prompted; which can be used as a security feature.

            Several other functions, which can be found in the utils3
            module, are working in the background for the credential
            validation and handling the actual database connection.

        Note:
            To prompt the user for login details, leave the parameter(s)
            blank.

        :Source:
            The connection argument keys for a MySQL connection using
            the mysql.connection library, are listed here:
            `dev.mysql <https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html>`_

        """
        try:
            # INITIALISE
            creds = dict()
            dbtype = 'mysql'

            # TEST IF A CONFIG FILE IS TO BE USED
            if self._from_file:
                # DEFINE CREDENTIAL KEYS
                db_keys = ['host', 'database', 'port', 'user', 'password']
                # GET CREDENTIALS FROM THE CONFIG FILE
                creds = utils._dbconn_fields(dbtype=dbtype, fields=db_keys,
                                             filename=self._filename)
            else:
                # GET CREDENTIALS FROM PASSED PARAMETERS
                creds = utils._dbconn_params(dbtype=dbtype, host=self._host,
                                             database=self._database, user=self._user,
                                             password=self._password)

            # TEST IF CREDENTIALS ARE POPULATED
            if creds is not None:
                # CONNECT TO THE DATABASE >> UPDATE CLASS PROPERTIES
                self._connect(creds=creds)

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_alert('\nAn error occurred while connecting to the MySQL database.')
            self._ui.print_error(err)

    def table_exists(self, table_name) -> bool:
        """
        Test if a table exists.

        Args:
            table_name (str): The name of the table to be tested.

        :Design:
            This function wraps the local ``MySQL._table_exists()``
            function and provides the SQL statement to be run.

        Returns:
            True if the table exists, otherwise False.

        """
        # BUILD SQL STATEMENT
        sql = """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE table_name = '%s'
        LIMIT 1
        """ % table_name
        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)

    def _connect(self, creds):
        """
        Connect to the database using the passed credentials, update
        class properties accordingly.

        Args:
            creds (dict): A dictionary of login credentials.

        :Design:
            The cursor is set with the buffered parameter set to True;
            allowing the cursor to fetch all rows, rather than being
            'lazily' loaded.

            `Design source <https://stackoverflow.com/a/33632767/6340496>`_

        """
        try:
            # MAKE THE CONNECTION
            dbo = utils._dbconn_mysql_conn(creds=creds)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = self.conn.cursor(buffered=True)
            self.connected  = True
        except Exception:
            self.connected = False

    def _table_exists(self, sql):
        """
        Test if a table exists and return a boolean result.

        :Design:
            This function is used rather than the general
            ``Database._table_exists()`` function as the MySQL
            ``cur.execute()`` object does not have a fetchall attribute,
            so the actions must be done in separate steps.

        """
        try:
            # RUN QUERY
            self.cur.execute(sql)
            # GET >> CONVERT RESULT TO BOOLEAN AND RETURN
            return bool(self.cur.fetchall()[0][0])
        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_error(err)


# ----------------------------------------------------------------------
class Oracle(Database):
    """
    This class is a lightweight wrapper for ``cx_Oracle``, where
    commonly used functionality have been added as class methods and
    functions.

    Args:
        host (str): Database name, or TNS host.
        user (str): Login username
        password (str): Login password
        from_file (bool): Load the database credentials directly from
            a config file.
            (Valid keys: host, user, password)
        filename (str): Full path to the file holding the database
            credentials.

    :Example:
        To connect to an **Oracle** database::

            from utils3.database import Oracle

            # LOAD CREDENTIALS
             ora = Oracle(host='my_host', user='my_user',
                          password='my_pass')

            # CONNECT TO THE DB
            ora.connect()
            # CHECK CONNECTION WAS SUCCESSFUL
            ora.connected
            > True

    """
    def __init__(self, host=None, user=None, password=None,
                 from_file=False, filename=None):
        """Class initialiser."""
        # INHERIT SUPER-CLASS PROPERTIES
        super(Oracle, self).__init__()
        # INITIALISE
        self.connstr    = ''
        self._host      = host
        self._user      = user
        self._password  = password
        self._from_file = from_file
        self._filename  = filename

    def connect(self):
        """
        Create a database connection and update class attributes
        accordingly.

        :Design:
            Function designed to create a connection to an Oracle
            database using the provided login parameters, or directly
            from a config file. If a login detail is not provided, the
            user is prompted; which can be used as a security feature.

            Several other functions, which can be found in the utils3
            module, are working in the background for the credential
            validation and handling the actual database connection.

        Note:
            To prompt the user for login details, leave the parameter(s)
            blank.

        """
        try:
            # INITIALISE
            creds = dict()
            dbtype = 'oracle'

            # TEST IF A CONFIG FILE IS TO BE USED
            if self._from_file:
                # DEFINE CREDENTIAL KEYS
                db_keys = ['host', 'user', 'password']
                # GET CREDENTIALS FROM THE CONFIG FILE
                creds = utils._dbconn_fields(dbtype=dbtype, fields=db_keys,
                                             filename=self._filename)
            else:
                # GET CREDENTIALS FROM PASSED PARAMETERS
                creds = utils._dbconn_params(dbtype=dbtype, host=self._host, user=self._user,
                                             password=self._password)

            # TEST IF CREDENTIALS ARE POPULATED
            if creds is not None:
                # CONNECT TO THE DATABASE >> UPDATE CLASS PROPERTIES
                self._connect(creds=creds)

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_alert('\nAn error occurred while connecting to the Oracle database.')
            self._ui.print_error(err)

    def execute_script(self, sql_file, commit=False) -> bool:
        """
        Execute a full SQL script on the database.

        Args:
            sql_file (str): The full file path to the script to be run.
            commit (bool): Commit after the script has finished?

        :Design:
            This method is a wrapper around cx_Oracle's ``execute()``
            method and is designed specifically to handle a full Oracle
            SQL script consisting of multiple SQL statements, as
            cx_Oracle cannot natively handle this.

            Once the script is parsed into individual statements using
            the ';' character, each individual statement is run using
            cx_Oracle's ``execute()`` method.

        Returns:
            True if the script and [optional commit] are successful,
            otherwise False.

        """
        try:
            # INITIALISE
            success = False

            # TEST IF THE FILE EXISTS
            if utils.fileexists(sql_file):
                # RE-INITIALISE (SO FIRST EXECUTE WILL RUN)
                success = True
                # PARSE THE SCRIPT INTO INDIVIDUAL COMMANDS
                cmds = self._parse_script(script_string=open(sql_file).read())

                # LOOP THROUGH EACH STATEMENT
                for cmd in cmds:
                    # EXECUTE COMMAND
                    if success: success = self._execute_commit(sql=cmd, commit=commit)

        except Exception as err:
            success = False
            self._ui.print_error(err)

        return success

    def table_exists(self, table_name) -> bool:
        """
        Test if a table exists.

        Args:
            table_name (str): The name of the table to be tested.

        :Design:
            This is an Oracle specific function which wraps the general
            ``Database._table_exists()`` function and provides the SQL
            statement to be run.

        Returns:
            True is the table exists, otherwise False.

        """
        # BUILD THE SQL STATEMENT
        sql = """
        SELECT COUNT(*) FROM dual WHERE EXISTS (
            SELECT *
            FROM sys.user_tables
            WHERE upper(table_name) = '%s'
        )
        """ % table_name.upper()
        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)

    def _execute_commit(self, sql, commit) -> bool:
        """
        Execute an SQL statement and commit if instructed.

        Args:
            sql (str): SQL script to be executed.
            commit (bool): Commit after script execute has finished?

        :Design:
            This is a simple execute / commit wrapper around cx_Oracle's
            ``execute()`` method.

        Returns:
            True if the script and [optional commit] are successful,
            otherwise False.

        """
        try:
            # EXECUTE COMMAND
            self.cur.execute(sql)
            # COMMIT?
            if commit: self.conn.commit()
            success = True
        except Exception as err:
            success = False
            self._ui.print_error(err)
        return success

    def _connect(self, creds):
        """
        Create a database connection and update class properties
        accordingly.

        Args:
            creds (dict): A dictionary of login credentials.

        :Design:
            In addition to setting the 'typical' class properties, a
            connection string property has been added to this Oracle
            specific connection.

        """
        try:
            # MAKE THE CONNECTION
            dbo = utils._dbconn_oracle_conn(creds=creds)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = dbo['cur']
            self.connstr    = '%s/%s@%s' % (creds['user'], creds['password'], creds['host'])
            self.connected  = True
        except Exception:
            self.connected = False


# ----------------------------------------------------------------------
class SQLite(Database):
    """
    This class is a lightweight wrapper for ``sqlite3``, and used to
    handle database objects for SQLite.

    Args:
        db_file_path (str): Full file path to the SQLite database file.

    :Example:
        To connect to an **SQLite** database::

            from utils3.database import SQLite

            # LOAD CREDENTIALS
            sql = SQLite(db_file_path='path/to/data.db')

            # CONNECT TO THE DB
            sql.connect()
            # CHECK CONNECTION WAS SUCCESSFUL
            sql.connected
            > True

    """
    def __init__(self, db_file_path):
        """Class initialiser."""
        # INHERIT SUPER-CLASS PROPERTIES
        super(SQLite, self).__init__()
        # INITIALISE
        self._db_file_path = db_file_path

    def connect(self):
        """Connect to the SQLite database file."""
        # CONNECT
        self._connect()

    def table_exists(self, table_name) -> bool:
        """
        Test if a table exists.

        Args:
            table_name (str): The name of the table to be tested.

        :Design:
            This is a SQLite specific function which wraps the general
            ``Database._table_exists()`` function and provides the SQL
            statement to be run.

        Returns:
            True if the table exists, otherwise False.

        """
        # BUILD THE SQL STATEMENT
        sql = """
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE type = "table"
        	AND upper(name) = '%s'
        LIMIT 1
        """ % table_name.upper()
        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)

    def vacuum(self):
        """
        Shrink the size of the database file.

        :Design:
            Per Ref01:
            "The VACUUM command rebuilds the database file, repacking it
            into a minimal amount of disk space. There are several
            reasons an application might do this:

            1) Unless SQLite is running in "auto_vacuum=FULL" mode, when
               a large amount of data is deleted from the database file
               it leaves behind empty space, or "free" database pages.
               This means the database file might be larger than
               strictly necessary. Running VACUUM to rebuild the
               database reclaims this space and reduces the size of the
               database file.

            2) Frequent inserts, updates, and deletes can cause the
               database file to become fragmented - where data for a
               single table or index is scattered around the database
               file. Running VACUUM ensures that each table and index is
               largely stored contiguously within the database file. In
               some cases, VACUUM may also reduce the number of
               partially filled pages in the database, reducing the size
               of the database file further.""

        :References:
            * Ref01: https://www.sqlite.org/lang_vacuum.html

        """
        # TEST FOR CONNECTION
        if self.connection_active():
            # RUN VACUUM
            self.cur.execute('vacuum')

    def _connect(self):
        """
        Connect to the database file, and update class attributes
        accordingly.

        :Design:
            Before connecting to the database file, this function tests
            if the file exists.  If the file does not exist, it is
            created automatically.

        """
        try:
            # TEST IF FILE EXISTS >> CREATE IT
            if not self._db_file_exists:
                open(self._db_file_exists, 'a').close()
            # MAKE THE CONNECTION
            dbo = utils.dbconn_sqlite(db_path=self._db_file_path)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = dbo['cur']
            self.connected  = True
        except Exception:
            self.connected = False

    def _db_file_exists(self) -> bool:
        """Test if the database file exists.

        Returns:
            True if the database file exists, otherwise False.
        """
        return os.path.exists(self._db_file_path)


# ----------------------------------------------------------------------
class SQLServer(Database):
    """
    This class is a lightweight wrapper for ``pyodbc``, and used to
    handle database objects for SQL Server.

    Args:
        server (str): Name of the server where the SQL Server database
            lives.
        database (str): The name of the database to be connected.
        user (str): Login username
        password (str): Login password
        from_file (bool): Load the database credentials directly from a
            config file.
            (Valid keys: server, database, user, password)
        filename (str): Full path to the file holding the database
            credentials.

    :Example:
        To connect to an **SQLServer** database::

            from utils3.database import SQLServer

            # LOAD CREDENTIALS
             sql = SQLServer(server='my_server', database='my_db',
                             user='my_user', password='my_pass')

            # CONNECT TO THE DB
            sql.connect()
            # CHECK CONNECTION WAS SUCCESSFUL
            sql.connected
            > True

    """
    def __init__(self, server=None, database=None, user=None,
                 password=None, from_file=False, filename=None):
        """Class initialiser."""
        # INHERIT SUPER-CLASS PROPERTIES
        super(SQLServer, self).__init__()
        # INITIALISE
        self._server    = server
        self._database  = database
        self._user      = user
        self._password  = password
        self._from_file = from_file
        self._filename  = filename

    def connect(self):
        """
        Connect to the database, and update class attributes
        accordingly.

        :Design:
            Function designed to create a connection to a SQL Server
            database using the provided login parameters, or directly
            from a config file. If a login detail is not provided, the
            user is prompted; which can be used as a security feature.

            Several other functions, which can be found in the utils3
            module, are working in the background for the credential
            validation and handling the actual database connection.

        Note:
            To prompt the user for login details, leave the parameter(s)
            blank.

        """
        try:
            # INITIALISE
            creds = dict()
            dbtype = 'sql_server'

            # TEST IF A CONFIG FILE IS TO BE USED
            if self._from_file:
                # DEFINE CREDENTIAL KEYS
                db_keys = ['server', 'database', 'user', 'password']
                # GET CREDENTIALS FROM THE CONFIG FILE
                creds = utils._dbconn_fields(dbtype=dbtype, fields=db_keys,
                                             filename=self._filename)
            else:
                # GET CREDENTIALS FROM PASSED PARAMETERS
                creds = utils._dbconn_params(dbtype=dbtype, server=self._server,
                                             database=self._database, user=self._user,
                                             password=self._password)

            # TEST IF CREDENTIALS ARE POPULATED
            if creds is not None:
                # CONNECT TO THE DATABASE >> UPDATE CLASS PROPERTIES
                self._connect(creds=creds)

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_alert('\nAn error occurred while connecting to the SQLServer database.')
            self._ui.print_error(err)

    def table_exists(self, table_name) -> bool:
        """
        Test if a table exists.

        Args:
            table_name (str): The name of the table to be tested.

        :Design:
            This is a SQL Server specific function which wraps the
            general ``Database._table_exists()`` function and provides
            the SQL statement to be run.

        Returns:
            True if the table exists, otherwise False.

        """
        # BUILD SQL STATEMENT
        sql = """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE upper(table_name) = '%s'
        """ % table_name.upper()
        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)

    def _connect(self, creds):
        """
        Connect to the database using the passed credentials, update
        class properties accordingly.

        Args:
            creds (dict): A dictionary of login credentials.

        """
        try:
            # MAKE THE CONNECTION
            dbo = utils._dbconn_sql_conn(creds=creds)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = dbo['cur']
            self.connected  = True
        except Exception:
            self.connected = False
