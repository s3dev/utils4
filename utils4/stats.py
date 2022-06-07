#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains the statistical calculations for the project.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

    Calculate a linear regression line on an X/Y dataset.:

        >>> from lib.stats import LinearRegression

        >>> linreg = LinearRegression(x, y)
        >>> linreg.calculate()

        >>> # View the intercept value.
        >>> linreg.intercept
        5.6

        >>> # View the slope value.
        >>> linreg.slope
        0.25678

        >>> # Obtain the regression line array.
        >>> y_ = linreg.regression_line

"""
# pylint: disable=line-too-long

import numpy as np


class LinearRegression:
    """Calculate the linear regression of a dataset.

    Args:
        x (np.array): Array of X-values.
        y (np.array): Array of Y-values.

    :Slope Calculation:
        The calculation for the slope itself is borrowed from the
        :func:`scipy.stats.linregress` function. Whose `source code`_ was
        obtained on GitHub.

    .. _source code: https://github.com/scipy/scipy/blob/v1.8.0/scipy/stats/_stats_mstats_common.py#L16-L203

    """

    def __init__(self, x: np.array, y: np.array):
        """LinearRegression class initialiser."""
        self._x = x
        self._y = y
        self._xbar = 0.0
        self._ybar = 0.0
        self._c = 0.0
        self._m = 0.0
        self._line = np.array(())

    @property
    def slope(self):
        """Accessor to the slope value."""
        return self._m

    @property
    def intercept(self):
        """Accessor to the slope's y-intercept."""
        return self._c

    @property
    def regression_line(self):
        """Accessor to the calculated regression line, as y-values."""
        return self._line

    def calculate(self):
        """Calculate the linear regression for the X/Y data arrays.

        The result of the calculation is accessible via the
        :attr:`regression_line` property.

        """
        self._calc_means()
        self._calc_slope()
        self._calc_intercept()
        self._calc_regression_line()

    def _calc_intercept(self):
        """Calculate the intercept as: ybar - m * xbar."""
        self._c = self._ybar - self._m * self._xbar

    def _calc_means(self) -> float:
        """Calculate the mean of the X and Y arrays."""
        self._xbar = self._x.mean()
        self._ybar = self._y.mean()

    def _calc_regression_line(self):
        """Calculate the regression line as: y = mx + c."""
        self._line = self._m * self._x + self._c

    def _calc_slope(self):
        """Calculate the slope value as: R * ( std(y) / std(x) ).

        Per the ``scipy`` source code comments::

            # Average sums of square differences from the mean
            #   ssxm = mean( (x-mean(x))^2 )
            #   ssxym = mean( (x-mean(x)) * (y-mean(y)) )

            ...

            slope = ssxym / ssxm

        """
        ssxm = np.mean( (self._x - self._xbar)**2 )
        ssxym = np.mean( (self._x - self._xbar) * (self._y - self._ybar) )
        self._m = ssxym / ssxm

    @staticmethod
    def _calc_std(data: np.array, ddof: int=1) -> float:  # pragma nocover
        """Calculate the standard deviation.

        Args:
            data (np.array): Array of values.
            ddof (int): Degrees of freedom. Defaults to 1.

        Returns:
            float: Standard deviation of the given values.

        """
        return np.std(data, ddof=ddof)
