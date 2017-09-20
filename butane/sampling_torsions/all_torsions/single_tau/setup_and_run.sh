#!/usr/bin/env bash

# Parameters for toy model
RJ=False
DB=all
TAU=single

SAMPLES='10000000'

REPEATS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24)

#mkdir all_${SAMPLES}
#cd all_${SAMPLES}

for C in ${REPEATS[*]}; do
    mkdir ${DB}_${SAMPLES}_${C}
    cd ${DB}_${SAMPLES}_${C}
    DBNAME=${DB}_${SAMPLES}_${C}
    sed "s/REPLACE/-rj $RJ -d ${DBNAME}.sqlite -i $SAMPLES -t $TAU /" ../submit_dummy > submit
    qsub submit
    #python ../run_sampler.py -rj $RJ -d ${DBNAME}.sqlite -i $SAMPLES -t $TAU  > log.out
    cd ../
done
