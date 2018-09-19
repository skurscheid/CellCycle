__author__ = "Sebastian Kurscheid (sebastian.kurscheid@anu.edu.au)"
__license__ = "MIT"
__date__ = "2018-09-015"

from snakemake.exceptions import MissingInputException
import os

REF_GENOME = config["references"]["active"]
REF_VERSION = config["references"][REF_GENOME]["version"]
RUN_ID = "N08851_SK_LR1807201_SEQ"
PROJECT_ID = "LR1807201"

rule:
    version:
        "1.0"

localrules:
    all

home = os.environ['HOME']

include_prefix = home + "/Development/JCSMR-Tremethick-Lab/CellCycle/snakemake/rules/"

include:
    include_prefix + "run_fastp.py"
include:
    include_prefix + "run_alignment.py"
include:
    include_prefix + "deepTools_QC.py"
include:
    include_prefix + "deepTools_plotting.py"


rule execute_collectInsertSize:
    input:
        expand("{assayType}/picardTools/CollectInsertSizeMetrics/{reference_version}/{runID}/{library}.{suffix}",
                assayType = "ChIP-Seq",
                reference_version = REF_VERSION,
                project = "LR1807201",
                runID = "N08851_SK_LR1807201_SEQ",
                library = [x for x in config["samples"]["ChIP-Seq"]["LR1807201"]["N08851_SK_LR1807201_SEQ"].keys()],
                suffix = ["histogram.pdf", "insert_size_metrics.txt"])


rule execute_deepTools_QC:
    input:
        expand("{assayType}/{project}/{runID}/deepTools/plotFingerprint/{reference_version}/{condition}/fingerprints.png",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               condition = ["G1", "M"]),
        expand("{assayType}/{project}/{runID}/deepTools/bamPEFragmentSize/{reference_version}/{condition}/histogram.png",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               condition = ["G1", "M"]),
        expand("{assayType}/{project}/{runID}/deepTools/plotPCA/{reference_version}/{condition}/PCA_readCounts.png",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               condition = ["G1", "M"]),
        expand("{assayType}/{project}/{runID}/deepTools/plotCorrelation/{reference_version}/{condition}/heatmap_SpearmanCorr_readCounts.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               condition = ["G1", "M"],
               suffix = ["png", "tab"])


rule execute_deepTools_plotting:
    input:
        expand("{assayType}/{project}/{runID}/deepTools/computeMatrix/scale-region/{reference_version}/{region}/matrix_{suffix}.gz",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               reference_version = REF_VERSION,
               runID = RUN_ID,
	       suffix = "RPKM",
               region = ["allGenes"])


rule all:
    input:
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}.bam.bai",
                assayType = "ChIP-Seq",
                reference_version = REF_VERSION,
                project = "LR1807201",
                runID = "N08851_SK_LR1807201_SEQ",
                library = [x for x in config["samples"]["ChIP-Seq"]["LR1807201"]["N08851_SK_LR1807201_SEQ"].keys()])
