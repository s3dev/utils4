/**
    General mathematical functions and supporting utilities library.

    This C module is designed to be accessed as utils4.mathfuncs, in 
    Python.
*/

#include <float.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define PHI (1 + sqrt(5)) / 2

// ------------------------------------------------------------------
//
// Function prototypes on which other functions rely are placed here
// at the top of the module.
//

long long reverse(long n);

// ------------------------------------------------------------------


/**
    Count the number of digits in an integer value.

    @param n  Number whose digits are to be counted.
    @return   Number of digits in the number (n).
*/
int digits(long n) {
    int c = 0;
    n = ( n > 0 ) ? n : -n;  // Support for negative numbers;
    if ( n == 0 )
        return 1;
    while (n >= 1) {
        n /= 10;
        c++;
    }
    return c;
}

/**
    Implementation of the Sieve of Eratosthenes which returns a pointer
    to an array of indexed boolean values, where 1 indicates a prime 
    number and 0 indicates a composite number.

    The `n` argument is the number to which the primes are generated,
    *not* generate the first (n) primes.

    @param *P  Pointer to an empty array for the primes numbers indexes.
    @param n   Generate an array of primes until this number, exclusive.
*/
void esieve(int *P, int n) {
    int j;
    int i = 2;
    // Initialise the array to 1's.
    for ( int i = 0; i < n; ++i ) P[i] = 1;
    // Sieve
    while ( i*i < n ) {
        if ( P[i] ) {
            for ( j = i*i; j < n; j += i )
                P[j] = 0;
        }
        ++i;
    }
    P[0] = 0;
    P[1] = 0;
}

/**
    Generate the Fibonacci sequence to index (N), inclusive.

    This function tests for an unsigned integer 'overflow' and stops
    generating the sequence when an overflow is detected, leaving all
    remaining values as their initialised value of 0.

    The overflow is detected using the system's ULLONG_MAX limit.
    
    Reminder:
        It is the responsibility of the *caller* to free the memory 
        allocated by this function.

    @param n  Ending index of the sequence, inclusive.
    @return   A pointer to the sequence array.
*/
unsigned long long *fib(int n) {

    int i;
    unsigned long long *ptr_f = (unsigned long long *)calloc(102, sizeof(unsigned long long));

    // Initialise and advance the pointer.
    *ptr_f++ = 0;
    *ptr_f++ = 1;

    for ( i = 2; i <= n; ++i, ++ptr_f ) {
        // Watch for integer overflow.
        if ( (*(ptr_f - 1) < ULLONG_MAX - *(ptr_f - 2)) ) {
            *ptr_f = *(ptr_f - 1) + *(ptr_f - 2);
        } else {
            printf("Overflow detected.\n");
            break;
        }
    }
    return ptr_f - i;
}

/**
    Return the Fibonacci index (floor) closest related to (n).

    @param n  Number for which the Fibonacci index is calculated.
*/
int fib_index(unsigned long long n) {
    return floor(log(n * sqrt(5) + 0.5) / log(PHI));
}

/**
    Calculate the greatest common divisor of integers a and b.

    @param a  Integer A.
    @param b  Integer B.
    @return   The GCD of A and B.
*/
long gcd(long a, long b) {
    long tmp;
    while ( b != 0 ) {
        tmp = a % b;
        a = b;
        b = tmp;
    }
    return a;
}

/**
    Concatenate two integers.

    @param x Integer A.
    @param y Integer B.
    @return  Integers A and B concatenated together as AB.
*/
long long intconcat(long long x, long long y) {
    long long pow = 10;
    while ( y >= pow ) pow *= 10;
    return x * pow + y;
}

/**
    Calculate the number of bits in a long long int.

    @param n Number to be tested.
    @return  The number of bits occupied by (n).
*/
int int_nbits(long long n) {
    int c = 1;
    if ( n == 0 ) return 0;
    while ( (n >>= 1) >= 1 ) ++c;
    return c;
}

/** 
    Test if a number is palindromatic.

    @param n  Number to be tested.
    @return   1 if the number is palindromatic, otherwise 0.
*/
bool is_palindrome_num(long n) {
    long rev;
    // Store absolute value of n.
    if ( n < 0 ) n = -n;
    rev = reverse(n);
    return ( n == rev) ? 1 : 0;
}

/**
    Test if a number is pandigital.

    :Criteria:
        - The number must *not* contain a zero.
        - Digits *must* be unique.

    @param n  Number to be tested.
    @return   1 if the number is pandigital, otherwise 0.
*/
bool is_pandigital(long n) {
    long d = 0;
    int e = (1 << (digits(n) + 1)) - 2;
    while (n > 0) {
        d |= 1 << (int)(n - (floor(n / 10) * 10));
        n = floor(n / 10);
    }
    return (d == e) ? 1 : 0;
}

/**
    Test if a number is pentagonal.

    @param n  Number to be tested.
    @return   1 if the number is pentagonal, otherwise 0.
*/
bool is_pentagonal(long n) {
    if (n == 0) return 0;
    float pent = ((sqrt(1 + 24*n) + 1) / 6);
    return ( !(fmod(pent, 1)) );
}

/**
    Test if (n) is a perfect number.

    A perfect number is defined as a positive integer that is equal to the
    sum of its positive divisors, excluding itself.

    Note: The only perfect numbers below 1000000 are: 6, 28, 496 and 8128.

    @param n Number to be tested.
    @return  True if (n) is perfect, otherwise False.
*/
bool is_perfect(unsigned int n) {

    unsigned int sum = 0;
    unsigned int i = 1;

    for ( ; i < n / 2+1; ++i ) {
        if ( !(n % i) ) sum += i;
    }
    return ( sum == n ) ? 1 : 0;

}

/**
    Test if a number is prime.

    @param n  Number to be tested.
    @return   1 if the number is prime, otherwise 0.
*/
bool is_prime(unsigned long n) {
    if (n == 2)
        return 1;
    else if ( !(n % 2) | (n < 2) )
        return 0;
    else {
        for ( int i = 3; i <= sqrt(n); i += 2 ) {
            if ( !(n % i) )
                return 0;
        }
    }
    return 1;
}

/**
    Test if a number is triangular.

    @param n  Number to be tested.
    @return   1 if the number is triangular, otherwise 0.
*/
bool is_triangular(long n) {
    if (n == 0) return 0;
    float tri = ((sqrt(1 + 8*n) + 1) / 2);
    return ( !(fmod(tri, 1)) );
}

/**
    Calculate the lease common multiple of integers A and B.

    @param a  Integer A.
    @param b  Integer B.
    @return   The LCM of A and B.
*/
long lcm(long a, long b) {
    if ( (a < 0) | (b < 0) ) {
        printf("ValueError: One or both of the passed integers are less than zero.\n");
        return -1;
    } else {
        return (a*b) / gcd(a, b);
    }
}

/**
    Calculate the value of PHI.

    @return  The value of PHI, as (1 + sqrt(5)) / 2.
*/
double phi(void) {
    return PHI;
}

/**
    Generate an array of prime factors of N, where N > 0.

    Reminder:
        It is the responsibility of the *caller* to free the memory 
        allocated by this function.

    @param N  Positive number to factorise.
    @return   Pointer to the prime factors array.
*/
unsigned long *primefactors(unsigned long N) {
    
    float sqrtN = sqrt(N);
    unsigned long *ptr_arr = (unsigned long *)calloc(256, sizeof(unsigned long));
    int curr = 0;
    int p = 3;

    while ( N >= 2 ) {
        // Primality test.
        if ( is_prime(N) ) {
            ptr_arr[curr++] = N;  
            break;
        } 
        // Evens test.
        if ( !(N % 2) ) {
            ptr_arr[curr++] = 2;  
            N /= 2;
        } else {
            // Loop to find next prime.
            while ( p <= sqrtN ) {
                if ( !(N % p) ) {
                    ptr_arr[curr++] = p;
                    N /= p;
                    p = 3;
                    break;  // In case n is now prime.
                } else {
                    p += 2;
                }
            }
        }
    }
    return ptr_arr;
}

/**
    Reverse an integer.

    @param n  Number to be reversed.
    @returns  The value of (n), reversed.
*/
long long reverse(long n) {

    bool neg = n < 0;
    int d = digits(n) - 1;
    long long new = 0;

    // Account for negative values.
    if ( neg ) n = -n;
    while ( n >=1 ) {
        new += n % 10 * pow(10, d);
        n /= 10;
        --d;
    }
    return ( neg ) ? -new : new;
}

/**
    Rotate (n), moving the last digit to the first.

    @param n  Number to be rotated.
    @return   The number (n), rotated left to right.
*/
long long rotate(long n) {
    int d = digits(n);
    int r = n % 10;
    long v = floor(n / 10);
    return (r * pow(10, d - 1)) + v; 
}

/**
    Print the data type size and ranges to a table.
*/
int sizes(void) {
    printf("\n");
    printf(" Datatype\t Size (bytes)\n");
    printf("----------\t--------------\n");
    printf(" %-10s\t %7ld\n", "bool", sizeof(_Bool));
    printf(" %-10s\t %7ld\n", "short", sizeof(short));
    printf(" %-10s\t %7ld\n", "ushort", sizeof(unsigned short));
    printf(" %-10s\t %7ld\n", "int", sizeof(int));
    printf(" %-10s\t %7ld\n", "uint", sizeof(unsigned int));
    printf(" %-10s\t %7ld\n", "long", sizeof(long));
    printf(" %-10s\t %7ld\n", "ulong", sizeof(unsigned long));
    printf(" %-10s\t %7ld\n", "llong", sizeof(long long));
    printf(" %-10s\t %7ld\n", "ullong", sizeof(unsigned long long));
    printf(" %-10s\t %7ld\n", "float", sizeof(float));
    printf(" %-10s\t %7ld\n", "double", sizeof(double));
    printf(" %-10s\t %7ld\n", "long double", sizeof(long double));
    printf("\n");
    
    printf(" Datatype\t Range\n");
    printf("----------\t--------------\n");
    printf(" %-10s\t %d - %d\n", "short", SHRT_MIN, SHRT_MAX);
    printf(" %-10s\t %d - %d\n", "ushort", 0, USHRT_MAX);
    printf(" %-10s\t %d - %d\n", "int", INT_MIN, INT_MAX);
    printf(" %-10s\t %d - %u\n", "uint", 0, UINT_MAX);
    printf(" %-10s\t %ld - %ld\n", "long", LONG_MIN, LONG_MAX);
    printf(" %-10s\t %d - %lu\n", "ulong", 0, ULONG_MAX);
    printf(" %-10s\t %lld - %lld\n", "long long", LLONG_MIN, LLONG_MAX);
    printf(" %-10s\t %d - %llu\n", "ulong long", 0, ULLONG_MAX);
    printf(" %-10s\t %.5e - %.5e\n", "float", FLT_MIN, FLT_MAX);
    printf(" %-10s\t %.5e - %.5e\n", "double", DBL_MIN, DBL_MAX);
    printf(" %-10s\t %.5Le - %.5Le\n", "long double", LDBL_MIN, LDBL_MAX);
    printf("\n");
    
    printf(" Exit Type\t Value\n");
    printf("-----------\t--------------\n");
    printf(" %-10s\t %7d\n", "EXIT_SUCCESS", EXIT_SUCCESS);
    printf(" %-10s\t %7d\n", "EXIT_FAILURE", EXIT_FAILURE);
    printf("\n");

    return EXIT_SUCCESS;
}

