#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
# all_codecs=(aeon_medium aeon_high aeon-motif_high rs_medium rs_high)
all_codecs=(aeon_medium rs_medium)

# list with error types
all_errortypes=(errors dropout)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for errortype in "${all_errortypes[@]}"
    do
        echo "$codec" "$errortype"
    done
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 144 8G run.py