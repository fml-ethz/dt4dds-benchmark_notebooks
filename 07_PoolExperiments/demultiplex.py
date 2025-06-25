import pathlib
import sys

INPUT_SAM = pathlib.Path(sys.argv[1])
OUTPUT_FOLDER = pathlib.Path(sys.argv[2])

# create output folder
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

OPEN_FILES = {}

with open(INPUT_SAM, "r") as f:
    for line in f:

        # parse line
        if line.startswith("@"):
            continue
        fields = line.strip().split("\t")
        ref_name = fields[2]
        read_sequence = fields[9]
        
        # remove numbers and last underscore from ref_name
        ref_name = ref_name.split("_")[:-1]
        ref_name = "_".join(ref_name)

        # open file if not already open
        if ref_name not in OPEN_FILES:
            OPEN_FILES[ref_name] = open(OUTPUT_FOLDER / f"{ref_name}.txt", "w")

        # write read sequence to file
        OPEN_FILES[ref_name].write(read_sequence + "\n")

# close all files
for f in OPEN_FILES.values():
    f.close()