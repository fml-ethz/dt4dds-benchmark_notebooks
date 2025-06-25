import dt4dds_benchmark
import pathlib
import sys

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = pathlib.Path(sys.argv[1]).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CODEC_CLASS, CODEC_TYPE = sys.argv[2].split('_')
CASE = sys.argv[3]

# designate input file
input_path, filesize = dt4dds_benchmark.inputs.random_19kB, dt4dds_benchmark.inputs.random_19kB.stat().st_size

# compile codecs
if CODEC_CLASS == "aeon":
    codec = dt4dds_benchmark.codecs.DNAAeon
elif CODEC_CLASS == "fountain":
    codec = dt4dds_benchmark.codecs.DNAFountain
elif CODEC_CLASS == "goldman":
    codec = dt4dds_benchmark.codecs.Goldman
elif CODEC_CLASS == "rs":
    codec = dt4dds_benchmark.codecs.DNARS
elif CODEC_CLASS == "hedges":
    codec = dt4dds_benchmark.codecs.HEDGES
elif CODEC_CLASS == "yinyang":
    codec = dt4dds_benchmark.codecs.YinYang
else:
    raise ValueError(f"Unknown codec: {CODEC_CLASS}")

if CODEC_TYPE == "low":
    codec = codec.low_coderate(filesize)
elif CODEC_TYPE == "medium":
    codec = codec.medium_coderate(filesize)
elif CODEC_TYPE == "high":
    codec = codec.high_coderate(filesize)
elif CODEC_TYPE == "default":
    codec = codec.default(filesize)
else:
    raise ValueError(f"Unknown codec: {CODEC_TYPE}")


# get clustering algorithm
codec2clustering = {
    'fountain_low': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
    'fountain_medium': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
    'hedges_low': dt4dds_benchmark.clustering.LSH('default'),
    'goldman_default': dt4dds_benchmark.clustering.LSH('default'),
}
clusterings = [
    dt4dds_benchmark.clustering.BasicSet('default'),
    codec2clustering.get(f"{CODEC_CLASS}_{CODEC_TYPE}", dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6)),
]


# compile workflows
if CASE == "serialpcr":
    workflow = lambda x: dt4dds_benchmark.workflows.SerialPCR(n_pcrs = x)
    range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
elif CASE == "serialdilution":
    workflow = lambda x: dt4dds_benchmark.workflows.SerialDilution(n_dilutions = x)
    range = [0, 1, 2, 3, 4, 5, 6, 7, 8]
elif CASE == "downsampling":
    workflow = lambda x: dt4dds_benchmark.workflows.Downsampling(coverage = x)
    range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
else:
    raise ValueError(f"Unknown case: {CASE}")

# create and run pipelines
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{CASE}/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
pipelines = dt4dds_benchmark.pipelines.Full.factory(
    input_files=[input_path],
    codecs=[codec],
    workflows=[workflow(i) for i in range],
    clusterings=clusterings,
    n_iterations=5,
    process_timeout=1*60*60,
)
manager.run(pipelines)