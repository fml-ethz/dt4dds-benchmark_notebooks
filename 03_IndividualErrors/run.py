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
WORKFLOW_TYPE = sys.argv[3]
CLUSTERING = sys.argv[4]

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
if CLUSTERING == "basic":
    clustering = dt4dds_benchmark.clustering.BasicSet.default()
else:
    codec2clustering = {
        'fountain_low': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
        'fountain_medium': dt4dds_benchmark.clustering.Starcode('sphereD6', spheres=True, distance=6),
        'hedges_low': dt4dds_benchmark.clustering.LSH('default'),
        'goldman_default': dt4dds_benchmark.clustering.LSH('default'),
    }
    clustering = codec2clustering.get(f"{CODEC_CLASS}_{CODEC_TYPE}", dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6))


# set workflow
if WORKFLOW_TYPE == "substitution":
    workflow = functools.partial(dt4dds_benchmark.workflows.ErrorGenerator, rate_deletions=0, rate_insertions=0, dropout=0, coverage=30)
    func_kwarg = 'rate_substitutions'
    vary_range = [0.001, 0.4]
elif WORKFLOW_TYPE == "deletion":
    workflow = functools.partial(dt4dds_benchmark.workflows.ErrorGenerator, rate_substitutions=0, rate_insertions=0, dropout=0, coverage=30)
    func_kwarg = 'rate_deletions'
    vary_range = [0.001, 0.4]
elif WORKFLOW_TYPE == "insertion":
    workflow = functools.partial(dt4dds_benchmark.workflows.ErrorGenerator, rate_substitutions=0, rate_deletions=0, dropout=0, coverage=30)
    func_kwarg = 'rate_insertions'
    vary_range = [0.001, 0.4]


# run variator for both clustering algorithms
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{WORKFLOW_TYPE}/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
variator = dt4dds_benchmark.pipelines.FocusVariator(
    manager = manager, 
    pipeline = dt4dds_benchmark.pipelines.Full, 
    fixed_kwargs = {'input_file': input_path, 'clustering': clustering, 'codec': codec, 'process_timeout': 1*60*60, 'metadata': {'name': WORKFLOW_TYPE}},
    vary_kwarg = 'workflow',
    func = workflow,
    func_kwarg = func_kwarg,
    vary_range = vary_range,
    metric_reversed = True, # higher error = less success
)
variator.run()