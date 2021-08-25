#!/usr/bin/env bash

dirs="./build ./dist ./utils3.egg-info"

# Check for existing build/dist directories.
printf "\nChecking for existing build directories ...\n\n"
for d in ${dirs}; do
    # Delete the directory if it exists.
    if [ -d "${d}" ]; then
        printf "Deleting %s\n" ${d}
        rm -rf "${d}"
    fi
done

# Create the package and wheel file.
python ./setup.py sdist bdist_wheel

# Update requirements file.
printf "\nUpdating the requirements file ...\n"
pipreqs . --force

# Notfication.
printf "\nAll done.\n\n"
