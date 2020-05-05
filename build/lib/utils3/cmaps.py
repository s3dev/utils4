#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides an easy-access, light-weight wrapper,
            around ``matplotlib``'s colour maps.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  n/a

:Example:
    Example code use::

        from utils3.cmaps import cmaps
        clrs = cmaps.get_cmap('viridis', 5, as_hex=True, preview=True)

        clrs
        >>> ['#005ed0', '#007ec0', '#009eb0', '#00bfa0', '#00ff80']

"""
# pylint: disable=invalid-name

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class _Preview():
    """Provide a preview for a given colourmap."""

    def __init__(self, colours):
        """_Preview class initialiser.

        Args:
            colours (list, np.array): Iterable of colours for preview.

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
    def get_cmap(map_name, n, as_hex=False, preview=False):
        """Get a list of (n) RGBA or Hex colours from a specified map.

        This colour wrapper is specialised to return (n) colours from
        a normalised colour map. Meaning, rather than returning the
        5 lightest colours, or the 200 lightest to medium colours, the
        lightest colours are removed (as often they are difficult to
        see in a graph) and the darkest colour is added. The intent
        is to provide (n) 'usable' colours for graphing.

        Args:
            map_name (str): Name of the matplotlib colourmap.
            n (int): Number of colours to return.  Must be >= 256.
            as_hex (bool): Return the colours as a hex string. By
                default, colours are returned as RGBA.

        Returns:
            A list (or np.array) of (n) colours.

        """
        norm = matplotlib.colors.Normalize(vmin=-150, vmax=256)
        cmap = matplotlib.cm.get_cmap(map_name)
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
        if preview:
            _Preview(colours=c).plot()
        return c

    @staticmethod
    def get_named_colours() -> dict:
        """Return a dictionary of CSS name and hex value."""
        named = matplotlib.colors.cnames
        return named

    @staticmethod
    def view_cmaps(view_only=True):
        """Show the available colour maps.

        Args:
            view_only (bool): If ``True`` the list will be printed
                and ``None`` is returned.  If ``False``, the list
                is returned and nothing is printed.

        """
        c = plt.colormaps()
        if view_only:
            print(c)
            c = None
        return c


cmaps = CMaps()
