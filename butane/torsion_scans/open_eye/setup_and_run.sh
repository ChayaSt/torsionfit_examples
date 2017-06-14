#!/usr/bin/env bash

DIH=($(ls -d */))
for D in ${DIH[*]}; do
    echo ${D}
    cd ${D}
    ANGLE=($(ls -d */))
    for A in ${ANGLE[*]}; do
        echo ${A}
        cd ${A}
        input=($(ls -d *.dat))
        echo ${input}
        output="${input//dat/out}"
        echo ${output}
        sed "s/REPLACE/ $input -o $output 2>&1/" ../../submit_dummy > submit
        qsub submit
        cd ../
    done
    cd ../
done
