/*
    Header for the mathfunc general utilities and calculations library.
*/

#include <stdbool.h>

const char *VERSION = "1.1.1";

/** 
    The constant phi.

    @return The constant value of phi.
*/
double PHI(void);

/**
    Count the number of digits in an integer value.

    @param n  Number whose digits are to be counted.
    @return   Number of digits in n.
*/
int digits(long n);

/**
    Populate distinct integers to the passed array.

    This function uses a hash-table to identify distinct integers from the
    passed array.

    @param pvals  Pointer to an array containing integers.
                  Note: The end of this array is identified when a zero is 
                  encountered.
    @param pdist  Pointer to an array to contain the distinct values.
                  This array can be initialised to a single value,
                  as the function will reallocate as required.
                  Note: This array must be created using malloc and passed
                  as an address.
    @return       Number of distinct values added to the `pdist` array.

    Usage:

        int size;
        unsigned long *pfac = primefactors(n);
        unsigned long *pdist = (unsigned long *)malloc(sizeof(unsigned long));

        size = distinctn(pfac, &pdist);

        // ...

        free(pfac);
        free(pdist);

    Reminder:
        The *caller* is responsible for freeing values and distinct values
        arrays. 

*/
int distinctn(unsigned long *pvals, unsigned long **pdist);

/**
    Implementation of the Sieve of Eratosthenes.

    A pointer to an array allocated to contain (n) boolean indicators
    is passed into this function and populated with boolean values, 
    where 1 indicates the position of a a prime number and 0 indicates 
    the position of a composite number. If these indicators are indexed 
    (starting at zero), the primes themselves will be revealed.

    The `n` argument is the number to which the primes are generated,
    *not* generate the first (n) primes.

    @param *P  Pointer to an empty array for the primes numbers indexes.
    @param n   Generate an array of primes until this number, exclusive.

    Note: For primes > 1e6, it is better to allocate the array using
    malloc, rather than 'standard' array initialisation, due to the amount
    of allocation required.
*/
void esieve(bool *P, int n);

/**
    Generate the Fibonacci sequence to index (N), inclusive.

    This function tests for an unsigned integer 'overflow' and stops
    generating the sequence when an overflow is detected, leaving all
    remaining values as their initialised value of 0.

    The overflow is detected using the system's ULLONG_MAX limit.

    @param n  Ending index of the sequence, inclusive.
    @return   A pointer to the sequence array.
*/
unsigned long long *fib(int n);

/**
    Return the Fibonacci index (floor) closest related to (n).

    @param n  Number from which the Fibonacci index is calculated.
    @return   The floor of the calculation, resulting in the index
              closest related to the given number.
*/
int fib_index(unsigned long long n);

/**
    Calculate the greatest common divisor of integers A and B.

    @param a  Integer A.
    @param b  Integer B.
    @return   The GCD of integers A and B.
*/
long gcd(long a, long b);

/**
    Concatenate two integers.

    @param x Integer A.
    @param y Integer B.
    @return  Integers A and B concatenated together as AB.
*/
long long intconcat(long long x, long long y);

/**
    Calculate the number of bits in a long long int.

    @param n Number to be tested.
    @return  The number of bits occupied by (n).
*/
int int_nbits(long long n);

/**
    Test if a number is palindromatic.

    @param n  Number to be tested.
    @return   1 if the number of palindromatic, otherwise 0.
*/
bool is_palindrome_num(long n);

/**
    Test if a number is pandigital.

    @param n  Number to be tested.
    @return   1 if the number is pandigital, otherwise 0.
*/
bool is_pandigital(long n);

/**
    Test if a number is pentagonal.

    @param n  Number to be tested.
    @return   1 if the number is pentagonal, otherwise 0.
*/
bool is_pentagonal(long n);

/**
    Test if (n) is a perfect number.

    A perfect number is defined as a positive integer that is equal to the
    sum of its positive divisors, excluding itself.

    Note: The only perfect numbers below 1000000 are: 6, 28, 496 and 8128.

    @param n Number to be tested.
    @return  True if (n) is perfect, otherwise False.
*/
bool is_perfect(unsigned int n);

/**
    Test if two positive integers are permutations of eachother.

    @param a  Integer to be tested.
    @param b  Integer to be tested.
    @return   1 if the integers are permutations, otherwise 0.
*/
bool is_permutation(unsigned long long a, unsigned long long b);

/**
    Test if a number is prime.

    @param n  Number to be tested.
    @return   1 if the number is prime, otherwise 0.
*/
bool is_prime(unsigned long n);

/**
    Test if a number is triangular.

    @param n  Number to be tested.
    @return   1 if the number is triangular, otherwise 0.
*/
bool is_triangular(long n);

/**
    Calculate the least common multiple of integers A and B.

    @param a  Integer A.
    @param b  Integer B.
    @return   The LCM of integers A and B.
*/
long lcm(long a, long b);

/**
    Calculate the result of the phi (or Euler's totient) function.

    The phi function gives a count of positive integers less than N, which
    are co-prime (or relatively) prime to N.

    If N is prime, the result of the phi function is N-1.

    If N is not prime, the result is calculated as:

        phi(n) = n * Pi(1 - 1/p)

    where the product is obtained for all *distinct* prime factors of N,
    (or p).

    @param n  Integer for which phi is calculated.
    @return   The result of the phi function.
*/
unsigned long phi(unsigned long n);

/**
    Generate an array of prime factors of N, where N > 0.

    Reminder:
        The caller of this function is responsible for freeing the
        memory block allocated by this function.

    @param N  Positive number to factorise.
    @return   Pointer to the prime factors array.
*/
unsigned long *primefactors(unsigned long N);

/**
    Reverse a number.

    @param n  Number to be reversed.
    @return   The specified number, reversed.
*/
long long reverse(long n);

/**
    Rotate a number, moving the last digit to the first.

    @param n  Number to be rotated.
    @return   The specified number, rotated one position left to right.
*/
long long rotate(long n);

/**
    Print data type sizes and ranges to a table.

    @return 0 if successful, otherwise non-zero;
*/
int sizes(void);

