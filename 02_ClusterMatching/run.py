import dt4dds_benchmark
import pathlib
import sys
import functools

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = pathlib.Path(sys.argv[1]).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CODEC_CLASS, CODEC_TYPE = sys.argv[2].split('_')
CLUSTERING = sys.argv[3]

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


# compile clustering algorithms
if CLUSTERING == "basic":
    clustering = dt4dds_benchmark.clustering.BasicSet.default()
elif CLUSTERING == "cdhit":
    clustering = dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6)
elif CLUSTERING == "mmseqs2":
    clustering = dt4dds_benchmark.clustering.MMseqs2('covmode1', coverage_mode=1)
elif CLUSTERING == "starcode":
    clustering = dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6)
elif CLUSTERING == "clover":
    clustering = dt4dds_benchmark.clustering.Clover("D15V4", depth=15, vertical_drift=4)
elif CLUSTERING == "lsh":
    clustering = dt4dds_benchmark.clustering.LSH('default')
else:
    raise ValueError(f"Unknown clustering: {CLUSTERING}")


# run variator for both clustering algorithms
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{CLUSTERING}/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
variator = dt4dds_benchmark.pipelines.FocusVariator(
    manager = manager, 
    pipeline = dt4dds_benchmark.pipelines.Full, 
    fixed_kwargs = {'input_file': input_path, 'clustering': clustering, 'codec': codec, 'process_timeout': 1*60*60},
    vary_kwarg = 'workflow',
    func = functools.partial(dt4dds_benchmark.workflows.ErrorGenerator.from_ratio, r_subs=0.53, r_dels=0.45, r_ins=0.02, coverage=30),
    func_kwarg = 'overall_rate',
    vary_range = [0.001, 0.4],
    metric_reversed = True, # higher error = less success
)
variator.run()