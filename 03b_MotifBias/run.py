import dt4dds_benchmark
import pathlib
import sys
import functools
import dataclasses

dt4dds_benchmark.tools.logs.setup_console()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = pathlib.Path(sys.argv[1]).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CODEC_CLASS, CODEC_TYPE = sys.argv[2].split('_')
ERRORTYPE = sys.argv[3]

# designate input file
input_path, filesize = dt4dds_benchmark.inputs.random_19kB, dt4dds_benchmark.inputs.random_19kB.stat().st_size


# create a subclass of the aeon codec that uses the motif-aware settings
@dataclasses.dataclass
class DNAAeonMotifs(dt4dds_benchmark.codecs.DNAAeon):

    # codebook settings
    codebook_words: pathlib.Path = './codewords/motif_codebooks.fasta'
    codebook_motifs: pathlib.Path = './codewords/motif_codebooks.json'
    
    @classmethod
    def high_coderate(cls, *args, **kwargs):
        kwargs.update(
            sync = 8,
            chunk_size = 28,
            package_redundancy = 0.035,
            error_detection = 'crc',
        )
        return cls("high", **kwargs)
    


# compile codecs
if CODEC_CLASS == "aeon":
    codec = dt4dds_benchmark.codecs.DNAAeon
elif CODEC_CLASS == "aeon-motif":
    codec = DNAAeonMotifs
elif CODEC_CLASS == "rs":
    codec = dt4dds_benchmark.codecs.DNARS
else:
    raise ValueError(f"Unknown codec: {CODEC_CLASS}")

if CODEC_TYPE == "medium":
    codec = codec.medium_coderate(filesize)
elif CODEC_TYPE == "high":
    codec = codec.high_coderate(filesize)


# get clustering algorithm
clustering = dt4dds_benchmark.clustering.CDHit('id85', identity_threshold=0.85, word_size=6)


# set workflow
base_errors = 0.03
base_dropout = 0.01
if ERRORTYPE == 'errors':
    workflow = functools.partial(
        dt4dds_benchmark.workflows.ErrorGeneratorMotifs.from_ratio,
        overall_rate=base_errors,
        r_subs=0.53, 
        r_dels=0.45, 
        r_ins=0.02,
        dropout=base_dropout,
        dropout_motif=base_dropout,
        coverage=30
    )
    func_kwarg = 'overall_rate_motif'
    vary_range = [base_errors, 0.5]
elif ERRORTYPE == 'dropout':
    workflow = functools.partial(
        dt4dds_benchmark.workflows.ErrorGeneratorMotifs.from_ratio,
        overall_rate=base_errors,
        overall_rate_motif=base_errors,
        r_subs=0.53, 
        r_dels=0.45, 
        r_ins=0.02,
        dropout=base_dropout,
        coverage=30
    )
    func_kwarg = 'dropout_motif'
    vary_range = [base_dropout, 1.0]
else:
    raise ValueError(f"Unknown error type: {ERRORTYPE}")


# run variator for both clustering algorithms
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{ERRORTYPE}/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
variator = dt4dds_benchmark.pipelines.FocusVariator(
    manager = manager, 
    pipeline = dt4dds_benchmark.pipelines.Full, 
    fixed_kwargs = {'input_file': input_path, 'clustering': clustering, 'codec': codec, 'process_timeout': 1*60*60, 'metadata': {'name': ERRORTYPE}},
    vary_kwarg = 'workflow',
    func = workflow,
    func_kwarg = func_kwarg,
    vary_range = vary_range,
    metric_reversed = True, # higher error = less success
)
variator.run()