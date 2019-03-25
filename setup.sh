#!/usr/bin/env bash

dirs="./build ./dist ./utils3.egg-info"

# CHECK FOR EXISTING BUILD/DIST DIRS
echo ""
echo Checking for existing build directories ...
for d in ${dirs}; do
    # IF FOUND, DELETE IT
    if [ -d "${d}" ]; then
        echo Deleting "${d}"
        rm -rf "${d}"
    fi
done

# PACKAGE IT!
python ./setup.py sdist bdist_wheel

# NOTIFICATION
echo ""
echo All done.
echo ""
