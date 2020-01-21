#!/usr/bin/env bash
#-----------------------------------------------------------------------
# Prog:     pylintr.sh
# Version:  0.1.1
# Desc:     This script walks down a project tree searching for all
#           *.py files and runs pylint over each file, using the default
#           pylint config file and stores the report to the defined
#           ${OUTPUT} location.
#
#           Once complete, the score from each report is written to a
#           summary file, which is printed at the end of the script.
#
# Platform: Linux / Windows*
#           *The script has been designed to run on both Linux and
#           Windows, providing Windows has git bash, cygwin, or the
#           like installed.
#
# Deploymt: This script (and its parent directory) should be placed at
#           the top level of a project.
#
# UPDATES:
# 11.01.19  J. Berendt  0.1.0  Written.
# 14.01.19  J. Berendt  0.1.1  Updated regex for accuracy.
#                              Moved script and output into same dir.
#                              Added date run to summary.
# 17.01.19  J. Berendt  0.1.2  Converted line endings to Unix format.
#-----------------------------------------------------------------------

EXT=".plr"
OUTPUT="./results"
SUMMARY="${OUTPUT}/summary${EXT}"

# TEST FOR OUTPUT DIRECTORY
if [ ! -d ${OUTPUT} ]; then
    echo
    echo Creating output directory ...
    mkdir ${OUTPUT}
else
    echo
    echo Removing current results ...
    rm ${OUTPUT}/*${EXT}
fi

# RUN PYLINT OVER ALL *.PY FILES
for f in $( /usr/bin/find ../ -name "*.py" ); do
    base=$( basename ${f} )
    if [[ ${base} =~ ^[a-z]+\.py ]]; then
        echo Processing: ${f}
        outname=$( echo ${base} | sed s/.py// )${EXT}
        pylint ${f} > "${OUTPUT}/${outname}"
    fi
done

echo Done.
echo

# READ EACH REPORT AND POPULATE RESULTS TO SUMMARY
echo Pylint Summary: > ${SUMMARY}
echo ------------------------ >> ${SUMMARY}
for f in ${OUTPUT}/*; do
    if [ ${f} != ${SUMMARY} ]; then
	score=$( cat ${f} | grep -Eo "^Your.*at\s([0-9]+\.[0-9]+\/[0-9]+)" | awk '{ print $NF }' )
        echo $( basename ${f} ): ${score} >> ${SUMMARY}
    fi
done
echo ------------------------ >> ${SUMMARY}
echo
echo Run date: $( date ) >> ${SUMMARY}

# PRINT SUMMARY
cat ${SUMMARY}
echo
