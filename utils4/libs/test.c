/**
    Testing module. *Not* for deployment use.
*/

#include <stdio.h>
#include "libmfunc.h"

void test_fib(void) {
    int test[] = {1, 5, 10, 25};
    int size = sizeof test / sizeof test[0];
    int *end = test + size;

    printf("Fibonacci Test:\n");
    for ( int *p = test; p < end; ++p ) {
        printf("- %d: %lld\n", *p, fib(*p));
    }
    printf("\n");
}

void test_fib_index(void) {
    int test[] = {5, 11, 13, 55, 56, 89, 90};
    int size = sizeof test / sizeof test[0];
    int *end = test + size;

    printf("Fibonacci Index Test:\n");
    for ( int *p = test; p < end; ++p ) {
        printf("- %d: %d\n", *p, fib_index(*p));
    }
    printf("\n");
}

void test_palindrome(void) {
    int test[] = { 12321, 98789, 5263625, 123, 654, 987654321 };
    int size = sizeof test / sizeof test[0];
    int *end = test + size;
    
    printf("Palindrome Test:\n");
    for ( int *p = test; p != end ; ++p ) {
        printf("- %d: %d\n", *p, is_palindrome_num(*p));
    }
    printf("\n");
}

void test_reverse(void) {
    long test[] = { 12, 110, 123, 1230, 987654321, -12, -110, -123, -1230, -987654321 };
    int size = sizeof test / sizeof test[0];
    long *end = test + size;
    
    printf("Reverse Test:\n");
    for ( long *p = test; p != end ; ++p ) {
        printf("- %ld: %ld\n", *p, reverse(*p));
    }
    printf("\n");
}

void test_sizes(void) {
    sizes();
}

int main(void) {

    printf("\n");
    test_fib();
    test_fib_index();
    test_palindrome();
    test_reverse();
    test_sizes();
    return 1;

}
