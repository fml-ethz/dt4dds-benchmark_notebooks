#!/bin/bash 
set -e
cd "$(dirname "$0")"

# downloading & merging paired reads
download_filter_and_merge () {
    # download files
    mkdir -p ./exp_data/"$3"/"$2"
    wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR151/"$1"/"$3"_"$2"_R1_original.fq.gz -O ./exp_data/"$3"/"$2"/R1.fq.gz
    wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR151/"$1"/"$3"_"$2"_R2_original.fq.gz -O ./exp_data/"$3"/"$2"/R2.fq.gz

    # set up directories
    echo ""
    echo filtering + merging "$2"
    echo "##########################"
    cp ./exp_data/"$3"/"$2"/R1.fq.gz ./exp_data/"$3"/"$2"/R1_original.fq.gz
    cp ./exp_data/"$3"/"$2"/R2.fq.gz ./exp_data/"$3"/"$2"/R2_original.fq.gz

    # filter reads to remove adapters and low quality reads
    ../00_Tools/bbmap/code/bbduk.sh in1=./exp_data/"$3"/"$2"/R1.fq.gz in2=./exp_data/"$3"/"$2"/R2.fq.gz out1=./exp_data/"$3"/"$2"/R1_filtered.fq.gz out2=./exp_data/"$3"/"$2"/R2_filtered.fq.gz ref=../00_Tools/bbmap/code/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo maq=10 minlen=100
    mv ./exp_data/"$3"/"$2"/R1_filtered.fq.gz ./exp_data/"$3"/"$2"/R1.fq.gz
    mv ./exp_data/"$3"/"$2"/R2_filtered.fq.gz ./exp_data/"$3"/"$2"/R2.fq.gz

    # merge reads
    ../00_Tools/ngmerge/run.sh ./exp_data/"$3"/"$2"/R1.fq.gz ./exp_data/"$3"/"$2"/R2.fq.gz ./exp_data/"$3"/"$2"/merged.fq.gz
    rm -f ./exp_data/"$3"/"$2"/R1.fq.gz
    rm -f ./exp_data/"$3"/"$2"/R2.fq.gz
}

download_filter_and_merge ERR15127735 Cov2 bestcase
download_filter_and_merge ERR15127736 Cov5 bestcase
download_filter_and_merge ERR15127737 Cov10 bestcase
download_filter_and_merge ERR15127738 Cov25 bestcase
download_filter_and_merge ERR15127739 Cov1000 bestcase
download_filter_and_merge ERR15127740 Cov5 worstcase
download_filter_and_merge ERR15127741 Cov10 worstcase
download_filter_and_merge ERR15127742 Cov25 worstcase
download_filter_and_merge ERR15127743 Cov50 worstcase
download_filter_and_merge ERR15127744 Cov1000 worstcase


# demultiplexing by mapping to reference sequences
demultiplex () {
    # map with bbmap
    echo ""
    echo mapping "$1" "$2"
    echo "##########################"
    cp ./final/combined/padded_indexed.fasta ./exp_data/"$2"/"$1"/design_files.fasta
    ../00_Tools/bbmap/code/bbmap.sh -Xmx4G -Xms4G in=./exp_data/"$2"/"$1"/merged.fq.gz ref=./exp_data/"$2"/"$1"/design_files.fasta nodisk outm=./exp_data/"$2"/"$1"/mapped.sam outu=./exp_data/"$2"/"$1"/unmapped.fq.gz vslow k=8 maxindel=200 minratio=0.1 scafstats=./exp_data/"$2"/"$1"/scafstats.txt

    # demultiplex based on mapping
    mkdir -p ./exp_data/"$2"/"$1"/demultiplexed
    python demultiplex.py ./exp_data/"$2"/"$1"/mapped.sam ./exp_data/"$2"/"$1"/demultiplexed
}

cp ./final/combined/padded_indexed.fasta ./exp_data/bestcase/design_files.fasta
cp ./final/combined/padded_indexed.fasta ./exp_data/worstcase/design_files.fasta
demultiplex Cov2 bestcase
demultiplex Cov5 bestcase
demultiplex Cov10 bestcase
demultiplex Cov25 bestcase
demultiplex Cov1000 bestcase
demultiplex Cov5 worstcase
demultiplex Cov10 worstcase
demultiplex Cov25 worstcase
demultiplex Cov50 worstcase
demultiplex Cov1000 worstcase


downsample() {
    echo ""
    echo downsampling "$1"-"$2"-"$3"
    echo "##########################"
    num_seqs=$(wc -l < ./final/"$2".txt)
    num_reads=$(($num_seqs * $4))
    num_lines=$(wc -l < ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt)

    # check that num_reads is not greater than the number of lines in the file
    if [ $num_reads -gt $num_lines ]; then
        echo "Error: num_reads is greater than the number of lines in the file"
        exit 1
    fi

    # perform ten iterations of downsampling
    for j in {0..9}; do
        echo iteration $j
        shuf ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt > ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt.shuffled
        head -n $num_reads ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt.shuffled > ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt.downsampled."$j"
        rm -f ./exp_data/"$3"/"$1"/demultiplexed/"$2".txt.shuffled
    done
}

# bestcase
for i in {2,5,10,25,1000}; do
    downsample Cov"$i" aeon_max bestcase 30
    downsample Cov"$i" aeon_high bestcase 30
    downsample Cov"$i" aeon_medium bestcase 30
    downsample Cov"$i" fountain_max bestcase 30
    downsample Cov"$i" fountain_high bestcase 30
    downsample Cov"$i" fountain_medium bestcase 30
    downsample Cov"$i" rs_max bestcase 30
    downsample Cov"$i" rs_high bestcase 30
    downsample Cov"$i" rs_medium bestcase 30
    downsample Cov"$i" goldman bestcase 30
    downsample Cov"$i" hedges bestcase 30
    downsample Cov"$i" yinyang bestcase 30
done

# worstcase
for i in {5,10,25,50,1000}; do
    downsample Cov"$i" aeon_max worstcase 30
    downsample Cov"$i" aeon_high worstcase 30
    downsample Cov"$i" aeon_medium worstcase 30
    downsample Cov"$i" fountain_max worstcase 30
    downsample Cov"$i" fountain_high worstcase 30
    downsample Cov"$i" fountain_medium worstcase 30
    downsample Cov"$i" rs_max worstcase 30
    downsample Cov"$i" rs_high worstcase 30
    downsample Cov"$i" rs_medium worstcase 30
    downsample Cov"$i" goldman worstcase 30
    downsample Cov"$i" hedges worstcase 30
    downsample Cov"$i" yinyang worstcase 30
done



# perform complete error analysis for Cov1000
for i in {bestcase,worstcase}; do
    mkdir -p ./exp_data/"$i"/Cov1000/full_analysis
    mkdir -p ./exp_data/"$i"/Cov1000/full_analysis/all
    cp ./final/combined/padded_indexed.fasta ./exp_data/"$i"/Cov1000/full_analysis/all/design_files.fasta
    rm ./exp_data/"$i"/Cov1000/full_analysis/all/R1.fq.gz
    rm -rf ./exp_data/"$i"/Cov1000/full_analysis/all/analysis
    rm ./exp_data/"$i"/Cov1000/full_analysis/all/mapped.bam
    ln -s ../../merged.fq.gz ./exp_data/"$i"/Cov1000/full_analysis/all/R1.fq.gz
    dt4dds-clusteranalysis -c standard ./exp_data/"$i"/Cov1000/full_analysis/all/
done



erroranalysis() {
    echo ""
    echo analyzing "$1" "$2"
    echo "##########################"
    # ensure clean directory
    mkdir -p ./exp_data/"$2"/Cov1000/full_analysis/"$1"
    rm -f ./exp_data/"$2"/Cov1000/full_analysis/"$1"/R1.fq.gz
    rm -rf ./exp_data/"$2"/Cov1000/full_analysis/"$1"/analysis
    rm -f ./exp_data/"$2"/Cov1000/full_analysis/"$1"/mapped.bam
    ln -s ../../merged.fq.gz ./exp_data/"$2"/Cov1000/full_analysis/"$1"/R1.fq.gz

    # copy design files and run analysis
    grep -A 1 "^>$1" ./final/combined/padded_indexed.fasta > ./exp_data/"$2"/Cov1000/full_analysis/"$1"/design_files.fasta
    dt4dds-clusteranalysis -c standard ./exp_data/"$2"/Cov1000/full_analysis/"$1"/
}

for i in {bestcase,worstcase}; do
    erroranalysis aeon_max "$i"
    erroranalysis aeon_high "$i"
    erroranalysis aeon_medium "$i"
    erroranalysis fountain_max "$i"
    erroranalysis fountain_high "$i"
    erroranalysis fountain_medium "$i"
    erroranalysis rs_max "$i"
    erroranalysis rs_high "$i"
    erroranalysis rs_medium "$i"
    erroranalysis goldman "$i"
    erroranalysis hedges "$i"
    erroranalysis yinyang "$i"
done