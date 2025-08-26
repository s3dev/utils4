/*
    Python wrapper for the _futils.c module.
*/

#include <Python.h>
#include "libs/_futils.h"

// Python docstrings.
const char _DOC_IS7ZIP[] = 
{ "Test if a file is a 7-zip archive.\n\n"
  "Refer to the utils.is7zip docstring for further detail."
};
const char _DOC_ISASCII[] = 
{ "Test if a file is ASCII only.\n\n"
  "Refer to the utils.isascii docstring for further detail."
};
const char _DOC_ISBINARY[] = 
{ "Test if a file is binary (non-ASCII only).\n\n"
  "Refer to the utils.isbinary docstring for further detail."
};
const char _DOC_ISGZIP[] = 
{ "Test if a file is a GZIP compressed file.\n\n"
  "Refer to the utils.isgzip docstring for further detail."
};
const char _DOC_ISPDF[] = 
{ "Test if a file is a PDF file.\n\n"
  "Refer to the utils.ispdf docstring for further detail."
};
const char _DOC_ISZIP[] = 
{ "Test if a file is a ZIP archive.\n\n"
  "Refer to the utils.iszip docstring for further detail."
};

// Method definitions.
static PyObject *futils_is7zip(PyObject *self, PyObject *args) {
    const char *path;
    if ( !PyArg_ParseTuple(args, "s", &path) )
        return NULL;
    return Py_BuildValue("i", is7zip_(path));
}
static PyObject *futils_isascii(PyObject *self, PyObject *args) {
    const char *path;
    size_t sz;
    if ( !PyArg_ParseTuple(args, "sK", &path, &sz) )
        return NULL;
    return Py_BuildValue("i", isascii_(path, sz));
}
static PyObject *futils_isbinary(PyObject *self, PyObject *args) {
    const char *path;
    size_t sz;
    if ( !PyArg_ParseTuple(args, "sK", &path, &sz) )
        return NULL;
    return Py_BuildValue("i", isbinary_(path, sz));
}
static PyObject *futils_isgzip(PyObject *self, PyObject *args) {
    const char *path;
    if ( !PyArg_ParseTuple(args, "s", &path) )
        return NULL;
    return Py_BuildValue("i", isgzip_(path));
}
static PyObject *futils_ispdf(PyObject *self, PyObject *args) {
    const char *path;
    if ( !PyArg_ParseTuple(args, "s", &path) )
        return NULL;
    return Py_BuildValue("i", ispdf_(path));
}
static PyObject *futils_iszip(PyObject *self, PyObject *args) {
    const char *path;
    if ( !PyArg_ParseTuple(args, "s", &path) )
        return NULL;
    return Py_BuildValue("i", iszip_(path));
}

static PyMethodDef futils_methods[] = {
    {"is7zip", futils_is7zip, METH_VARARGS, _DOC_IS7ZIP},
    {"isascii", futils_isascii, METH_VARARGS, _DOC_ISASCII},
    {"isbinary", futils_isbinary, METH_VARARGS, _DOC_ISBINARY},
    {"isgzip", futils_isgzip, METH_VARARGS, _DOC_ISGZIP},
    {"ispdf", futils_ispdf, METH_VARARGS, _DOC_ISPDF},
    {"iszip", futils_iszip, METH_VARARGS, _DOC_ISZIP},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef futils_module = {
    PyModuleDef_HEAD_INIT,
    "futils",
    "Fast utility-based functions, implemented in C for efficiency.",
    -1,
    futils_methods
};

PyMODINIT_FUNC PyInit_futils(void) {
    return PyModule_Create(&futils_module);
}

