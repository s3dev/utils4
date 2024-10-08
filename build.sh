#!/usr/bin/env bash

dirs="./build ./dist ./utils4.egg-info"

# Check for existing build/dist directories.
printf "\nChecking for existing build directories ...\n\n"
for d in ${dirs}; do
    # Delete the directory if it exists.
    if [ -d "${d}" ]; then
        printf "|- Deleting %s\n" ${d}
        rm -rf "${d}"
    fi
done

# Update requirements file.
printf "Updating the requirements file, ignoring './tests' ...\n"
preqs . --replace --ignore_dirs tests

# Create the package and wheel file.
printf "\nCreating the source distribution ...\n"
python -m build --sdist

# Notfication.
printf "\nAll done.\n\n"

