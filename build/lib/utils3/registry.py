# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides a simple interface to the Windows
            registry.  It contains a :class:`~Registry` class that can
            be used to interact with the registry; and is supported by
            the :class:`~Key` and :class:`~Value` classes.

            This module also provides the following objects that can be
            used to directly access the registry methods for each root
            HKEY.

                * hkcr = HKEY_CLASSES_ROOT
                * hkcu = HKEY_CURRENT_USER
                * hklm = HKEY_LOCAL_MACHINE
                * hkus = HKEY_USERS
                * hkcc = HKEY_CURRENT_CONFIG

:Platform:  Windows | Python 3.5
:Developer: M Critchard
:Email:     support@73rdstreetdevelopment.co.uk

:Example:  For a use example, refer to the :class:`~Registry` docstring.

"""

import utils3.user_interface as ui
from utils3 import utils

_UI = ui.UserInterface()
_OS = utils.get_os()

# TEST OS BEFORE IMPORTING winreg
if 'win' in _OS:
    import winreg as wr
else:
    _UI.print_alert('\nYour operating system (%s) is not compatible with this module.' % (_OS))

# IGNORE PYLINT WARNINGS
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
class Value(object):
    """This class encapsulates the Windows registry values.

    It provides name, type and data attributes to mimic the attributes
    of a value in the registry.

    """

    def __init__(self, name, regtype, data):
        """Set the name, type and data attributes."""
        self.name = name
        self.type = regtype
        self.data = data


# ----------------------------------------------------------------------
class Key(object):
    """This class encapsulates the Windows registry keys.

    It provides methods that can be used to interact with the values
    of the key.

    """

    def __init__(self, key):
        """Initialise a private self._key attribute.

        This attribute is used throughout the class to provide a set
        of key specific functions.

        """
        self._key = key

    def get_value(self, name):
        """Get the key value specified by name.

        Args:
            name (str): Name of the registry key.

        Returns:
            If the value exists, a value object is returned, otherwise
            ``None`` is returned.

        """
        try:
            data, regtype = wr.QueryValueEx(self._key, name)
            value = Value(name, regtype, data)
            return value
        except WindowsError:
            return None

    def set_data(self, name, data):
        """Set the data of the key value specified by name.

        Args:
            name (str): Name of the registry key.
            data (str): Data to store into the key.

        Note:
            Currently, only strings or unicode values are supported.

        """
        try:
            if isinstance(data, str):
                wr.SetValueEx(self._key, name, 0, wr.REG_SZ, data)
            else:
                raise NotImplementedError
        except NotImplementedError:
            _UI.print_error_notimp()
            # return None
        except WindowsError:
            _UI.print_error_windws()
            # return None


# ----------------------------------------------------------------------
class Registry(object):
    r"""This class encapsulates the Windows registry.

    It provides methods that can be used to interact with the keys and
    values in the registry.

    :Example:
        Example of how to get the value of a registry key::

            from utils3 import registry

            hkcu = registry.hkcu
            my_value = hkcu.get_value('control panel\desktop', 'wallpaper')
            my_wallpaper = my_value.data

    """

    def __init__(self, hkey):
        """Initialise a private self._hkey attribute.

        This attribute is used throughout the class to provide a set
        of hkey specific functions.

        """
        self._hkey = hkey

    def get_value(self, path, name):
        """Get the key value specified by the path and name

        Args:
            path (str): Path to the registry key.
            name (str): Name of the registry key.

        Returns:
            If the value exists, a value object is returned, otherwise
            ``None`` is returned.

        """
        key = self._open_key(path, wr.KEY_READ)
        value = key.get_value(name)
        return value

    def set_data(self, path, name, data):
        """Set the data of the key value specified by the path and name.

        Args:
            path (str): Path to the registry key.
            name (str): Name of the registry key.
            data (str): Data to store into the key.

        :Design:
            If the value doesn't exist, this method creates it and sets
            its type and data accordingly. A check is performed to
            determine if the operation has been completed successfully.
            If it hasn't the user is notified.

        Returns:
            The value of the registry key.

        """
        key = self._open_key(path, wr.KEY_SET_VALUE)
        key.set_data(name, data)
        key = self._open_key(path, wr.KEY_READ)
        value = key.get_value(name)
        if (value is None) or (value.data != data):
            _UI.print_error_unexpd()
        return value

    def create_key(self, path):
        """Create the key specified by the path.

        Args:
            path (str): Path to the registry key.

        :Design:
            If a creation error occurs, the user is notified.

        Returns:
            If created successfully, a ``winreg.CreateKey`` object is
            returned, otherwise ``None`` is returned.

        """
        try:
            return wr.CreateKey(self._hkey, path)
        except WindowsError:
            _UI.print_error_windws()
            return None

    def delete_key(self, path):
        """Delete the key specified by the path.

        Args:
            path (str): Path to the registry key.

        Note:
            **All of the values under the key are also deleted** but
            subkeys cannot be deleted with this method. The user is
            notified if an error occurs.

        Returns:
            If deleted successfully, a ``winreg.DeleteKey`` object is
            returned, otherwise ``None`` is returned.

        """
        try:
            return wr.DeleteKey(self._hkey, path)
        except WindowsError:
            _UI.print_error_windws()
            return None

    def _open_key(self, path, sam):
        """Open and return the key specified by the path.

        Args:
            path (str): Path to the registry key.
            sam: The SAM privilege level used to open the key.

        :Design:
            The key is opened with privilege level defined by ``sam``.
            The user is notified if an error occurs.

        Returns:
            If opened successfully, a ``winreg.OpenKey`` object is
            returned, otherwise ``None`` is returned.

        """
        try:
            key = wr.OpenKey(self._hkey, path, 0, sam)
            key = Key(key)
            return key
        except WindowsError:
            _UI.print_error_windws()
            return None

# TEST OS BEFORE SHORTCUTTING
if 'win' in _OS:
    # SHORTCUT CLASS INSTANCES FOR OUTSIDE ACCESS
    hkcr = Registry(wr.HKEY_CLASSES_ROOT)
    hkcu = Registry(wr.HKEY_CURRENT_USER)
    hklm = Registry(wr.HKEY_LOCAL_MACHINE)
    hkus = Registry(wr.HKEY_USERS)
    hkcc = Registry(wr.HKEY_CURRENT_CONFIG)
