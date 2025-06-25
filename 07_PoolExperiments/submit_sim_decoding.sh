#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all scenarios
all_scenarios=(bestcase worstcase)

# list with all codec types
all_codecs=(aeon_max aeon_medium aeon_high fountain_max fountain_medium fountain_high goldman rs_max rs_medium rs_high hedges yinyang)

# list with all clustering types
all_clusterings=(basic default)

# create submit_arguments.txt with all possible combinations
for scenario in "${all_scenarios[@]}"
do 
    for codec in "${all_codecs[@]}"
    do 
        for clustering in "${all_clusterings[@]}"
        do 
            echo "$scenario $codec $clustering"
        done
    done
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 144 8G run_sim_decoding.py