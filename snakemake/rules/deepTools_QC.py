__author__ = "Sebastian Kurscheid (sebastian.kurscheid@anu.edu.au)"
__license__ = "MIT"
__date__ = "2018-08-07"

# vim: syntax=python tabstop=4 expandtab
# coding: utf-8

from snakemake.exceptions import MissingInputException
import os

"""
Rules for running deepTools QC/QC on ChIP-Seq data
For usage, include this in your workflow.
"""

# global functions
def get_sample_labels(wildcards):
    sl = []
    runIDs = config["samples"][wildcards["assayType"]][wildcards["project"]]["runID"]
    for i in runIDs:
        for k in config["samples"]wildcards["assayType"]][wildcards["project"]][i].keys():
            sl.append(k)
    return(sl)

REF_VERSION = "GRCh38_ensembl84"
RUN_ID = "N08851_SK_LR1807201_SEQ"
PROJECT_ID = "LR1807201"
home = os.environ['HOME']

rule multiBamSummary:
    version:
        "2"
    params:
        deepTools_dir = home + config["program_parameters"]["deepTools"]["deepTools_dir"],
        binSize = config["program_parameters"]["deepTools"]["binSize"]
    threads:
        32
    input:
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["ChIP"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"]),
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["Input"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"])
    output:
        npz = "{assayType}/{project}/{runID}/deepTools/multiBamSummary/{reference_version}/{condition}/results.npz"
    shell:
        """
            {params.deepTools_dir}/multiBamSummary bins --bamfiles {input} \
                                                        --numberOfProcessors {threads} \
                                                        --centerReads \
                                                        --binSize {params.binSize} \
                                                        --outFileName {output.npz}
        """


rule plotCorrelation_heatmap:
    version:
        "2"
    params:
        deepTools_dir = home + config["program_parameters"]["deepTools"]["deepTools_dir"],
        plotTitle = "Correlation heatmap - read counts"
    input:
        npz = rules.multiBamSummary.output.npz
    output:
        png = "{assayType}/{project}/{runID}/deepTools/plotCorrelation/{reference_version}/{condition}/heatmap_SpearmanCorr_readCounts.png",
        tab = "{assayType}/{project}/{runID}/deepTools/plotCorrelation/{reference_version}/{condition}/heatmap_SpearmanCorr_readCounts.tab"
    shell:
        """
            {params.deepTools_dir}/plotCorrelation --corData {input.npz} \
                                                   --corMethod spearman \
                                                   --skipZeros \
                                                   --plotTitle "{params.plotTitle}" \
                                                   --whatToPlot heatmap \
                                                   --colorMap RdYlBu \
                                                   --plotNumbers \
                                                   -o {output.png} \
                                                   --outFileCorMatrix {output.tab}
        """

rule plotPCA:
    version:
        "2"
    params:
        deepTools_dir = home + config["program_parameters"]["deepTools"]["deepTools_dir"],
        plotTitle = "PCA - read counts"
    input:
        npz = rules.multiBamSummary.output.npz
    output:
        png = "{assayType}/{project}/{runID}/deepTools/plotPCA/{reference_version}/{condition}/PCA_readCounts.png"
    shell:
        """
            {params.deepTools_dir}/plotPCA --corData {input.npz} \
                                           --plotFile {output.png} \
                                           --plotTitle "{params.plotTitle}"
        """

rule bamPEFragmentSize:
    params:
        deepTools_dir = home + config["program_parameters"]["deepTools"]["deepTools_dir"],
        plotTitle = "BAM PE fragment size"
    threads:
        32
    input:
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["ChIP"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"]),
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["Input"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"])
    output:
        "{assayType}/{project}/{runID}/deepTools/bamPEFragmentSize/{reference_version}/{condition}/histogram.png"
    shell:
        """
            {params.deepTools_dir}/bamPEFragmentSize --bamfiles {input} \
                                                     --numberOfProcessors {threads} \
                                                     --histogram {output}
        """


rule plotFingerprint:
    params:
        deepTools_dir = home + config["program_parameters"]["deepTools"]["deepTools_dir"],
        plotTitle = "BAM PE fingerprint"
    threads:
        32
    input:
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["ChIP"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"]),
        expand("{assayType}/{project}/{runID}/samtools/rmdup/{reference_version}/{library}{replicate}.{suffix}",
               assayType = "ChIP-Seq",
               project = PROJECT_ID,
               runID = RUN_ID,
               reference_version = REF_VERSION,
               library = [ y for y in config["samples"]["ChIP-Seq"]["conditions"][RUN_ID][wildcards["condition"]]["Input"] ],
               replicate = ["-1", "-2"],
               suffix = ["bam"])
    output:
        "{assayType}/{project}/{runID}/deepTools/plotFingerprint/{reference_version}/{condition}/fingerprints.png"
    shell:
        """
            {params.deepTools_dir}/plotFingerprint --bamfiles {input} \
                                                   --numberOfProcessors {threads} \
                                                   --centerReads \
                                                   --plotTitle "{params.plotTitle}" \
                                                   --skipZeros \
                                                   --plotFile {output}
        """
