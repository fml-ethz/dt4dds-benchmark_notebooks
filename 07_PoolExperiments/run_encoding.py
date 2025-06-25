import dt4dds_benchmark
import pathlib
import yaml

from codec_definitions import POOL_CODECS

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# define folder for output
output_folder = pathlib.Path("./codec_data")
output_folder.mkdir(parents=True, exist_ok=False)


def encode(codec, input_file, output_folder):
    """ Run the codec on the input file and save the output to the output folder. """
    
    # create output folder
    output_folder = pathlib.Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=False)

    # encode the input file
    input_file = pathlib.Path(input_file)
    output_file = output_folder / f"encoded.txt"
    codec.encode(input_file, output_file)
    logger.info(f"Encoded {input_file} to {output_file} with codec {codec}.")

    # get encoding stats
    stats = dt4dds_benchmark.tools.encoding_stats(input_file, output_file)
    with open(output_folder / "encoding_stats.yaml", "w") as f:
        yaml.dump(stats, f, default_flow_style=False, sort_keys=False)


# go through all codecs and encode the input file
for codec_info in POOL_CODECS:
    encode(codec_info['codec'], codec_info['input'], output_folder / codec_info['name'])