/*
    Python wrapper for the _mathfunc.c module.
*/

#include <Python.h>
#include "libs/_mathfunc.h"

// Python docstrings.
const char _DOC_DIGITS[] = 
{ "Return the number of digits in an integer value.\n\n" 
  "Args:\n"
  "    n (int): Number whose digits are to be counted.\n\n"
  "Returns:\n"
  "    int: Number of digits in n."
};
const char _DOC_ESIEVE[] = 
{ "Implementation of the Sieve of Eratosthenes.\n\n"
  "This method returns an indexed boolean array where 1 indicates the\n"
  "index of a prime number, and 0 indicates the index of a composite\n"
  "number. Alternatively, if the deindex parameter is True, the prime\n"
  "numbers themselves are returned.\n\n"
  "Args:\n"
  "    n (int): Number to which the prime index is generated. This number\n"
  "        is *not* included in the results.\n"
  "    deindex (bool): De-index the array and return prime numbers.\n\n"
  "Returns:\n"
  "    list: If deindex is True, a list of prime numbers up to (n).\n"
  "    If deindex is False, a boolean list of prime/composite flags, where\n"
  "    1 indicates a prime number, and 0 indicates a composite number."
};
const char _DOC_FIB[] = 
{ "Generate the Fibonacci sequence to index (N), inclusive.\n\n"
  "Args:\n"
  "    n (int): Ending Fibonacci index, inclusive.\n\n"
  "Returns:\n"
  "    list: A list of the Fibonacci numbers to index N, inclusive."
};
const char _DOC_FIB_INDEX[] =
{ "Calculate the Fibonacci index (floor) closest related to (n).\n\n"
  "Args:\n"
  "    n (int): Number from which the Fibonacci index is calculated.\n\n"
  "Returns:\n"
  "    int: The floor of the calculation, resulting in the index closest\n"
  "    related to the given number."
};
const char _DOC_GCD[] = 
{ "Calculate the greatest common divisor of integers A and B.\n\n"
  "Args:\n"
  "    a (int): Integer value A.\n"
  "    b (int): Integer value B.\n\n"
  "Returns:\n"
  "    int: The GCD of integers A and B."
};
const char _DOC_INTCONCAT[] = 
{ "Concatenate two integers.\n\n"
  "Args:\n"
  "    x (int): Integer A.\n"
  "    y (int): Integer B.\n\n"
  "Returns:\n"
  "    int: Integers A and B concatenated together as AB."
};
const char _DOC_INT_NBITS[] = 
{ "Return the number of bits (n) occupies.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    int: Number of bits occupied by (n)."
};
const char _DOC_IS_PANDIGITAL[] = 
{ "Test if a number is a *zeroless* pandigital number.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"  
  "Note:\n"
  "    This method will *not* work if the number contains a zero. This\n"
  "    *must* be a *zeroless* pandigital number. Additionally, the digits\n"
  "    in the number must be *unique*. If a digit is duplicated, the\n"
  "    function will return 0.\n\n" 
  "Returns:\n"
  "    int: 1 if the number is pandigital, otherwise 0."
};
const char _DOC_IS_PALINDROME_NUM[] = 
{ "Test if a number is palindromatic.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    int: 1 if the number is palindromatic, otherwise 0."
};
const char _DOC_IS_PENTAGONAL[] = 
{ "Test if a number is pentagonal.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    int: 1 if the number is pentagonal, otherwise 0."
};
const char _DOC_IS_PERFECT[] = 
{ "Test if a number is perfect.\n\n"
  "Note: The only perfect numbers less than 1000000 are:\n"
  "  8, 28, 496 and 8128.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    bool: True if the number is perfect, otherwise False."
};
const char _DOC_IS_PERMUTATION[] = 
{ "Test if two positive integers are permutations of each other.\n\n"
  "Args:\n"
  "    a (int): Integer to be tested.\n"
  "    b (int): Integer to be tested.\n\n"
  "Returns:\n"
  "    bool: True if the numbers are permutations, otherwise False."
};
const char _DOC_IS_PRIME[] = 
{ "Test if a number is prime.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    int: 1 if the number is prime, otherwise 0."
}; 
const char _DOC_IS_TRIANGULAR[] = 
{ "Test if a number is triangular.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"
  "Returns:\n"
  "    int: 1 if the number is triangular, otherwise 0."
};
const char _DOC_LCM[] = 
{ "Calculate the least common multiple of integers A and B.\n\n"
  "Args:\n"
  "    a (int): Integer A.\n"
  "    b (int): Integer b.\n\n"
  "Returns:\n"
  "    int: The LCM of integers A and B."
};
const char _DOC_PHI[] = 
{ "Calculate the result of the phi (or Euler's totient) function.\n\n"
  "The phi function gives the count of positive integers less than N,\n"
  "which are co-prime (or relatively prime) to N.\n\n"
  "If N is prime, the result of the phi function is N-1.\n\n"
  "Args:\n"
  "    n (int): Integer for which phi is calculated.\n\n"
  "Returns:\n"
  "    int: The result of the phi function.\n"
};
const char _DOC_PHI_CONST[] = 
{ "Return the value of PHI.\n\n"
  "The Golden Ratio is calculated as:\n\n"
  "    (1 + sqrt(5)) / 2\n\n"
  "Returns:\n"
  "    int: The value of PHI."
};
const char _DOC_PRIMEFACTORS[] = 
{ "Calculate the prime factors of (n), where n > 0.\n\n"
  "Args:\n"
  "    n (int): Number to be factorised.\n\n"
  "Returns:\n"
  "    list: A list containing the prime factors of (n)."
}; 
const char _DOC_REVERSE[] = 
{ "Reverse an integer value.\n\n"
  "Args:\n"
  "    n (int): Number to be reversed.\n\n"
  "Returns:\n"
  "    int: The passed integer, reversed."
}; 
const char _DOC_ROTATE[] = 
{ "Rotate an integer value, where the last digit becomes the first.\n\n"
  "Args:\n"
  "    n (int): Number to be rotated.\n\n"
  "Returns:\n"
  "    int: The number (n), rotated 1 position to the right."
 };
const char _DOC_SIZES[] = 
{ "Display platform-specific data type sizes and ranges.\n\n"
  "Returns:\n"
  "    bool: 0 if successful, otherwise non-zero."
};
const char _DOC_VERSION[] =
{ "Display the embedded mathfunc version.\n" };

// Method definitions.
static PyObject *mathfunc_digits(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", digits(i));
}

static PyObject *mathfunc_esieve(PyObject *self, PyObject *args) {
    int n;
    bool deindex = 0;
    if ( !PyArg_ParseTuple(args, "ib", &n, &deindex) ) {
        return NULL;
    }
    PyObject *list = PyList_New(0);
    // malloc used as static array allocation runs out of
    // stack memory with large allocations.
    bool *ptr_P = (bool *)malloc(n * sizeof(bool));
    bool *cptr_P = ptr_P;  // Copy of the pointer for free.
    if ( ptr_P == NULL ) {
        fprintf(stderr, "Array allocation failed.\n");
        return list;
    }
    esieve(ptr_P, n);
    if ( deindex ) {
        // Return array of prime numbers.
        for ( int i = 0; i < n; ++i, ++ptr_P ) {
            if ( *ptr_P ) 
                PyList_Append(list, PyLong_FromDouble(i));
        }
    } else {
        // Return the indexed boolean array.
        for ( int i = 0 ; i < n; ++i, ++ptr_P )
            PyList_Append(list, PyLong_FromDouble(*ptr_P));
    }
    free(cptr_P);
    return list;
}

static PyObject *mathfunc_fib(PyObject *self, PyObject *args) {
    int n;
    if ( !PyArg_ParseTuple(args, "i", &n) ) {
        return NULL;
    }
    unsigned long long *ptr_f = fib(n);
    PyObject *list = PyList_New(0);
    // Convert Fibonacci sequence array into a Python list.
    // Uses indexing rather than pointer truthiness as the first value is 0.
    for ( int i = 0; i <= n; ++i )
        PyList_Append(list, PyLong_FromDouble(ptr_f[i]));
    // Deallocate memory allocated by fib function.
    free(ptr_f);
    return list;
}

static PyObject *mathfunc_fib_index(PyObject *self, PyObject *args) {
    unsigned long long i;
    if ( !PyArg_ParseTuple(args, "K", &i) )
        return NULL;
    return Py_BuildValue("i", fib_index(i));
}

static PyObject *mathfunc_gcd(PyObject *self, PyObject *args) {
    long a, b;
    if ( !PyArg_ParseTuple(args, "ll", &a, &b) )
        return NULL;
    return Py_BuildValue("l", gcd(a, b));
}

static PyObject *mathfunc_intconcat(PyObject *self, PyObject *args) {
    long long a, b;
    if ( !PyArg_ParseTuple(args, "LL", &a, &b) )
        return NULL;
    return Py_BuildValue("L", intconcat(a, b));
}

static PyObject *mathfunc_int_nbits(PyObject *self, PyObject *args) {
    long long n;
    if ( !PyArg_ParseTuple(args, "L", &n) )
        return NULL;
    return Py_BuildValue("i", int_nbits(n));
}

static PyObject *mathfunc_is_palindrome_num(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_palindrome_num(i));
}

static PyObject *mathfunc_is_pandigital(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_pandigital(i));
}

static PyObject *mathfunc_is_pentagonal(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_pentagonal(i));
}

static PyObject *mathfunc_is_perfect(PyObject *self, PyObject *args) {
    int i;
    if ( !PyArg_ParseTuple(args, "i", &i) )
        return NULL;
    return Py_BuildValue("i", is_perfect(i));
}

static PyObject *mathfunc_is_permutation(PyObject *self, PyObject *args) {
    int a, b;
    if ( !PyArg_ParseTuple(args, "ii", &a, &b) )
        return NULL;
    return Py_BuildValue("i", is_permutation(a, b));
}

static PyObject *mathfunc_is_prime(PyObject *self, PyObject *args) {
    unsigned long i;
    if ( !PyArg_ParseTuple(args, "k", &i) )
        return NULL;
    return Py_BuildValue("i", is_prime(i));
}

static PyObject *mathfunc_is_triangular(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_triangular(i));
}

static PyObject *mathfunc_lcm(PyObject *self, PyObject *args) {
    long a, b;
    if ( !PyArg_ParseTuple(args, "ll", &a, &b) )
        return NULL;
    return Py_BuildValue("l", lcm(a, b));
}
static PyObject *mathfunc_phi(PyObject *self, PyObject *args) {
    unsigned long n;
    if ( !PyArg_ParseTuple(args, "k", &n) )
        return NULL;
    return Py_BuildValue("k", phi(n));
}
static PyObject *mathfunc_phi_const(PyObject *self, PyObject *args) {
    return Py_BuildValue("d", PHI());
}
static PyObject *mathfunc_primefactors(PyObject *self, PyObject *args) {
    unsigned long n;
    if ( !PyArg_ParseTuple(args, "k", &n) ) {
        return NULL;
    }
    unsigned long *ptr_f = primefactors(n);
    PyObject *list = PyList_New(0);
    // Convert primes from array pointer into a Python list.
    for ( int i = 0; ptr_f[i] ; ++i ) {
        PyList_Append(list, PyLong_FromDouble(ptr_f[i]));
    }
    // Deallocate memory allocated by primefactors function.
    free(ptr_f);
    return list;
}

static PyObject *mathfunc_reverse(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("L", reverse(i));
}

static PyObject *mathfunc_rotate(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("L", rotate(i));
}

static PyObject *mathfunc_sizes(PyObject *self, PyObject *args) {
    if ( sizes() )
        return NULL;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *mathfunc_version(PyObject *self, PyObject *args) {
    const char *version = VERSION;
    return Py_BuildValue("s", version);
}

static PyMethodDef mathfunc_methods[] = {
    {"PHI", mathfunc_phi_const, METH_NOARGS, _DOC_PHI_CONST},
    {"digits", mathfunc_digits, METH_VARARGS, _DOC_DIGITS},
    {"esieve", mathfunc_esieve, METH_VARARGS, _DOC_ESIEVE},
    {"fib", mathfunc_fib, METH_VARARGS, _DOC_FIB},
    {"fib_index", mathfunc_fib_index, METH_VARARGS, _DOC_FIB_INDEX},
    {"gcd", mathfunc_gcd, METH_VARARGS, _DOC_GCD},
    {"intconcat", mathfunc_intconcat, METH_VARARGS, _DOC_INTCONCAT},
    {"int_nbits", mathfunc_int_nbits, METH_VARARGS, _DOC_INT_NBITS},
    {"is_palindrome_num", mathfunc_is_palindrome_num, METH_VARARGS, _DOC_IS_PALINDROME_NUM},
    {"is_pandigital", mathfunc_is_pandigital, METH_VARARGS, _DOC_IS_PANDIGITAL},
    {"is_pentagonal", mathfunc_is_pentagonal, METH_VARARGS, _DOC_IS_PENTAGONAL},
    {"is_perfect", mathfunc_is_perfect, METH_VARARGS, _DOC_IS_PERFECT},
    {"is_permutation", mathfunc_is_permutation, METH_VARARGS, _DOC_IS_PERMUTATION},
    {"is_prime", mathfunc_is_prime, METH_VARARGS, _DOC_IS_PRIME},
    {"is_triangular", mathfunc_is_triangular, METH_VARARGS, _DOC_IS_TRIANGULAR},
    {"lcm", mathfunc_lcm, METH_VARARGS, _DOC_LCM},
    {"phi", mathfunc_phi, METH_VARARGS, _DOC_PHI},
    {"primefactors", mathfunc_primefactors, METH_VARARGS, _DOC_PRIMEFACTORS},
    {"reverse", mathfunc_reverse, METH_VARARGS, _DOC_REVERSE},
    {"rotate", mathfunc_rotate, METH_VARARGS, _DOC_ROTATE},
    {"sizes", mathfunc_sizes, METH_NOARGS, _DOC_SIZES},
    {"version", mathfunc_version, METH_NOARGS, _DOC_VERSION},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mathfunc_module = {
    PyModuleDef_HEAD_INIT,
    "mathfunc",
    "Mathematical functions and supporting calculations, implemented in C for efficiency.",
    -1,
    mathfunc_methods
};

PyMODINIT_FUNC PyInit_mathfunc(void) {
    return PyModule_Create(&mathfunc_module);
}

