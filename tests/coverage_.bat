@echo off

:: This file is called coverage_.bat as calling the coverage program
:: from a file called coverage.bat was problematic.

echo.
echo Running unit tests under coverage ...

coverage run -m unittest discover

echo.
echo Generating HTML report ...

coverage html

echo.
echo Done.
echo.

