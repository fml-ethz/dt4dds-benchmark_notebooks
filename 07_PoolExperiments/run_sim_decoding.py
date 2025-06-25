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
CLUSTERING = sys.argv[4]


# define folder for codec input files
codec_folder = pathlib.Path("./codec_data")
if not codec_folder.exists():
    raise FileNotFoundError(f"Folder {codec_folder} must already exist with the input files.")

design_folder = pathlib.Path("./final")
if not design_folder.exists():
    raise FileNotFoundError(f"Folder {design_folder} must already exist with the design files.")


# get clustering algorithm
if CLUSTERING == "basic":
    clustering = dt4dds_benchmark.clustering.BasicSet.default()
else:
    codec2clustering = {
        'fountain_medium': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
        'goldman': dt4dds_benchmark.clustering.LSH('default'),
    }
    clustering = codec2clustering.get(f"{CODEC}", dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6))


# define the codec and inputs
codecs_dict = {c['name']: c for c in POOL_CODECS}
if CODEC not in codecs_dict:
    raise ValueError(f"Codec {CODEC} not found.")
codec = codecs_dict[CODEC]['codec']
input_file = codecs_dict[CODEC]['input']
design_file = design_folder / f"{CODEC}.txt"
codec_folder = codec_folder / CODEC

# we use the pool workflow depending on the scenario
if SCENARIO == "worstcase":
    workflow = dt4dds_benchmark.workflows.Pool_Worstcase
elif SCENARIO == "bestcase":
    workflow = dt4dds_benchmark.workflows.Pool_Bestcase
else:
    raise ValueError(f"Scenario {SCENARIO} not found.")


# create and run focus variator
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./sim_data/{SCENARIO}/{CLUSTERING}/{CODEC}.hdf5')
variator = dt4dds_benchmark.pipelines.FocusVariator(
    manager = manager, 
    pipeline = dt4dds_benchmark.pipelines.NoEncode, 
    fixed_kwargs = {'design_file': design_file, 'codec': codec, 'clustering': clustering, 'input_file': input_file, 'codec_folder': codec_folder, 'process_timeout': 1*60*60},
    vary_kwarg = 'workflow',
    func = workflow,
    func_kwarg = 'coverage',
    vary_range = [0.1, 1000]
)
variator.run()