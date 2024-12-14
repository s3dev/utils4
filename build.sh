#!/usr/bin/env bash

declare -a delme=(
                  "./build" 
                  "./dist" 
                  "./utils4.egg-info"
                  "requirements.txt"
                  "setup.cfg"
                 )

# Check for existing build/dist directories.
printf "\nChecking for existing build directories ...\n\n"
#for d in ${dirs}; do
for f in ${delme[@]}; do
    # Delete the directory if it exists.
    if [ -d "${f}" ] || [ -f "${f}" ]; then
        printf "|- Deleting %s\n" ${f}
        rm -rf "${f}"
    fi
done

# Update requirements file.
printf "\nUpdating the requirements file, ignoring './tests' ...\n"
preqs . --replace --ignore_dirs tests

# Create the package and wheel file.
printf "Creating the source distribution ...\n"
python -m build --sdist

# Notfication.
printf "\nAll done.\n\n"

