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
CASE = sys.argv[3]
COVERAGE_TYPE = sys.argv[4]
COVERAGE = sys.argv[5]

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
clustering = codec2clustering.get(f"{CODEC_CLASS}_{CODEC_TYPE}", dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6))


# compile workflows
if CASE == "worst":
    workflow = dt4dds_benchmark.workflows.WorstCase
elif CASE == "best":
    workflow = dt4dds_benchmark.workflows.BestCase
else:
    raise ValueError(f"Unknown case: {CASE}")

if COVERAGE_TYPE == "seqdepth":
    workflow = functools.partial(workflow, sequencing_depth=COVERAGE, aging_halflives=0)
    func_kwarg = 'initial_coverage'
    vary_range = [0.1, 1000]
elif COVERAGE_TYPE == "initcov":
    workflow = functools.partial(workflow, initial_coverage=COVERAGE, aging_halflives=0)
    func_kwarg = 'sequencing_depth'
    vary_range = [0.1, 1000]
else:
    raise ValueError(f"Unknown type: {COVERAGE_TYPE}")

# create and run focus variator
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{COVERAGE_TYPE}/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
variator = dt4dds_benchmark.pipelines.FocusVariator(
    manager = manager, 
    pipeline = dt4dds_benchmark.pipelines.Full, 
    fixed_kwargs = {'input_file': input_path, 'clustering': clustering, 'codec': codec, 'process_timeout': 1*60*60},
    vary_kwarg = 'workflow',
    func = workflow,
    func_kwarg = func_kwarg,
    vary_range = vary_range
)
variator.run()