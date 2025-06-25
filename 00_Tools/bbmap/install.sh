#!/bin/bash 
set -e

rm -rf code

wget https://sourceforge.net/projects/bbmap/files/BBMap_39.01.tar.gz/download
mkdir code
tar -zxvf download --strip-components=1 -C code
rm download