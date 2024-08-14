#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides an easy-access, light-weight wrapper,
            around ``matplotlib``'s colour maps, and can be used for
            retrieving and previewing named colour maps.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Examples:

    Retrieve 5 colours from the 'viridis' colour map in hex format
    and preview the colours::

        >>> from utils4.cmaps import cmaps

        >>> clrs = cmaps.get_cmap('viridis', 15, as_hex=True, preview=True)
        >>> clrs

        ['#2d718e', '#297b8e', '#25858e', '#218f8d', '#1f998a',
         '#20a386', '#26ad81', '#34b679', '#46c06f', '#5cc863',
         '#73d056', '#8ed645', '#aadc32', '#c5e021', '#fde725']

    .. figure:: _static/img/cmaps_viridis15.png
        :scale: 75%
        :align: center

        Preview of the requested 'viridis' colour map of 15 colours


    List named colours from the matplotlib colour palette::

        >>> from utils4.cmaps import cmaps

        >>> cmaps.get_named_colours()

        {'aliceblue': '#F0F8FF',
         'antiquewhite': '#FAEBD7',
         'aqua': '#00FFFF',
         ...,
         'whitesmoke': '#F5F5F5',
         'yellow': '#FFFF00',
         'yellowgreen': '#9ACD32'}


    List or retrieve colour map names::

        >>> from utils4.cmaps import cmaps

        >>> cmaps.view_cmaps(view_only=True)

        ['magma',
         'inferno',
         'plasma',
         ...,
         'tab20_r',
         'tab20b_r',
         'tab20c_r']

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from typing import Union


class _Preview:  # pragma: nocover
    """Provide a preview for a given colourmap."""

    def __init__(self, colours):
        """_Preview class initialiser.

        Args:
            colours (Union[list, np.array]): Iterable of colours for
                preview.

        """
        self._c = colours
        self._n = len(colours)
        self._x = None
        self._y = None
        self._build_dataset()

    def plot(self):
        """Plot to show colours."""
        w = 6 if self._n < 50 else 10
        h = w/1.618033
        _, ax = plt.subplots(figsize=[w, h])
        ax.scatter(self._x,
                   self._y,
                   marker='o',
                   s=100,
                   c=self._c)
        plt.show()

    def _build_dataset(self):
        """Create a dataset to be plotted."""
        self._x = np.arange(self._n)
        self._y = np.sin(self._x*(np.pi/180))


class CMaps():
    """Provides an easy-access layer to ``matplotlib``'s colour maps."""

    @staticmethod
    def get_cmap(map_name: str,
                 n: int=25,
                 as_hex: bool=False,
                 preview: bool=False) -> Union[list, np.array]:
        """Get a list of (n) RGBA or Hex colours from a specified map.

        This colour wrapper is specialised to return (n) colours from
        a normalised colour map. Meaning, rather than returning the
        5 lightest colours, or the 200 lightest to medium colours, the
        lightest colours are removed (as often they are difficult to
        see in a graph) and the darkest colour is added. The intent
        is to provide (n) 'usable' colours for graphing.

        Args:
            map_name (str): Name of the matplotlib colourmap.
            n (int, optional): Number of colours to return. Must
                be >= 255. Defaults to 25.
            as_hex (bool, optional): Return the colours as a hex string.
                Defaults to False, which returns colours as RGBA.
            preview (bool, optional): Preview the colour map. Defaults
                to False.

        Raises:
            ValueError: If the value of ``n`` is not between 1 and 255.

        Returns:
            Union[list, np.array]: Iterable of (n) colours.

        """
        if (n < 1) | (n > 255):
            raise ValueError('The value of n must be: 1 <= n <= 255.')
        norm = matplotlib.colors.Normalize(vmin=-150, vmax=256)
        cmap = matplotlib.colormaps.get_cmap(map_name)
        clrs = cmap(norm(range(256)))
        N = int(256//n)
        c = clrs[::N]
        # Trim colours until desired length is met.
        while len(c) > n:
            if len(c) - n == 1:
                c = c[:-1]
            else:
                # Shave colours off boths ends until desired length is met.
                c = c[:-1] if len(c) % 2 == 0 else c[1:]
        c[-1] = clrs[-1]
        if as_hex:
            c_ = [matplotlib.colors.rgb2hex(i) for i in c]
            c = c_[:]
        if preview:  # pragma: nocover
            _Preview(colours=c).plot()
        return c

    @staticmethod
    def get_named_colours() -> dict:
        """Return a dictionary of CSS name and hex value.

        Returns:
            dict: A dict of named colours as ``{name: hex_code}`` pairs.

        """
        return matplotlib.colors.cnames

    @staticmethod
    def view_cmaps(view_only: bool=True) -> Union[list, None]:
        """Show the available colour map names.

        Args:
            view_only (bool, optional): If ``True`` the list will be
                printed and ``None`` is returned.  If ``False``, the list
                is returned and nothing is printed. Defaults to True.

        Returns:
            Union[list, None]: A list of colour maps names if
            ``view-only`` is False, otherwise None.

        """
        c = plt.colormaps()
        if view_only:
            print(c)
            c = None
        return c


cmaps = CMaps()
