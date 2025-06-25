#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
all_codecs=(aeon_low aeon_medium aeon_high fountain_low fountain_medium fountain_high goldman_default rs_low rs_medium rs_high hedges_low hedges_medium yinyang_default)

# list with all workflow types
all_workflows=(best worst)

# list with all sequencing depths
sequencing_depths=(1 2.2 4.6 10 22 46 100 215 464 1000)

# list with all initial coverages
initial_coverages=(1 2.2 4.6 10 22 46 100 215 464 1000)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for workflow in "${all_workflows[@]}"
    do
        for seq_depth in "${sequencing_depths[@]}"
        do
            echo "$codec $workflow seqdepth $seq_depth"
        done
        for init_cov in "${initial_coverages[@]}"
        do
            echo "$codec $workflow initcov $init_cov"
        done
    done
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 144 8G run.py