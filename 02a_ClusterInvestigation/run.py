import dt4dds_benchmark
import pathlib
import sys
import functools
import yaml
import pandas as pd

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


# create a variant clustering pipeline class which performs an error analysis after clustering
class ClusteringPipelineWithAnalysis(dt4dds_benchmark.pipelines.Full):

    @property
    def _pipeline(self):
        return [
            (self.codec, self.codec.encode, self.filepath_input, self.filepath_sequences, 'encoding'),
            (self.workflow, self.workflow.run, self.filepath_sequences, self.filepath_reads, 'workflow'),
            (self.clustering, self.clustering.run, self.filepath_reads, self.filepath_clusters, 'clustering'),
        ]

    def _customize_result(self, result):
        # add the encoding stats
        try:
            result.update(dt4dds_benchmark.tools.encoding_stats(self.input_file, self.filepath_sequences))
        except FileNotFoundError as e:
            logger.warning(f"Could not calculate encoding stats: {e}")

        # perform error analysis
        try:
            ref_seqs = dt4dds_benchmark.analysis.fileio.read_txt(pathlib.Path(self.filepath_sequences).resolve())
            clusters = dt4dds_benchmark.analysis.fileio.read_txt(self.filepath_clusters)
            seq_df = dt4dds_benchmark.analysis.clustering.compare_to_references(clusters, ref_seqs)
            result.update(dt4dds_benchmark.analysis.clustering.assess_clustering_performance(seq_df, ref_seqs))

        except Exception as e:
            logger.error(f"Error during analysis: {e}")



# run variator for both clustering algorithms
manager = dt4dds_benchmark.pipelines.HDF5Manager(f'./data/{CODEC_CLASS}_{CODEC_TYPE}.hdf5')
pipelines = ClusteringPipelineWithAnalysis.factory(
    input_files=[input_path],
    codecs=[codec],
    workflows=[dt4dds_benchmark.workflows.ErrorGenerator.from_ratio(overall_rate=r, r_subs=0.53, r_dels=0.45, r_ins=0.02, coverage=30) for r in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]],
    clusterings=[clustering],
)
manager.run(pipelines)