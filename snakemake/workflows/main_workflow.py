__author__ = "Sebastian Kurscheid (sebastian.kurscheid@anu.edu.au)"
__license__ = "MIT"
__date__ = "2018-09-015"

from snakemake.exceptions import MissingInputException
import os

REF_GENOME = config["references"]["active"]
REF_VERSION = config["references"][REF_GENOME]["version"]

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


rule execute_collectInsertSize:
    input:
        expand("{assayType}/picardTools/CollectInsertSizeMetrics/{reference_version}/{runID}/{library}.{suffix}",
                assayType = "ChIP-Seq",
                reference_version = REF_VERSION,
                project = "LR1807201",
                runID = "N08851_SK_LR1807201_SEQ",
                library = [x for x in config["samples"]["ChIP-Seq"]["LR1807201"]["N08851_SK_LR1807201_SEQ"].keys()],
                suffix = ["histogram.pdf", "insert_size_metrics.txt"])

rule all:
    input:
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}.bam.bai",
                assayType = "ChIP-Seq",
                reference_version = REF_VERSION,
                project = "LR1807201",
                runID = "N08851_SK_LR1807201_SEQ",
                library = [x for x in config["samples"]["ChIP-Seq"]["LR1807201"]["N08851_SK_LR1807201_SEQ"].keys()])
