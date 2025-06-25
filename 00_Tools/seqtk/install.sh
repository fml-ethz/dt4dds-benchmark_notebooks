#!/bin/bash 
set -e

rm -rf code

wget https://github.com/lh3/seqtk/archive/refs/tags/v1.4.tar.gz
mkdir code
tar -zxvf v1.4.tar.gz --strip-components=1 -C code
rm v1.4.tar.gz

cd code
make