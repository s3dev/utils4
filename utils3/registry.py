"""------------------------------------------------------------------------------------------------
Program:    registry.py
Purpose:    This module provides a simple interface to the Windows registry. It contains a
            Registry class that can be used to interact with the registry. The Registry class is
            supported by a Key class and a Value class

            This module also provides the following objects that can be used to directly access
            the Registry methods for each root HKEY.
                - hkcr = HKEY_CLASSES_ROOT
                - hkcu = HKEY_CURRENT_USER
                - hklm = HKEY_LOCAL_MACHINE
                - hkus = HKEY_USERS
                - hkcc = HKEY_CURRENT_CONFIG

Developer:  M. Critchard

Email:      mark.critchard@rolls-royce.com

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
05.03.18    M. Critchard    1.0.0       Permanently branched for Python 3 from the Python 2.7
                                        utils module.
07.03.18    J. Berendt      1.0.1       Minor formatting changes and cleaning.  pylint (10/10)
------------------------------------------------------------------------------------------------"""

import winreg as wr
import utils3.user_interface as ui

# IGNORE
# pylint: disable=too-few-public-methods
# IGNORE SHORTCUT TO CLASS INSTANTIATIONS
# pylint: disable=invalid-name


class Value(object):
    """
    PURPOSE:
    This class encapsulates the Windows registry value. It provides
    name, type and data attributes to mimic the attributes of a
    value in the registry.
    """

    def __init__(self, name, regtype, data):
        """
        PURPOSE:
        This constructor sets the name, type and data attributes.
        """
        self.name = name
        self.type = regtype
        self.data = data


class Key(object):
    """
    PURPOSE:
    This class encapsulates the Windows registry key. It provides
    methods that can be used to interact with the values of the
    key.
    """

    # INSTANTIATE THE UserInterface CLASS
    _ui = ui.UserInterface()

    def __init__(self, key):
        """
        PURPOSE:
        This constructor initialises a private self._key attribute
        which is used throughout the class to provide a set of key
        specific functions.
        """
        self._key = key

    def get_value(self, name):
        """
        PURPOSE:
        This method gets the key value specified by name. If the
        value exists, a value object is returned to the caller. Else,
        None is returned.
        """
        try:
            data, regtype = wr.QueryValueEx(self._key, name)
            value = Value(name, regtype, data)
            return value
        except WindowsError:
            return None

    def set_data(self, name, data):
        """
        PURPOSE:
        This method sets the data of the key value specified by name.

        NOTE:
        Only strings or unicode values are currently supported.
        """
        try:
            if isinstance(data, str):
                wr.SetValueEx(self._key, name, 0, wr.REG_SZ, data)
            else:
                raise NotImplementedError
        except NotImplementedError:
            self._ui.print_error_notimp()
            return None
        except WindowsError:
            self._ui.print_error_windws()
            return None


class Registry(object):
    """
    PURPOSE:
    This class encapsulates the Windows registry. It provides
    methods that can be used to interact with the keys and values in
    the registry.
    """

    # INSTANTIATE THE UserInterface CLASS
    _ui = ui.UserInterface()

    def __init__(self, hkey):
        """
        PURPOSE:
        This constructor initialises a private self._hkey attribute
        which is used throughout the class to provide a set of hkey
        specific functions.
        """
        self._hkey = hkey

    def get_value(self, path, name):
        """
        PURPOSE:
        This method gets the key value specified by path and name. If
        the value exists, a value object is returned to the caller.
        Else, None is returned.
        """
        key = self._open_key(path, wr.KEY_READ)
        value = key.get_value(name)
        return value

    def set_data(self, path, name, data):
        """
        PURPOSE:
        This method sets the data of the key value specified by path
        and name. If the value doesn't exist, this method creates it
        and sets its type and data accordingly. A check is performed
        to see if the operation has been completed successfully. If it
        hasn't the user is notified.
        """
        key = self._open_key(path, wr.KEY_SET_VALUE)
        key.set_data(name, data)
        key = self._open_key(path, wr.KEY_READ)
        value = key.get_value(name)
        if (value is None) or (value.data != data):
            self._ui.print_error_unexpd()
        return value

    def create_key(self, path):
        """
        PURPOSE:
        This method creates the key specified by path. The user is
        notified if an error occurs.
        """
        try:
            return wr.CreateKey(self._hkey, path)
        except WindowsError:
            self._ui.print_error_windws()
            return None

    def delete_key(self, path):
        """
        PURPOSE:
        This method deletes the key specified by path. All of the
        values under the key are also deleted but subkeys cannot be
        deleted with this method. The user is notified if an error
        occurs.
        """
        try:
            return wr.DeleteKey(self._hkey, path)
        except WindowsError:
            self._ui.print_error_windws()
            return None

    def _open_key(self, path, sam):
        """
        PURPOSE:
        This method opens and returns the key specified by path. The
        key is opened with privilege level defined by sam. The user is
        notified if an error occurs.
        """
        try:
            key = wr.OpenKey(self._hkey, path, 0, sam)
            key = Key(key)
            return key
        except WindowsError:
            self._ui.print_error_windws()
            return None


hkcr = Registry(wr.HKEY_CLASSES_ROOT)
hkcu = Registry(wr.HKEY_CURRENT_USER)
hklm = Registry(wr.HKEY_LOCAL_MACHINE)
hkus = Registry(wr.HKEY_USERS)
hkcc = Registry(wr.HKEY_CURRENT_CONFIG)
