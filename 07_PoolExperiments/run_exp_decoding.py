import dt4dds_benchmark
import pathlib
import sys

from codec_definitions import POOL_CODECS

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# input arguments
OUTPUT_DIR = pathlib.Path(sys.argv[1]).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SCENARIO = sys.argv[2]
CODEC = sys.argv[3]

# select the coverages to use based on the dataset
COVERAGES = ['Cov2', 'Cov5', 'Cov10', 'Cov25', 'Cov1000'] if SCENARIO == 'bestcase' else ['Cov5', 'Cov10', 'Cov25', 'Cov50', 'Cov1000']


# define folder for codec input files
codec_folder = pathlib.Path("./codec_data")
if not codec_folder.exists():
    raise FileNotFoundError(f"Folder {codec_folder} must already exist with the input files.")

design_folder = pathlib.Path("./final")
if not design_folder.exists():
    raise FileNotFoundError(f"Folder {design_folder} must already exist with the design files.")

exp_folder = pathlib.Path(f"./exp_data/{SCENARIO}")
if not exp_folder.exists():
    raise FileNotFoundError(f"Folder {exp_folder} must already exist with the experimental data.")

main_folder = pathlib.Path(f"./decoding_data/{SCENARIO}")
main_folder.mkdir(parents=True, exist_ok=True)

# define the clusterings to use
codec2clustering = {
    'fountain_medium': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
    'goldman': dt4dds_benchmark.clustering.LSH('default'),
}

# define the codec and inputs
codecs_dict = {c['name']: c for c in POOL_CODECS}
if CODEC not in codecs_dict:
    raise ValueError(f"Codec {CODEC} not found.")
codec_info = codecs_dict[CODEC]

# attempt to decode the experimental sequencing data with both clusterings and all coverage levels, in 5 iterations each
pipelines = []
clusterings = [dt4dds_benchmark.clustering.BasicSet.default(), codec2clustering.get(codec_info['name'], dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6))]
for clustering in clusterings:
    for cov in COVERAGES:
        for iter in range(0, 9+1):
            # define files and folders
            design_file = exp_folder / cov / 'demultiplexed' / f"{codec_info['name']}.txt.downsampled.{iter}"
            data_folder = codec_folder / codec_info['name']

            # create the pipeline for each codec
            pipeline = dt4dds_benchmark.pipelines.Decoding(
                read_file = design_file, 
                clustering = clustering,
                codec = codec_info['codec'], 
                codec_folder = data_folder,
                input_file = codec_info['input'],
                metadata = {'coverage': cov, 'iteration': iter, 'scenario': SCENARIO},
            )
            pipelines.append(pipeline)

manager = dt4dds_benchmark.pipelines.HDF5Manager(str(main_folder / f"{codec_info['name']}.hdf5"))
manager.run(pipelines)