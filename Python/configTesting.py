import json
from pprint import pprint
from snakemake.io import expand
import os

REF_VERSION = "blablub"

with open("config_RNA-Seq_round_spermatids.json") as data_file:
    config = json.load(data_file)

with open("config.json") as data_file:
    config = json.load(data_file)

wildcards = dict()
wildcards = {"assayType" : "ChIP-Seq",
             "project" : "LR1807201",
             "runID" : "N08851_SK_LR1807201_SEQ",
             "library" : "INPUTM-2"}

REF_VERSION = "GRCh38_ensembl84"
RUN_ID = "N08851_SK_LR1807201_SEQ"
PROJECT_ID = "LR1807201"
home = os.environ['HOME']

expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
       assayType = "ChIP-Seq",
       project = "LR1807201",
       runID = RUN_ID,
       reference_version = REF_VERSION,
       library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID]["M"]["ChIP"] ],
       replicate = ["-1", "-2"],
       suffix = ["bam"])

expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
       assayType = "ChIP-Seq",
       project = "LR1807201",
       runID = RUN_ID,
       reference_version = REF_VERSION,
       library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID]["M"]["Input"] ],
       replicate = ["-1", "-2"],
       suffix = ["bam"])
