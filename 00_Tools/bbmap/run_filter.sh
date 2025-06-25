#!/bin/bash 
set -e
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

"$BASE_PATH"/code/bbmap.sh -1 "$1".unmerged -2 "$2".unmerged -o "$1" -d -e 20 -z -v


exit