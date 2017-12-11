import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os
import sys
from regmaxsn.core.matplotlibRCParams import mplPars

sns.set(rc=mplPars)

setNames = ["LCInt", "ALPN", "OPInt", "AA1", "AA2"]
intSetNames = ["LLC", "OMB", "OPSInt", "AA1", "RAL"]

def combinePlotMethodComparisons(inDir):
    plt.ion()

    allPerfsDF = pd.DataFrame()
    for setInd, setName in enumerate(setNames):

        intSetName = intSetNames[setInd]

        metricsXL = os.path.join(inDir, "{}.xlsx".format(intSetName))


        if os.path.isfile(metricsXL):
            metricsDFNormed = pd.DataFrame()
            metricsDF = pd.read_excel(metricsXL)
            for irName, irDF in metricsDF.groupby("Initial Reference"):
                standardisedMeasure = float(irDF.loc[lambda df: df["Method"] == "Standardized",
                                                      "Occupancy Based Dissimilarity Measure"])
                irDF["Occupancy Based Dissimilarity Measure"] /= standardisedMeasure
                metricsDFNormed = metricsDFNormed.append(irDF)
            metricsDFNormed["Group"] = setName
            allPerfsDF = allPerfsDF.append(metricsDFNormed, ignore_index=True)

    [darkblue, green, red, violet, yellow, lightblue] = sns.color_palette()
    fig1, ax1 = plt.subplots(figsize=(14, 11.2))
    sns.barplot(data=allPerfsDF, x="Group", y="Occupancy Based Dissimilarity Measure",
                hue='Method', ax=ax1, hue_order=["PCA", "PCA + RobartsICP", "BlastNeuron",
                                                 "Reg-MaxS", "Reg-MaxS-N", "Standardized"],
                palette=[red, violet, yellow, lightblue, darkblue, green])
    ax1.set_ylabel("Occupancy Based Dissimilarity Measure\nNormalized to Standardized")
    ax1.set_xticklabels(setNames)
    # ax1.text(0, 12, 'n=4', color='r', fontsize=48)
    fig1.tight_layout()
    return fig1


if __name__ == "__main__":

    assert len(sys.argv) == 2, "Improper Usage! Please use as:\n" \
                             "python {} <directory with performance excel files".format(sys.argv[0])

    fig = combinePlotMethodComparisons(sys.argv[1])





