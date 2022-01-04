/*
    Python wrapper for the libmfunc.c module.
*/

#include <Python.h>
#include "libs/libmfunc.h"

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
  "number.\n\n"
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
{ "Return the Fibonacci number for the given index.\n\n"
  "Args:\n"
  "    n (int): Fibonacci index.\n\n"
  "Returns:\n"
  "    int: The Fibonacci number for the given index."
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
const char _DOC_IS_PANDIGITAL[] = 
{ "Test if a number is a *zeroless* pandigital number.\n\n"
  "Args:\n"
  "    n (int): Number to be tested.\n\n"  
  "Note:\n"
  "    This method will *not* work if the number contains a zero. This\n"
  "    *must* be a *zeroless* pandigital number.\n\n" 
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
{ "Return the value of PHI.\n\n"
  "The Golden Ratio is calculated as:\n\n"
  "    (1 + sqrt(5)) / 2\n\n"
  "Returns:\n"
  "    int: The value of PHI."
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
  "    None"
};


// Method definitions.
static PyObject *libmfunc_digits(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", digits(i));
}

static PyObject *libmfunc_esieve(PyObject *self, PyObject *args) {
    int n;
    bool deindex = 0;
    if ( !PyArg_ParseTuple(args, "ib", &n, &deindex) ) {
        return NULL;
    }
    int P[n];
    int *ptr_P = P;
    esieve(ptr_P, n);
    PyObject *list = PyList_New(0);
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
    return list;
}

static PyObject *libmfunc_fib(PyObject *self, PyObject *args) {
    int i;
    if ( !PyArg_ParseTuple(args, "i", &i) )
        return NULL;
    return Py_BuildValue("K", fib(i));
}

static PyObject *libmfunc_fib_index(PyObject *self, PyObject *args) {
    unsigned long long i;
    if ( !PyArg_ParseTuple(args, "K", &i) )
        return NULL;
    return Py_BuildValue("i", fib_index(i));
}

static PyObject *libmfunc_gcd(PyObject *self, PyObject *args) {
    long a, b;
    if ( !PyArg_ParseTuple(args, "ll", &a, &b) )
        return NULL;
    return Py_BuildValue("l", gcd(a, b));
}

static PyObject *libmfunc_is_palindrome_num(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_palindrome_num(i));
}

static PyObject *libmfunc_is_pandigital(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_pandigital(i));
}

static PyObject *libmfunc_is_pentagonal(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_pentagonal(i));
}

static PyObject *libmfunc_is_prime(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_prime(i));
}

static PyObject *libmfunc_is_triangular(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("i", is_triangular(i));
}

static PyObject *libmfunc_lcm(PyObject *self, PyObject *args) {
    long a, b;
    if ( !PyArg_ParseTuple(args, "ll", &a, &b) )
        return NULL;
    return Py_BuildValue("l", lcm(a, b));
}

static PyObject *libmfunc_phi(PyObject *self, PyObject *args) {
    return Py_BuildValue("d", phi());
}

static PyObject *libmfunc_reverse(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("L", reverse(i));
}

static PyObject *libmfunc_rotate(PyObject *self, PyObject *args) {
    long i;
    if ( !PyArg_ParseTuple(args, "l", &i) )
        return NULL;
    return Py_BuildValue("L", rotate(i));
}

static PyObject *libmfunc_sizes(PyObject *self, PyObject *args) {
    if ( sizes() )
        return NULL;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef libmfunc_methods[] = {
    {"digits", libmfunc_digits, METH_VARARGS, _DOC_DIGITS},
    {"esieve", libmfunc_esieve, METH_VARARGS, _DOC_ESIEVE},
    {"fib", libmfunc_fib, METH_VARARGS, _DOC_FIB},
    {"fib_index", libmfunc_fib_index, METH_VARARGS, _DOC_FIB_INDEX},
    {"gcd", libmfunc_gcd, METH_VARARGS, _DOC_GCD},
    {"is_palindrome_num", libmfunc_is_palindrome_num, METH_VARARGS, _DOC_IS_PALINDROME_NUM},
    {"is_pandigital", libmfunc_is_pandigital, METH_VARARGS, _DOC_IS_PANDIGITAL},
    {"is_pentagonal", libmfunc_is_pentagonal, METH_VARARGS, _DOC_IS_PENTAGONAL},
    {"is_prime", libmfunc_is_prime, METH_VARARGS, _DOC_IS_PRIME},
    {"is_triangular", libmfunc_is_triangular, METH_VARARGS, _DOC_IS_TRIANGULAR},
    {"lcm", libmfunc_lcm, METH_VARARGS, _DOC_LCM},
    {"phi", libmfunc_phi, METH_NOARGS, _DOC_PHI},
    {"reverse", libmfunc_reverse, METH_VARARGS, _DOC_REVERSE},
    {"rotate", libmfunc_rotate, METH_VARARGS, _DOC_ROTATE},
    {"sizes", libmfunc_sizes, METH_NOARGS, _DOC_SIZES},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef libmfunc_module = {
    PyModuleDef_HEAD_INIT,
    "mathfunc",
    "Mathematical functions and supporting calculations, implemented in C for efficiency.",
    -1,
    libmfunc_methods
};

PyMODINIT_FUNC PyInit_mathfunc(void) {
    return PyModule_Create(&libmfunc_module);
}

