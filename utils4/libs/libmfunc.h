/*
    Header for the general utilities and calculations library.
*/

#include <stdbool.h>

/**
    Return the number of digits in an integer value.

    @param n Number whose digits are to be counted.
    @return Number of digits in n.
*/
int digits(long n);

/**
    Implementation of the Sieve of Eratosthenes.

    Returns an indexed boolean array where 1 indicates the index of a 
    prime number, whereas 0 indicates the index of a composite number.

    @param *P Pointer to an array of (n) size.
    @param n Maximum number to which the prime index is generated.
    @return A pointer to the index array.
*/
int *esieve(int *P, int n);

/**
    Return the Fibonacci number for the given index.

    @param n Fibonacci index.
    @return The Fibonacci number for the given index.
*/
unsigned long long fib(int n);

/**
    Return the Fibonacci index (floor) closest related to (n).

    @param n Number from which the Fibonacci index is calculated.
    @return The floor of the calculation, resulting in the index
            closest related to the given number.
*/
int fib_index(unsigned long long n);

/**
    Calculate the greatest common divisor of integers A and B.

    @param a Integer A.
    @param b Integer B.
    @return The GCD of integers A and B.
*/
long gcd(long a, long b);

/**
    Test if a number is palindromatic.

    @param n Number to be tested.
    @return 1 if the number of palindromatic, otherwise 0.
*/
bool is_palindrome_num(long n);

/**
    Test if a number is pandigital.

    @param n Number to be tested.
    @return 1 if the number is pandigital, otherwise 0.
*/
bool is_pandigital(long n);

/**
    Test if a number is pentagonal.

    @param n Number to be tested.
    @return 1 if the number is pandigital, otherwise 0.
*/
bool is_pentagonal(long n);

/**
    Test if a number is prime.

    @param n Number to be tested.
    @return 1 if the number is prime, otherwise 0.
*/
bool is_prime(long n);

/**
    Test if a number is triangular.

    @param n Number to be tested.
    @return 1 if the number is triangular, otherwise 0.
*/
bool is_triangular(long n);

/**
    Calculate the least common multiple of integers A and B.

    @param a Integer A.
    @param b Integer B.
    @return The LCM of integers A and B.
*/
long lcm(long a, long b);

/**
    Return the value of PHI.

    Calculated as (1 + sqrt(5)) / 2

    @return Value of PHI.
*/
double phi(void);

/**
    Reverse a number.

    @param n Number to be reversed.
    @return The specified number, reversed.
*/
long long reverse(long n);

/**
    Rotate a number, moving the last digit to the first.

    @param n Number to be rotated.
    @return The specified number, rotated one position.
*/
long long rotate(long n);

/**
    Print data type sizes and ranges to a table.

    @return 0 if successful, otherwise non-zero;
*/
int sizes(void);

