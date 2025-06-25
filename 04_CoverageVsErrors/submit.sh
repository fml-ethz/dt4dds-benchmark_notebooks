#!/bin/bash 
set -e
cd "$(dirname "$0")"

# list with all codec types
all_codecs=(aeon_high aeon_medium aeon_low fountain_high fountain_medium fountain_low rs_high rs_medium rs_low hedges_medium hedges_low goldman_default yinyang_default)

# list with all error rates
error_rates=(0.001 0.002 0.004 0.008 0.016 0.032 0.064 0.128 0.25 0.5)

# list with all dropout rates
dropout_rates=(0.001 0.0021 0.0045 0.0096 0.021 0.044 0.093 0.20 0.42 0.9)

# create submit_arguments.txt with all possible combinations
for codec in "${all_codecs[@]}"
do
    for error_rate in "${error_rates[@]}"
    do
        echo "$codec "rate" $error_rate"
    done
    for dropout_rate in "${dropout_rates[@]}"
    do
        echo "$codec "dropout" $dropout_rate"
    done
done > submit_arguments.txt

# submit array
../00_Tools/slurm/submit_array.sh 144 8G run.py