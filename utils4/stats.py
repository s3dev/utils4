#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Provide access to various statistical calculations, namely:

            - **CUSUM:** :meth:`~Stats.cusum`
            - **Gaussian KDE:** :meth:`~Stats.kde`
            - **Linear Regression:** :class:`~LinearRegression`

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

    Create a sample dataset for the stats methods::

        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import pandas as pd

        >>> np.random.seed(73)
        >>> data = np.random.normal(size=100)*100
        >>> x = np.arange(data.size)
        >>> y = pd.Series(data).rolling(window=25, min_periods=25).mean().cumsum()

        >>> # Preview the trend.
        >>> plt.plot(x, y)

"""
# pylint: disable=line-too-long
# pylint: disable=wrong-import-order

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from typing import Union
# local
from utils4.reporterror import reporterror


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

    :Example Use:

        .. tip::

            For a sample dataset and imports to go along with this
            example, refer to the docstring for
            :mod:`this module <stats>`.

        Calculate a linear regression line on an X/Y dataset::

            >>> from lib.stats import LinearRegression

            >>> linreg = LinearRegression(x, y)
            >>> linreg.calculate()

            >>> # Obtain the regression line array.
            >>> y_ = linreg.regression_line

            >>> # View the intercept value.
            >>> linreg.intercept
            -31.26630

            >>> # View the slope value.
            >>> linreg.slope
            1.95332

            >>> # Plot the trend and regression line.
            >>> plt.plot(x, y, 'grey')
            >>> plt.plot(x, y_, 'red')
            >>> plt.show()

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


class Stats:
    """Wrapper class for various statistical calculations."""

    @staticmethod
    def cusum(df: pd.DataFrame,
              cols: Union[list, str],
              window: int=None,
              min_periods: int=1,
              inplace=False,
              show_plot: bool=False) -> Union[pd.DataFrame, None]:
        r"""Calculate a CUSUM on a set of data.

        A CUSUM is a generalised method for smoothing a noisy trend, or
        for detecting a change in the trend.

        Note:
            A CUSUM is *not* a cumulative sum (cumsum), although a
            cumulative sum is used. A CUSUM is a cumulative sum of
            derived values, where each derived value is calculated as the
            delta of a single value relative to the rolling mean of all
            previous values.

        Args:
            df (pd.DataFrame): The DataFrame containing the column(s) on
                which a CUSUM is to be calculated.
            cols (Union[list, str]): The column (or list of columns) on
                which the CUSUM is to be calculated.
            window (int, optional): Size of the window on which the
                rolling mean is to be calculated. This corresponds to the
                ``pandas.df.rolling(window)`` parameter.
                Defaults to None.

                - If None is received, a %5 window is calculated based on
                  the length of the DataFrame. This method helps smooth
                  the trend, while keeping a representation of the
                  original trend.
                - For a *true* CUSUM, a running average should be
                  calculated on the length of the DataFrame, except for
                  the current value. For this method, pass
                  ``window=len(df)``.

            min_periods (int, optional): Number of periods to wait before
                calculating the rolling average. Defaults to 1.
            inplace (bool, optional): Update the passed DataFrame
                (in-place), rather returning a *copy* of the passed
                DataFrame. Defaults to False.
            show_plot (bool, optional): Display a graph of the raw value,
                and the calculated CUSUM results. Defaults to False.

        :Calculation:
            The CUSUM is calculated by taking a rolling mean :math:`RA`
            (optionally locked at the first value), and calculate the
            delta of the current value, relative to the rolling mean all
            previous values. A cumulative sum is applied to the deltas.
            The cumulative sum for each data point is returned as the
            CUSUM value.

        :Equation:

            :math:`c_i = \sum_{i=1}^{n}(x_i - RA_i)`

            where :math:`RA` (Rolling Mean) is defined as:

                :math:`RA_{i+1} = \frac{1}{n}\sum_{j=1}^{n}x_j`

        :Example Use:

            Generate a *sample* trend dataset::

                >>> import numpy as np
                >>> import pandas as pd

                >>> np.random.seed(13)
                >>> s1 = pd.Series(np.random.randn(1000)).rolling(window=100).mean()
                >>> np.random.seed(73)
                >>> s2 = pd.Series(np.random.randn(1000)).rolling(window=100).mean()
                >>> df = pd.DataFrame({'sample1': s1, 'sample2': s2})


            Example for calculating a CUSUM on two columns::

                >>> from EHM.stats import stats

                >>> df_c = stats.cusum(df=df,
                                       cols=['sample1', 'sample2'],
                                       window=len(df),
                                       inplace=False,
                                       show_plot=True)
                >>> df_c.tail()
                      sample1   sample2  sample1_cusum  sample2_cusum
                995  0.057574  0.065887      23.465337      29.279936
                996  0.062781  0.072213      23.556592      29.369397
                997  0.028513  0.072658      23.613478      29.459204
                998  0.024518  0.070769      23.666305      29.547022
                999  0.000346  0.074849      23.694901      29.638822

        Returns:
            Union[pd.DataFrame, None]: If the ``inplace`` argument is
            ``False``, a *copy* of the original DataFrame with the new
            CUSUM columns appended is returned. Otherwise, the passed
            DataFrame is *updated*, and ``None`` is returned.

        """
        # Convert a single column name to a list.
        cols = [cols] if not isinstance(cols, list) else cols
        if not inplace:
            df = df.copy(deep=True)
        window = int(len(df) * 0.05) if window is None else window  # Set default window as 5%
        for col in cols:
            new_col = f'{col}_cusum'
            # CUSUM calculation (rolling_sum on rolling_mean, with a shift of 1).
            df[new_col] = ((df[col] - df[col].rolling(window=window, min_periods=min_periods)
                            .mean()
                            .shift(1))
                           .rolling(window=len(df), min_periods=min_periods).sum())
            # Show simple plot if requested.
            if show_plot:  # pragma: nocover
                df[[col, new_col]].plot(title=f'TEMP PLOT\n{col} vs {new_col}',
                                        color=['lightgrey', 'red'],
                                        secondary_y=new_col,
                                        legend=False,
                                        grid=False)
        return None if inplace else df

    def kde(self,
            data: Union[list, np.array, pd.Series],
            n: int=500) -> tuple:
        """Calculate the kernel density estimate (KDE) for an array X.

        This function returns the *probability density* (PDF) using
        Gaussian KDE.

        Args:
            data (Union[list, np.array, pd.Series]): An array-like object
                containing the data against which the Gaussian KDE is
                calculated. This can be a list, numpy array, or pandas
                Series.
            n (int, optional): Number of values returned in the X, Y
                arrays. Defaults to 500.

        :Example Use:

            .. tip::

                For a sample dataset and imports to go along with this
                example, refer to the docstring for
                :mod:`this module <stats>`.

            Calculate a Gaussian KDE on Y::

                >>> from utils4.stats import stats

                >>> # Preview the histogram.
                >>> _ = plt.hist(data)

                >>> X, Y, max_x = stats.kde(data=data, n=500)
                >>> plt.plot(X, Y)

                >>> # Show X value at peak of curve.
                >>> max_x
                -9.718684033029376

        :Max X:
            This function also returns the X value of the curve's peak;
            where ``max_x`` is the ``X`` value corresponding to the max
            ``Y`` value on the curve. The result (``max_x``) is
            returned as the third tuple element.

        :Further Detail:
            This method uses the :func:`scipy.stats.gaussian_kde` method
            for the KDE calculation. For further detail on the
            calculation itself, refer to that function's docstring.

        :Background:
            Originally, :func:`plotly.figure_factory.dist_plot` was used
            to calculate the KDE. However, to remove the ``plotly``
            dependency from this library, their code was copied and
            refactored (simplified) into this function. Both the
            :func:`dist_plot` and :func:`pandas.DataFrame.plot.kde`
            method call :func:`scipy.stats.gaussian_kde` for the
            calculation, which this function also calls.

        Returns:
            tuple: A tuple containing the X-array, Y-array
            (both of ``n`` size), as well a the X value at max Y, as::

                (curve_x, curve_y, max_x)

        """
        try:
            data_ = self._obj_to_array(data=data)
            curve_x = np.linspace(data_.min(), data_.max(), n)
            curve_y = gaussian_kde(data_).evaluate(curve_x)
            max_x = curve_x[curve_y.argmax()]
            return (curve_x, curve_y, max_x)
        except Exception as err:
            reporterror(err)
        return (np.array(()), np.array(()), 0.0)

    @staticmethod
    def _obj_to_array(data: Union[list, np.array, pd.Series]) -> np.ndarray:
        """Convert an iterable object to a numpy array.

        Args:
            data (Union[list, np.array, pd.Series]): Array-like object
                to be converted into a ``numpy.ndarray``.

        :NaN Values:
            In addition to converting the following types to a
            ``numpy.ndarray``, any ``nan`` values are dropped from
            the ``numpy.array`` and ``pd.Series`` objects.

        Returns:
            np.array: A ``numpy.ndarray``, with ``nan`` values removed.

        """
        data_ = None
        if isinstance(data, np.ndarray):
            data_ = data
        elif isinstance(data, pd.Series):
            data_ = data.astype(float).to_numpy()
        elif isinstance(data, list):
            data_ = np.array(data)
        data_ = data_[~np.isnan(data_)]
        return data_


stats = Stats()
