=================
Release Checklist
=================

A checklist of things to remember for each release:

#. Ensure the version number has been updated.

#. Check code styling via pylintr.

#. Create a new branch and run all test cases.

#. Rebase all commits.

#. Create a new branch and update the docs, to capture the change log.

#. Commit and rebase again.

#. Create a source distribution on a new branch.

#. Commit and rebase again.

#. Add version tag to latest commit.

#. Push to the remote repo.

#. Copy the source distribution to NAS01 and RRDAPC50029 and create builds for:

    - Location 1: nas01/sharedfolders/Jez/S3D/Builds/  (storage / xfer)
    - Location 2: dev01/var/devmt/builds               (building)
    - Location 3: ltp02/var/devmt/builds               (building)
    - Location 4: rrdapc50029/c/devmt/builds

    - Linux x86_64
    - Linux armv7l
    - Windows x86_64

#. Run autobuild on:

    - 73DEVDEV01   (armhf builds)
    - 73DEVLTP02   (linux amd64 builds)
    - RRDAPC50029  (win amd64 builds)

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
    
