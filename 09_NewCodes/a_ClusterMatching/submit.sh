#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
all_codecs=(modulation_medium ldpc_medium dbgps_low dbgps_medium dbgps_high)

# list with clusterings
all_clusterings=(basic cdhit starcode clover lsh)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for clustering in "${all_clusterings[@]}"
    do
        echo "$codec" "$clustering"
    done
done > submit_arguments.txt

# submit array
../../00_Tools/slurm/submit_array.sh 144 8G run.py