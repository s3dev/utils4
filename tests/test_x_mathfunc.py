#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``mathfunc`` module.

:Note:
            This test module tests the **installed** ``utils4.mathfunc``
            module, as this is a C implementation and therefore cannot be
            tested directly. Preferably, there should be an
            *dev release* of utils4 which can be installed locally where
            this module can be tested.

            Although some functions can be tested through ``ctypes`` the
            functions which return lists, such as ``esieve``, end in seg
            faults. Therefore, the full test is carried out on the
            *installed* library.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  Because this test module fiddles with (**destroys**)
            ``sys.path`` and ``sys.modules``, it's best to ensure this
            test runs **last**. Hence the ``_x_`` in the test module
            name.

"""
# Enable installed library testing.
# pylint: disable=global-statement
# pylint: disable=import-outside-toplevel
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=no-name-in-module
# pylint: disable=too-many-public-methods

import ctypes
import sys
try:
    from .base import TestBase
    from .testlibs import msgs
    from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    from testlibs.utilities import utilities
mathfunc = None  # Global placeholder for import

# Kept just in case.
# try:
#     _old_modules = sys.modules.copy()
#     _old_path = sys.path[:]
#     # Clear utils4 from imports to allow re-import.
#     keys = [k for k in sys.modules if 'utils4' in k]
#     for k in keys:
#         del sys.modules[k]
#     # Force import from *installed* library.
#     sys.path = [i for i in sys.path if 'site-packages' in i]
#     from utils4 import mathfunc
#     sys.path = _old_path[:]
#     sys.modules = _old_modules.copy()
# except ImportError as err:
#     sys.path = _old_path[:]
#     sys.modules = _old_modules.copy()
#     msgs.msgs.errors.importerror(msg=err)


class TestMathfunc(TestBase):
    """Testing class used to test the ``mathfunc`` module.

    :Test case ordering:
        The test cases in this module are listed in *alphabetical* order, per
        the method name - *not* the numerical test order number. Any new
        methods which are to be tested, should be listed in alphabetical
        order, although for example, ``test9__<tuv>`` sits between
        ``test2__<abc>`` and ``test3__<xyz>``.

    """

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Tasks to be run at the testing startup.

        :Tasks:
            - Print the start of test message.
            - Hack ``sys.modules`` and ``sys.path`` to allow import from
              *installed* ``utils4`` for C library testing.

        """
        msgs.startoftest.startoftest(module_name='mathfunc')
        # Clear utils4 from imports to allow re-import from installed.
        keys = [k for k in sys.modules if 'utils4' in k]
        for k in keys:
            del sys.modules[k]
        # Force import from *installed* library.
        sys.path = [i for i in sys.path if 'site-packages' in i]
        from utils4 import mathfunc as mathfunc_
        # Export the import to global namespace.
        global mathfunc
        mathfunc = mathfunc_

    # @classmethod
    # def tearDownClass(cls):
    #     """Print the test's startup message."""

    @staticmethod
    def _bytes_to_decimal__signed(nbytes) -> int:
        """Convert a number of (signed) bytes into its max decimal value."""
        return (1 << (8 * nbytes) - 1) - 1

    @staticmethod
    def _bytes_to_decimal__unsigned(nbytes) -> int:
        """Convert a number of (unsigned) bytes into its max decimal value."""
        return (1 << (8 * nbytes)) - 1

    def _input_filter(self, inp:int, signed:bool, dtype:str):
        """Remove any input values which exceed the platform's dtype length."""
        inp_ = inp[:]
        if signed:
            func = self._bytes_to_decimal__signed
        else:
            func = self._bytes_to_decimal__unsigned
        bytes_ = ctypes.sizeof(ctypes.__getattribute__(dtype))
        max_ = func(bytes_)
        for i in inp_:
            if (i < -max_-1) | (i > max_):  # < min or > max
                inp.pop()

    def test01__digits(self):
        """Test the ``digits`` method.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test five inputs and compare the number of digits returned
              from the func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        inp = [0, -73, 123, (1<<31)-1, (1<<63)-1]
        exp = [1, 2, 3, 10, 19]
        self._input_filter(inp=inp, **sig)
        for i, e in zip(inp, exp):
            with self.subTest(msg=f'i={i} e={e}'):
                test = mathfunc.digits(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test02__esieve_10_true(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the primes up to 10 are as expected.

        """
        exp = [2, 3, 5, 7]
        test = mathfunc.esieve(10, True)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test02__esieve_10_false(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the prime index up to 10 is as expected.

        """
        exp = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0]
        test = mathfunc.esieve(10, False)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test02__esieve_100_true(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the primes up to 100 are as expected.

        """
        exp = [2,3,5,7,11,13,17,19,23,29,31,37,41,
               43,47,53,59,61,67,71,73,79,83,89,97]
        test = mathfunc.esieve(100, True)
        utilities.assert_true_pyiter(expected=exp, test=test, msg=self._MSG1)

    def test02__esieve_100_false(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the prime index up to 100 is as expected, using only
              the first 10 and last 10 indexes.

        """
        exp_a = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0]
        exp_b = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        test = mathfunc.esieve(100, False)
        test_a = test[:10]
        test_b = test[-10:]
        for e, t in zip([exp_a, exp_b], [test_a, test_b]):
            with self.subTest(msg=f'exp={e} test={t}'):
                utilities.assert_true_pyiter(expected=e, test=t, msg=self._MSG1)

    def test02__esieve_10k_true(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the primes up to 10K are as expected, using only the
              first 10 after the 1000th index and last 10.

        """
        exp_a = [7927, 7933, 7937, 7949, 7951, 7963, 7993, 8009, 8011, 8017]
        exp_b = [9887, 9901, 9907, 9923, 9929, 9931, 9941, 9949, 9967, 9973]
        test = mathfunc.esieve(10000, True)
        test_a = test[1000:1010]
        test_b = test[-10:]
        for e, t in zip([exp_a, exp_b], [test_a, test_b]):
            with self.subTest(msg=f'exp={e} test={t}'):
                utilities.assert_true_pyiter(expected=e, test=t, msg=self._MSG1)

    def test02__esieve_10k_false(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the prime index up to 10K are as expected, using only
              the first 10 after the 1000th index and last 10.

        """
        exp_a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        exp_b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        test = mathfunc.esieve(10000, False)
        test_a = test[1000:1010]
        test_b = test[-10:]
        for e, t in zip([exp_a, exp_b], [test_a, test_b]):
            with self.subTest(msg=f'exp={e} test={t}'):
                utilities.assert_true_pyiter(expected=e, test=t, msg=self._MSG1)

    def test02__esieve_100m_true(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the primes up to 100M are as expected, using only the
              first 10 after the 1,000,000th index and last 10.

        """
        exp_a = [15485867, 15485917, 15485927, 15485933, 15485941,
                 15485959, 15485989, 15485993, 15486013, 15486041]
        exp_b = [99999787, 99999821, 99999827, 99999839, 99999847,
                 99999931, 99999941, 99999959, 99999971, 99999989]
        test = mathfunc.esieve(int(1e8), True)
        test_a = test[1_000_000:1_000_010]
        test_b = test[-10:]
        for e, t in zip([exp_a, exp_b], [test_a, test_b]):
            with self.subTest(msg=f'exp={e} test={t}'):
                utilities.assert_true_pyiter(expected=e, test=t, msg=self._MSG1)

    def test02__esieve_100m_false(self):
        """Test the ``esieve`` method.

        :Test:
            - Test the prime index up to 100M are as expected, using only
              the first 10 after the 1,000,000th index and last 10.

        """
        exp_a = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        exp_b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        test = mathfunc.esieve(int(1e8), False)
        test_a = test[1_000_000:1_000_010]
        test_b = test[-10:]
        for e, t in zip([exp_a, exp_b], [test_a, test_b]):
            with self.subTest(msg=f'exp={e} test={t}'):
                utilities.assert_true_pyiter(expected=e, test=t, msg=self._MSG1)

    def test06__fib(self):
        """Test the ``fib`` method.

        :Test:
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        inp = [1, 5, 7, 10, 25]
        exp = [[0, 1],
               [0, 1, 1, 2, 3, 5],
               [0, 1, 1, 2, 3, 5, 8, 13],
               [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
               [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55,
                89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765,
                10946, 17711, 28657, 46368, 75025]]
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.fib(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test07__fib_index(self):
        """Test the ``fib_index`` method.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        sig = {'signed': 0, 'dtype': 'c_ulonglong'}
        exp = [2, 5, 7, 7, 10, 10, 11, 11, 90]
        inp = [1, 5, 13, 14, 55, 59, 89, 90, 2880067194370816210]
        self._input_filter(inp=inp, **sig)
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.fib_index(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test03__gcd(self):
        """Test the ``gcd`` method.

        :Test:
            - Test five inputs and compare the GCD returned from the func
              with the expected value.

        """
        exp = [2, 10, 11, 13, 73]
        inp = [(8, 122), (10, 100), (55, 143), (39, 91), (219, 365)]
        for e, (a, b) in zip(exp, inp):
            with self.subTest(msg=f'input={a, b} exp={e}'):
                test = mathfunc.gcd(a, b)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test04__is_pandigital_true(self):
        """Test the ``is_pandigital`` method.

        :Test:
            - Test six inputs and compare the result returned from the
              func with the expected value.

        """
        inp = [1, 3412, 562413, 635241, 7564231, 987123456]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_pandigital(i)
                utilities.assert_true(expected=1, test=test, msg=self._MSG1)

    def test04__is_pandigital_false(self):
        """Test the ``is_pandigital`` method.

        :Test:
            - Test six inputs and compare the result returned from the
              func with the expected value.

        """
        inp = [2, 124, 5412, 62413, 152437, 98745632]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_pandigital(i)
                utilities.assert_true(expected=0, test=test, msg=self._MSG1)

    def test05__is_pentagonal_true(self):
        """Test the ``is_pentagonal`` method.

        :Test:
            - Test six inputs and compare the result returned from the
              func with the expected value.

        """
        inp = [1, 12, 22, 35, 210, 1335]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_pentagonal(i)
                utilities.assert_true(expected=1, test=test, msg=self._MSG1)

    def test05__is_pentagonal_false(self):
        """Test the ``is_pentagonal`` method.

        :Test:
            - Test six inputs and compare the result returned from the
              func with the expected value.

        """
        inp = [2, 15, 30, 45, 350, 2015]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_pentagonal(i)
                utilities.assert_true(expected=0, test=test, msg=self._MSG1)

    def test05__is_prime_true(self):
        """Test the ``is_prime`` method.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test eight inputs and compare the result returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        inp = [2, 13, 37, 73, 6700417, 2147483647, 999999000001, 67280421310721]
        self._input_filter(inp=inp, **sig)
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_prime(i)
                utilities.assert_true(expected=1, test=test, msg=self._MSG1)

    def test05__is_prime_false(self):
        """Test the ``is_prime`` method.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test seven inputs and compare the result returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        inp = [1, 9, 21, 39, 6700419, 2147483649, 999999000003]
        self._input_filter(inp=inp, **sig)
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_prime(i)
                utilities.assert_true(expected=0, test=test, msg=self._MSG1)

    def test08__is_triangular_true(self):
        """Test the ``is_triangular`` method.

        :Test:
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        inp = [1, 21, 78, 136, 231, 325, 465, 630]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_triangular(i)
                utilities.assert_true(expected=1, test=test, msg=self._MSG1)

    def test08__is_triangular_false(self):
        """Test the ``is_triangular`` method.

        :Test:
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        inp = [2, 22, 73, 137, 250, 330, 470, 650]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.is_triangular(i)
                utilities.assert_true(expected=0, test=test, msg=self._MSG1)

    def test09__lcm(self):
        """Test the ``lcm`` method.

        :Test:
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        exp = [4, 15, 65, 1400, 19416396]
        inp = [(2, 4), (3, 5), (5, 13), (56, 100), (12, 1618033)]
        for e, (a, b) in zip(exp, inp):
            with self.subTest(msg=f'input={a, b} exp={e}'):
                test = mathfunc.lcm(a, b)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test10__phi_const(self):
        """Test the ``PHI`` constant method.

        :Test:
            - Test the ``PHI`` method outputs the expected value, to 10
              decimal places.

        """
        exp = ( 1 + 5**0.5 ) / 2
        exp_s = f'{exp:.10f}'
        test = mathfunc.PHI()
        test_s = f'{test:.10f}'
        utilities.assert_true(expected=exp_s, test=test_s, msg=self._MSG1)

    def test11__reverse_neg(self):
        """Test the ``reverse`` method for negative integers.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        exp = [-1, -1, -11, -21, -321, -41, -10091, -69361491, -7463847412, -6927694924]
        inp = [-1, -10, -11, -120, -123, -1400, -19001, -19416396, -2147483647, -4294967296]
        self._input_filter(inp=inp, **sig)
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.reverse(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test11__reverse_pos(self):
        """Test the ``reverse`` method for positive integers.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        inp = [1, 10, 11, 120, 123, 1400, 19001, 19416396, 2147483647, 4294967296]
        exp = [1, 1, 11, 21, 321, 41, 10091, 69361491, 7463847412, 6927694924]
        self._input_filter(inp=inp, **sig)
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.reverse(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test12__rotate_neg(self):
        """Test the ``rotate`` method for negative integers.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        exp = [-1, -11, -12, -312, -140, -11900, -61941639, -7214748364, -6429496729]
        inp = [-1, -11, -120, -123, -1400, -19001, -19416396, -2147483647, -4294967296]
        self._input_filter(inp=inp, **sig)
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.rotate(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test12__rotate_pos(self):
        """Test the ``rotate`` method for positive integers.

        :Test:
            - The values in this test are filtered to remove test cases
              which will be known to fail due to varying
              (platform-specific) data type length.
            - Test (n) inputs and compare the output returned from the
              func with the expected value.

        """
        sig = {'signed': 1, 'dtype': 'c_long'}
        exp = [1, 11, 12, 312, 140, 11900, 61941639, 7214748364, 6429496729]
        inp = [1, 11, 120, 123, 1400, 19001, 19416396, 2147483647, 4294967296]
        self._input_filter(inp=inp, **sig)
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.rotate(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test15__prime_factors(self):
        """Test the ``prime_factors`` method.

        :Test:
            - Test a series of input values and ensure the expected list
              of primes factors is returned.

        """
        inp = [7, 10, 13, 25, 123456, 98765431, 987654321]
        exp = [[7],
               [2, 5],
               [13],
               [5, 5],
               [2, 2, 2, 2, 2, 2, 3, 643],
               [98765431],
               [3, 3, 17, 17, 379721]]
        for e, i in zip(exp, inp):
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.primefactors(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test16__intconcat(self):
        """Test the ``intconcat`` method.

        :Test:
            - verify integer concatenation is working as expected.

        """
        inp = [(1, 10), (200, 500), (123, 123), (123, 987), (123456, 987654)]
        exp = [110, 200500, 123123, 123987, 123456987654]
        for e, (a, b) in zip(exp, inp):
            with self.subTest(msg=f'input={a, b} exp={e}'):
                test = mathfunc.intconcat(a, b)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test17__int_nbits(self):
        """Test the ``int_nbits`` method.

        :Test:
            - Using Python's built-in :func:`~int(n).bit_length`
              function, verify the mathfunc is calculating the number of
              bits correctly.

        """
        inp = [0, 1, 3, 7, 8, 15, 16, 255, 256, 123456789, 987654321]
        for i in inp:
            with self.subTest(msg=f'input={i}'):
                exp = int(i).bit_length()
                test = mathfunc.int_nbits(i)
                utilities.assert_true(expected=exp, test=test, msg=self._MSG1)

    def test18__is_perfect(self):
        """Test the ``is_perfect`` method.

        :Test:
            - Verify the output for a list of numbers; four of which are
              the only perfect numbers less than 1000000.

        """
        inp = [(1, 0), (3, 0), (6, 1), (8, 0),              # 6
               (20, 0), (24, 0), (28, 1), (29, 0),          # 28
               (475, 0), (495, 0), (496, 1), (497, 0),      # 496
               (8120, 0), (8125, 0), (8128, 1), (8129, 0),  # 8128
               (10000, 0)]
        for i, e in inp:
            with self.subTest(msg=f'input={i} exp={e}'):
                test = mathfunc.is_perfect(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)

    def test19__is_permutation_true(self):
        """Test the ``is_permutation`` method.

        :Test:
            - Verify the provided integer pairs *are* a permutation of
              each other.

        """
        inp = ((12, 21), (123, 231), (1234, 4231), (12345, 54231),
               (123456, 645213), (1234567, 7564213),
               (12345678, 84765213), (123456789, 125634879),
               (1234567890, 1025364879))
        for a, b in inp:
            with self.subTest(msg=f'A={a} B={b}'):
                test = mathfunc.is_permutation(a, b)
                utilities.assert_true(expected=1, test=test, msg=self._MSG1)

    def test19__is_permutation_false(self):
        """Test the ``is_permutation`` method.

        :Test:
            - Verify the provided integer pairs are *not* a permutation
              of each other.

        """
        inp = ((12, 210), (123, 23), (1234, 423), (12345, 5423),
               (123456, 64521), (1234567, 756421),
               (12345678, 8476521), (123456789, 12563487),
               (1234567890, 102536487))
        for a, b in inp:
            with self.subTest(msg=f'A={a} B={b}'):
                test = mathfunc.is_permutation(a, b)
                utilities.assert_true(expected=0, test=test, msg=self._MSG1)

    def test20__phi(self):
        """Test the ``phi`` method.

        :Test:
            - Verify the ``phi`` function returns the expected number of
              co-primes for each N.

        """
        inp = (9, 10, 123, 1234, 12345, 123456, 1234567, 12345678,
               123456789, 1234567890,
               98, 987, 9876, 98765, 987654, 9876543, 98765432,
               987654321, 9876543210)
        exp = (6, 4, 80, 616, 6576, 41088,
               1224720, 4027392, 82260072, 329040288, 42, 552,
               3288, 79008, 325632, 6554904, 48047904,
               619703040, 2478812160)
        for i, e in zip(inp, exp):
            with self.subTest(msg=f'input={i}'):
                test = mathfunc.phi(i)
                utilities.assert_true(expected=e, test=test, msg=self._MSG1)
