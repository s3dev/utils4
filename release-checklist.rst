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

#. Copy the source distribution to 73DEVNAS01 and 73DEVVMW01 and create builds for:

    - Location 1: nas01/sharedfolders/Jez/S3D/Builds/  (storage / xfer)
    - Location 2: dev02/var/devmt/builds               (Linux ARM builds)
    - Location 3: adm02/var/devmt/builds               (Linux aarch64 builds)
    - Location 4: ltp03/var/devmt/builds               (Linux x86_64 builds)
    - Location 5: vmw01/c/devmt/builds                 (Windows 10 builds)

    - Linux x86_64
    - Linux armv7l
    - Linux aarch64
    - Windows x86_64

#. Run autobuild on:

    - 73DEVDEV02   (armhf builds)
    - 73DEVADM02   (aarch64 builds)
    - 73DEVLTP03   (linux amd64 builds)
    - 73DEVVMW01   (win amd64 builds)

#. Done
    
