#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all clustering types
all_clusterings=(basic clover mmseqs2 starcode cdhit lsh)

# create submit_arguments.txt with all possible combinations
for clustering in "${all_clusterings[@]}"
do
    echo "$clustering"
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 24 16G run.py