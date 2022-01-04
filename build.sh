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

# Create the package and wheel file.
printf "Creating the source distribution and wheel file ...\n"
sleep 1
python ./setup.py sdist bdist_wheel

# Update requirements file.
printf "\nUpdating the requirements file ...\n"
pipreqs . --force

# Notfication.
printf "\nAll done.\n\n"

