#!/bin/bash 
set -e
cd "$(dirname "$0")"

# create data directory
mkdir seq_data
cd seq_data

# create function for sampling
handle () {
    # download files
    wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR120/"$1"/R1.fq.gz
    wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR120/"$1"/R2.fq.gz

    # merge paired reads
    ../../00_Tools/ngmerge/run.sh R1.fq.gz R2.fq.gz merged.fq.gz

    # sub-sample
    ../../00_Tools/seqtk/code/seqtk sample -s1 merged.fq.gz $((20 * $2)) > merged_20x.fq

    # convert fastq files to txt files
    awk 'NR%4==2' merged_20x.fq > merged_20x.txt

    # move and remove files
    mv merged_20x.txt "$3"_20x.txt
    rm -f R1.fq.gz
    rm -f R2.fq.gz
    rm -f merged.fq.gz
    rm -f merged_20x.fq
}

# experimental electrochemical synthesis example
handle ERR12033820 12402 exp_electrochemical

# experimental material deposition synthesis example
handle ERR12033821 12000 exp_material


# download reference sequences
wget https://raw.githubusercontent.com/fml-ethz/dt4dds_notebooks/master/data/Aging/7d_Genscript_GCfix/design_files.fasta
mv design_files.fasta reference_electrochemical.fasta
wget https://raw.githubusercontent.com/fml-ethz/dt4dds_notebooks/master/data/Aging/7d_Twist_GCall/design_files.fasta
mv design_files.fasta reference_material.fasta