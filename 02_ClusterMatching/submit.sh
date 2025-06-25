#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
all_codecs=(aeon_low aeon_medium aeon_high fountain_low fountain_medium fountain_high goldman_default rs_low rs_medium rs_high hedges_low hedges_medium yinyang_default)

# list with clusterings
all_clusterings=(basic cdhit mmseqs2 starcode clover lsh)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for clustering in "${all_clusterings[@]}"
    do
        echo "$codec" "$clustering"
    done
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 144 8G run.py