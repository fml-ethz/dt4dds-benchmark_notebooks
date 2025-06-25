#!/bin/bash 
set -e
NAME_OF_DIR=$(basename $(pwd))

EXP_DIR="$SIMULATION_DIR"/"$NAME_OF_DIR"
NUM_COMMANDS=$(wc -l submit_arguments.txt | awk '{print $1}')

echo "Creating directory $EXP_DIR"
echo "Size of array: $NUM_COMMANDS"
mkdir -p "$EXP_DIR"

sbatch <<EOT
#!/bin/bash

#SBATCH -n 1
#SBATCH --time="$1":00:00
#SBATCH --mem-per-cpu="$2"
#SBATCH --tmp=2G
#SBATCH --array=1-"$NUM_COMMANDS"
#SBATCH --job-name="$NAME_OF_DIR"
#SBATCH --output="$EXP_DIR"/%a/slurm.out
#SBATCH --constraint=EPYC_7763

source ~/env.sh

awk -v jindex=\$SLURM_ARRAY_TASK_ID 'NR==jindex' submit_arguments.txt | xargs python "$3" "$EXP_DIR"/"\$SLURM_ARRAY_TASK_ID"
EOT