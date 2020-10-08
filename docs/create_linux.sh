#!/usr/bin/env bash

printf "\nRemoving current ./build directory ...\n"
rm -rf ./build

printf "\nCreating new docs ...\n"
sphinx-build ./source/ ./build/ -b html

