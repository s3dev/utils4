/**
    Header file for the _futils.c module.
*/

#ifndef _FUTILS_H

#include <stdbool.h>

/**
    Determine if a file is plain-text (ASCII only).

    A file is deemed non-binary if *all* of the characters in the file
    are within ASCII's printable range.

    Design:
        This function simply inverts the return value of the isbinary 
        function. For design detail, refer to the isbinary documentation.
    
    @param path Pointer to the full path of the file to be tested.
    @return Returns True if *all* characters are within ASCII's printable
            range. Otherwise, False.
*/
bool
isascii_(const char *path, size_t sz);

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
isbinary_(const char *path, size_t sz);

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
iszip_(const char *path);

#endif /* _FUTILS_H */

