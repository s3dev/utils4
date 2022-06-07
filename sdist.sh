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

# Add line between deletion and setup runner.
printf "\n"

# Update requirements file.
printf "Updating the requirements file, ignoring './tests' ...\n"
pipreqs . --force --ignore tests

# Create the package and wheel file.
printf "\nCreating the source distribution ...\n"
sleep 1
python ./setup.py sdist

# Notfication.
printf "\nAll done.\n\n"

