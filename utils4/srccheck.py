#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module is used to perform checksum calculations on a
            collection of files to verify if the checksum *calculated* on each
            file matches the *expected* checksum value.

            In practical terms, an application can call the
            :meth:`~SourceCheck.check` method by passing a list of filepaths
            to be checksummed, along with a reference file (containing the
            expected checksums). If the checksum values match the reference
            file, a value of ``True`` is returned to the caller application,
            signaling the inspected source code files have *not* been modified
            and are 'safe' for use. Otherwise, a value of ``False`` is
            returned to the caller the filenames of each failing file are
            printed to the terminal.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example usage:

    Generate an *un-encrypted* reference file::

        >>> from utils4.srccheck import srccheck

        >>> files = ['list.c', 'of.py', 'files.sql']
        >>> srccheck.generate(filepaths=files, encrypt=False)


    Verify checksums from within an application, with an *un-encrypted*
    reference file::

        >>> from utils4.srccheck import srccheck

        >>> srccheck.check(ref_file='path/to/srccheck.ref')
        True

    Generate an **encrypted** reference file::

        >>> from utils4.srccheck import srccheck

        >>> files = ['list.c', 'of.py', 'files.sql']
        >>> srccheck.generate(filepaths=files, encrypt=True)


    Verify checksums from within an application, with an *encrypted* reference
    file::

        >>> from utils4.srccheck import srccheck

        >>> srccheck.check(ref_file='path/to/srccheck.ref',
                           key_file='path/to/srccheck.key')
        True


    **Advanced usage:**

    If you wish to *delay the output* of mismatched files (to give the caller
    application display control), the caller can redirected the output from
    the :meth:`~SourceCheck.check` method into a buffer and display at a more
    appropriate time. For example::

        >>> from contextlib import redirect_stdout
        >>> from io import StringIO
        >>> from utils4.srccheck import srccheck

        >>> buff = StringIO()
        >>> with redirect_stdout(buff):
        >>>     test = srccheck.check(ref_file='path/to/srccheck.ref')

        >>> # ...

        >>> if not test:
        >>>     print(buff.getvalue())
        >>> buff.close()

        Checksum verification has failed for the following:
        - 02-01_first.c
        - 10-09_ptr_exchange.c
        - 06-ex07.c
        - 15-ex05_col_output.c
        - 02-03_multi_lines.c

"""
# pylint: disable=wrong-import-order

import json
import os
import pickle
import sys
import uuid
from cryptography import fernet
from typing import List
from utils4.crypto import crypto


class SourceCheck:
    """Verify source code checksums values are as expected."""

    def check(self, ref_file: str, key_file: str='') -> bool:
        """Verify the provided source code file checksums are as expected.

        If any checksum do not match, the names of those files are reported
        to the terminal.

        Args:
            ref_file (str): Full path to the reference file containing the
                full paths to the file(s) to be tested and the associated
                checksum value(s).
            key_file (str, optional): Full path to the key file. If a key file
                is not provided, the method assumes the reference file is in
                plaintext CSV and does not attempt to decrypt.
                Defaults to ''.

        Note:
            If the ``key_file`` argument is *not* provided, it is assumed the
            ``ref_file`` is a plaintext CSV file, and decryption is *not*
            attempted.

            If the ``key_file`` argument *is* provided, it is assumed the
            ``ref_file`` has been encrypted, and decryption is carried out.

        Raises:
            FileNotFoundError: If either the reference file, or key file do
                not exist.

        Returns:
            bool: True if all file's checksum values agree with the checksum
            listed in the reference file; otherwise False.

        """
        # pylint: disable=no-else-return
        if not os.path.exists(ref_file):
            raise FileNotFoundError(f'Reference file not found: {ref_file}')
        if all([key_file, not os.path.exists(key_file)]):
            raise FileNotFoundError(f'Key file not found: {key_file}')
        if key_file:
            # Decrypt reference file.
            with open(ref_file, 'rb') as rfp:
                data = pickle.load(rfp)
            with open(key_file, 'rb') as kfp:
                f = fernet.Fernet(kfp.read())
            ref = json.loads(f.decrypt(data).decode())
        else:
            # Read plaintext reference file.
            ref = {}
            with open(ref_file, 'r', encoding='utf-8') as rfp:
                for line in rfp:
                    ref.update([line.strip().split(',')])
        chksums = self._checksum(files=ref.keys())
        # Object check for quick validation.
        if chksums == ref:
            return True
        else:
            self._report_mismatches(checksums=chksums, reference=ref)
            return False

    def generate(self, filepaths: List[str], encrypt: bool=False):
        """Generate the reference file containing the source file checksums,
        and the associated key file.

        Args:
            filepaths (list[str]): A list of full paths which are to be
                included in the reference file.
            encrypt (bool, optional): Encrypt the reference file and generate
                a key file. Defaults to False.

        :Reference File:

            **If unencrypted:**

            The reference file is a flat, plaintext CSV file with the file
            path as the first field and the checksum value as the second field.

            For example::

                filepath_01,md5_hash_string_01
                filepath_02,md5_hash_string_02
                filepath_03,md5_hash_string_03
                ...
                filepath_NN,md5_hash_string_NN

            **If encrypted:**

            The reference file contains is a serialised, encrypted
            representation of the full path and associated checksum value for
            all provided files, in JSON format. This data is written to the
            ``srccheck.ref`` file.

            A unique encryption key is created and stored with *each* call to
            this method, and stored to the ``srccheck.key`` file.

            To perform checks, both the reference file *and* the key file must
            be provided to the :meth:`~check` method.

            .. note:: These files are a **pair**. If one file is lost, the
                      other file is useless.

        :Layout:

            **If encrypted:**

            The layout of the *deserialised* and *decrypted* reference file is
            in basic JSON format, with the filename as the keys, and checksum
            values as the values.

            For example::

                {"filepath_01": "md5_hash_string_01",
                 "filepath_02": "md5_hash_string_02",
                 "filepath_03": "md5_hash_string_03",
                 ...,
                 "filepath_NN": "md5_hash_string_NN"}

        Raises:
            FileNotFoundError: If any of the files provided to the
                ``filepaths`` argument do not exist.

        """
        if not self._all_files_exist(files=filepaths):
            raise FileNotFoundError('The files listed above were not found.')
        op_ref, op_key = self._build_outpaths()
        chksums = self._checksum(files=filepaths)
        if encrypt:
            key = crypto.b64(uuid.uuid4().hex, decode=False)
            with open(op_key, 'wb') as kfp:
                kfp.write(key)
            f = fernet.Fernet(key=key)
            with open(op_ref, 'wb') as rfp:
                pickle.dump(f.encrypt(json.dumps(chksums).encode()), rfp)
            print('\nComplete.\nThe reference and key files are available on your desktop.')
        else:
            with open(op_ref, 'w', encoding='utf-8') as rfp:
                for k, v in chksums.items():
                    rfp.write(f'{k},{v}\n')
            print('\nComplete.\nThe reference file is available on your desktop.')

    @staticmethod
    def _all_files_exist(files: list) -> bool:
        """Verify all provided files exist.

        If any file does not exist, the user is alerted via the terminal and a
        ``FileNotFoundError`` exception is raised by the caller.

        Args:
            files (list): List of files to be tested.

        Returns:
            bool: True, if all files exist, otherwise False.

        """
        # pylint: disable=consider-using-f-string
        success = True
        nexist = []
        for f in files:
            if not os.path.exists(f):
                nexist.append(f)
                success = False
        if nexist:
            print('\nThe following files do not exist:')
            print(*map(' - {}'.format, nexist), sep='\n')
            print('')
        return success

    @staticmethod
    def _build_outpaths() -> tuple:
        """Build the output path to the reference and key files.

        Returns:
            tuple: Full path to the reference and key files as::

                ('fname.ref', 'fname.key')

        """
        _os = sys.platform.lower()
        fn_ref = 'srccheck.ref'
        fn_key = 'srccheck.key'
        if 'win' in _os:  # pragma nocover
            desk = os.path.join(os.environ.get('USERPROFILE'), 'Desktop')
        elif 'lin' in _os:
            desk = os.path.join(os.environ.get('HOME'), 'Desktop')
        else:  # pragma nocover
            raise NotImplementedError(f'Not a currently supported OS: {_os}')
        return os.path.join(desk, fn_ref), os.path.join(desk, fn_key)

    @staticmethod
    def _checksum(files: list) -> dict:
        """Calculate checksum for all passed files.

        Args:
            files (list): List of full paths against which a checksum is to be
                calculated.

        Returns:
            dict: A dictionary containing the filename and checksum for all
            passed files, as::

                {'fname_01': 'checksum_hash_01',
                 'fname_02': 'checksum_hash_02',
                 'fname_03': 'checksum_hash_03',
                 ...,
                 'fname_NN': 'checksum_hash_NN'}

        """
        return {f: crypto.checksum_md5(path=f) for f in files}

    @staticmethod
    def _report_mismatches(checksums: dict, reference: dict):
        """Report the files for which the checksums do not match.

        Args:
            checksums (dict): A dictionary containing the recently calculated
                checksums.
            reference (dict): A dictionary containing the *expected* checksums.

        """
        # pylint: disable=consider-using-f-string
        m = []
        for k, v in reference.items():
            if checksums.get(k) != v:
                m.append(os.path.basename(k))
        print('\nChecksum verification has failed for the following:')
        print(*map('- {}'.format, m), sep='\n')
        print('')


srccheck = SourceCheck()
