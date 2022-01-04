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

/**
    Function prototypes on which other functions rely are placed here
    at the top of the module.
*/
long long reverse(long n);


/**
    Return the number of digits in (n).
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
    //return P;
}

/**
    Return the Fibonacci number for the given index.

    This method uses rounding (ceil/floor) for the final value
    due to the truncation of fractional values in the casting
    from double to integer (unsigned long long) type.

    Note: This method is only accurate to index 75!

    TODO: This method should be updated to calculated the F(n) 
    iteratively to gain accruacy.
*/
unsigned long long fib(int n) {
    double f;
    unsigned long long f_;
    f = ( pow(PHI, n) - pow(-1 / PHI, n) ) / sqrt(5);
    f_ = ( (f - floor(f)) >= 0.5 ) ? ceil(f) : floor(f);
    return f_;
}

/**
    Return the Fibonacci index (floor) closest related to (n).
*/
int fib_index(unsigned long long n) {
    return floor(log(n * sqrt(5) + 0.5) / log(PHI));
}

/**
    Calculate the greatest common divisor of integers a and b.
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
    Test if a number is palindromatic.
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
        - The number must *not* include zero.
        - Digits *must* be unique.
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
    Return 1 if the number if pentagonal, else 0.
*/
bool is_pentagonal(long n) {
    if (n == 0) return 0;
    float pent = ((sqrt(1 + 24*n) + 1) / 6);
    return ( !(fmod(pent, 1)) );
}

/**
    Return 1 if the number is prime, otherwise 0.

    This prime algorithm has been optimised for efficiency.
*/
bool is_prime(long n) {
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
    Return 1 if the number is triangular, else 0.
*/
bool is_triangular(long n) {
    if (n == 0) return 0;
    float tri = (sqrt(1 + 8*n) + 1 / 2);
    return ( !(fmod(tri, 1)) );
}

/**
    Calculate the lease common multiple of integers A and B.
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
    Return the value of PHI.
*/
double phi(void) {
    return (1 + sqrt(5)) / 2;
}

/**
    Reverse an integer, return the reversed number.
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
