=================
Release Checklist
=================

A checklist of things to remember for each release:

#. Ensure the version number has been updated.

#. Check code styling via pylintr.

#. Create a new branch and run all test cases.

    - Python 3.7
    - Python 3.12

#. Rebase all commits.

#. Create a new branch and update the docs, to capture the change log.

#. Commit and rebase again.

#. Create a source distribution on a new branch.

#. Commit and rebase again.

#. Add version tag to latest commit.

#. Push to the remote repo.

#. Upload to PyPI (test).

#. Upload to PyPI.

#. Copy the source distribution to NAS01 and RRDAPC50029 and create builds for:

    - Location 1: nas01/sharedfolders/Jez/S3D/Builds/  (storage / xfer)
    - Location 2: dev02/var/devmt/builds               (Linux ARM builds)
    - Location 3: ltp02/var/devmt/builds               (Linux x86_64 builds)
    - Location 4: rrdapc50029/c/devmt/builds           (Windows builds)

    - Linux x86_64
    - Linux armv7l
    - Windows x86_64

#. Run autobuild on:

    - 73DEVDEV02   (armhf builds)
    - 73DEVLTP02   (linux amd64 builds)
    - RRDAPC50029  (win amd64 builds)

#. Done
    
