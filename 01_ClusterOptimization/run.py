import dt4dds_benchmark
import pathlib
import sys

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = pathlib.Path(sys.argv[1]).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CLUSTER = sys.argv[2]

# get the clusterings to run based on selected clustering
if CLUSTER == "basic":
    clusterings = [
        dt4dds_benchmark.clustering.BasicSet('default'),
    ]
elif CLUSTER == "cdhit":
    clusterings = [
        dt4dds_benchmark.clustering.CDHit('default'),
        dt4dds_benchmark.clustering.CDHit('id80', identity_threshold=0.8, word_size=5),
        dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6),
    ]
elif CLUSTER == "clover":
    clusterings = [
        dt4dds_benchmark.clustering.Clover('default'),
        dt4dds_benchmark.clustering.Clover("D20", depth=20),
        dt4dds_benchmark.clustering.Clover("D10", depth=10),
        dt4dds_benchmark.clustering.Clover("D15V4", depth=15, vertical_drift=4),
        dt4dds_benchmark.clustering.Clover("D20V4", depth=20, vertical_drift=4),
        dt4dds_benchmark.clustering.Clover("D15H5", depth=15, horizontal_drift=5),
        dt4dds_benchmark.clustering.Clover("D20H5", depth=20, horizontal_drift=5),
    ]
elif CLUSTER == "mmseqs2":
    clusterings = [
        dt4dds_benchmark.clustering.MMseqs2('default'),
        dt4dds_benchmark.clustering.MMseqs2('id50', minimum_identity=0.5),
        dt4dds_benchmark.clustering.MMseqs2('covmode1', coverage_mode=1),
    ]
elif CLUSTER == "starcode":
    clusterings = [
        dt4dds_benchmark.clustering.Starcode('default'),
        dt4dds_benchmark.clustering.Starcode('sphere', spheres=True),
        dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
    ]
elif CLUSTER == "lsh":
    clusterings = [
        dt4dds_benchmark.clustering.LSH('default'),
    ]
else:
    raise ValueError(f"Unknown clustering {CLUSTER}")

# collect inputs
inputs = []
design_files = []
for syn_type in ('electrochemical', 'material'):
    inputs.append(pathlib.Path(__file__).parent / 'seq_data' / f'exp_{syn_type}_20x.txt')
    design_files.append(pathlib.Path(__file__).parent / 'seq_data' / f'reference_{syn_type}.fasta')
logger.info(f"Running clustering on inputs: {', '.join([str(i) for i in inputs])}")

# create and run pipelines
pipelines = [dt4dds_benchmark.pipelines.Clustering(
    input_file = i,
    clustering = c,
    design_file = f,
    output_folder = OUTPUT_DIR,
    process_timeout = 4*60*60,
) for i, f in zip(inputs, design_files) for c in clusterings]
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{CLUSTER}.hdf5')
manager.run(pipelines)