=================
Release Checklist
=================

A checklist of things to remember for each release:

#. Ensure the version number has been updated.

#. Check code styling via pylintr.

#. Create a new branch and run all test cases.

#. Create a source distribution.

#. Rebase all commits.

#. Create a new branch and update the docs, to capture the change log.

#. Commit and rebase again.

#. Add version tag to latest commit.

#. Push to the remote repo.

#. Copy the source distribution to NAS01 and create builds for:

    - Location: nas01/sharedfolders/Jez/S3D/Builds/

    - Linux x86_64
    - Linux armv7l
    - Windows x86_64

#. Copy the following files to the S3D archive:

    - Source dist (tar.gz):
        - latest / version numbered
    - Linux x86_64 wheels:
        - latest / version numbered
    - Linux armv7l:
        - latest / version numbered
    - Windows x86_64:
        - latest / version numbered

#. Done
    
