/**
    Purpose:    This module contains the C implementations for utils4's
                f(ast)utils module.

    Developer:  J Berendt
    Email:      development@3dev.uk

    Comments:   These C implementations were derived from the original
                Python implementations used in the badsnakes utilities
                module.

                The isascii_() function has an underscore appended to the
                name to differenciate it from the isascii() function in
                the standard library. The other functions have a trailing
                underscore for module consistency.

    Copyright (C) 73rd Street Development
    This file is part of the utils4 library.
*/

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/* Prototypes */
bool isascii_(const char *path, size_t sz);
bool isbinary_(const char *path, size_t sz);
bool iszip_(const char *path);
static bool _inasciirange(char c);

/**
    Determine if a file is plain-text (ASCII only).

    A file is deemed non-binary if *all* of the characters in the file
    are within ASCII's printable range.

    Design:
        This function simply inverts the return value of the isbinary 
        function. For design detail, refer to the isbinary documentation.
    
    @param path Pointer to the full path of the file to be tested.
    @param sz Number of bytes to be read in a each chunk.
    @return Returns True if *all* characters are within ASCII's printable
            range. Otherwise, False.
*/
bool
isascii_(const char *path, size_t sz) {
    return !isbinary_(path, sz);
}

/**
    Determine if a file is binary.

    A file is deemed non-binary if *all* of the characters in the file
    are within ASCII's printable range.

    Design:
        For each chunk read, test each character to determine if the 
        character is outside the ASCII printable range. If yes, True is
        returned immediately as the file is not plain-text. Otherwise, 
        if a file is read to the end, with all characters being within
        ASCII's printable range, False is returned as the file is 
        plain-text (ASCII).

    @param path Pointer to the full path of the file to be tested.
    @param sz Number of bytes to be read in a each chunk.
    @return Returns True if any of the characters in the file are outside
            ASCII's printable range. Otherwise, False.
*/
bool
isbinary_(const char *path, size_t sz) {

    char buf[sz];
    size_t i;
    size_t bytes;
    FILE *fp;

    if ( (fp = fopen(path, "rb")) == NULL ) {
        perror("Error opening file");
        return false;
    }
    while ( (bytes = fread(buf, 1, sz, fp)) ) {
        for ( i = 0; i < bytes; ++i ) {
            if ( !_inasciirange(buf[i]) ) {
                fclose(fp);
                return true;  // Quick escape for binary files.
            }    
        }
    }
    fclose(fp);
    return false;
}

/**
    Determine if a file is a ZIP archive.

    Notes:
        A file is tested to be a ZIP archive by checking the first four
        bytes of the file itself, *not* using the file extension.

        It is up to the caller to handle empty or spanned ZIP
        archives appropriately.
    
    @param path Pointer to the full path of the file to be tested.
    @return Returns True if the first four bytes of the file match any of
            the below. Otherwise, False.
    
            - ``\x50\x4b\x03\x04``: A 'standard' archive
            - ``\x50\x4b\x05\x06``: Empty archive
            - ``\x50\x4b\x07\x08``: Spanned archive
*/
bool
iszip_(const char *path) {

    size_t bytes;
    unsigned char buf[4];
    FILE *fp;

    if ( (fp = fopen(path, "rb")) == NULL ) {
        perror("Error opening file");
        return false;
    }
    if ( (bytes = fread(buf, 1, 4, fp)) != 4 ) {
        fprintf(stderr, "[ERROR]: Expecting a 4-byte read, got %ld\n", bytes);
        fclose(fp);
        return false;
    }
    fclose(fp);
    // Early escape if the first two bytes don't match.
    if ( !(buf[0] == 0x50 && buf[1] == 0x4b) ) return false;
    if ( !(   (buf[2] == 0x03 && buf[3] == 0x04)
           || (buf[2] == 0x05 && buf[3] == 0x06) 
           || (buf[2] == 0x07 && buf[3] == 0x08)) ) {
        return false;
    }
    return true;
}

/**
    Determine if a character is in the printable ASCII range.

    As a micro-optimisation (given short-circuiting), the 
    range [0x20, 0x7e] is evaluated *first*, followed by [0x07, 0x0d]
    and finally 0x1b.
    
    @param c Character to be tested.
    @return Returns True if the character is in the printable ASCII range,
            otherwise False.
*/
static bool
_inasciirange(char c) {

    if ( (0x20 <= c && c <= 0x7e) || (0x07 <= c && c <= 0x0d) || (c == 0x1b) ) 
        return true;
    return false;
}

