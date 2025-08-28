#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
all_codecs=(modulation_medium ldpc_medium dbgps_low dbgps_medium dbgps_high)

# list with all workflow types
all_workflows=(substitution deletion insertion dropout)

# list with clusterings
all_clusterings=(basic default)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for workflow in "${all_workflows[@]}"
    do
        for clustering in "${all_clusterings[@]}"
        do
            echo "$codec" "$workflow" "$clustering"
        done
    done
done > submit_arguments.txt

# submit array
../../00_Tools/slurm/submit_array.sh 144 8G run.py