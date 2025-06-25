# 🧬🏋 dt4dds-benchmark_notebooks


- [Overview](#overview)
- [Software Requirements](#software-requirements)
- [Installation Guide](#installation-guide)
- [License](#license)


# Overview
This repository contains the data analysis, in the form of Jupyter Notebooks and data files, for the analyses and figures in the following publication:

> Gimpel, A.L., Remschak, A., Stark, W.J., Heckel, R., Grass R.N. manuscript in preparation

The Python package `dt4dds-benchmark`, providing a comprehensive benchmarking suite for codecs and clustering algorithms in the field of DNA data storage, is found in the [dt4dds-benchmark repository](https://github.com/fml-ethz/dt4dds-benchmark).

The subdirectories contain the following analyses:
- 01_ClusterOptimization: parameter optimization of the individual clustering algorithms based on experimental sequencing data from the literature
- 02_ClusterMatching: screening of all clustering algorithms with each codec in a synthetic error benchmark to assess fit
- 03_IndividualErrors: benchmarking codecs against individual error types
- 04_CoverageVsErrors: extension of the benchmark with sequence dropout
- 05_LiteratureExperiments: re-implementation of common literature benchmark experiments in silico and assessment of codec performance
- 06_PhysicalVsSeqdepth: benchmarking of codecs in two realistic error scenarios, varying physical redundancy and sequencing depth
- 07_PoolExperiments: experimental validation of results with both a high- and a low-fidelity scenario



# Software requirements
The package has been developed and tested on Ubuntu 20.04 using Python 3.10. The Python packages listed in [requirements.txt](/requirements.txt) are required.

In addition, bbmap (v39.01), NGmerge (v0.3), and seqtk (v1.4) are required, if post-processing of raw data is to be performed. For this, see the installation guide. Note that these tools have other dependencies, such as a Java Runtime and gcc.


# Installation guide
To install this package from Github, use
```bash
git clone https://github.com/fml-ethz/dt4dds-benchmark_notebooks
cd dt4dds-benchmark_notebooks
```

If intermediary files are to be re-generated from the raw sequencing data, bbmap, NGmerge and seqtk are required as well. To install these tools, run the `install.sh` scripts located in the subdirectories of [00_Tools/](/00_Tools/).


# License
This project is licensed under the GPLv3 license, see [here](LICENSE).