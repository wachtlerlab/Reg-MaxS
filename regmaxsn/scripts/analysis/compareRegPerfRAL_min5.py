import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from regmaxsn.core.matplotlibRCParams import mplPars
from regmaxsn.core.occupancyBasedMeasure import occupancyEMD
from regmaxsn.core.farthestPointStats import maxDistStats
import numpy as np
import sys

plt.ion()
sns.set(rc=mplPars)

def standardizedExpNameLambda(x):
    if x.endswith("_Standardized"):
        return x[:-len("_Standardized")]
    else:
        return x

homeFolder = "/home/aj/DataAndResults/morphology/"

expNames = [
    "Trh-F-700063_Standardized",
    "Trh-F-700063.CNG",
    "Trh-F-500050.CNG",
    "Trh-F-500106.CNG",
    "Trh-M-500051.CNG",
    "Trh-F-600071.CNG",
    "Trh-F-500093.CNG",
    "Trh-F-500148.CNG",
    "Trh-F-500154.CNG",
    "Trh-F-700018.CNG",
]

case1 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangRAL"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangRAL"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangRAL"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangRAL"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangRAL_min5"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangRAL",),
    },
        'initRef': "Trh-F-700063-Standardized",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "blastneuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case2 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangRAL_Trh-F-700063.CNG"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangRAL_Trh-F-700063.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangRAL_Trh-F-700063.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangRAL_Trh-F-700063.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangRAL_Trh-F-700063.CNG_min5"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangRAL"),
    },
        'initRef': "Trh-F-700063",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "blastneuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case3 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangRAL_Trh-F-700018.CNG"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangRAL_Trh-F-700018.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangRAL_Trh-F-700018.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangRAL_Trh-F-700018.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangRAL_Trh-F-700018.CNG_min5"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangRAL"),
    },
        'initRef': "Trh-F-700018",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "blastneuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case4 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangRAL_Trh-M-500051.CNG"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangRAL_Trh-M-500051.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangRAL_Trh-M-500051.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangRAL_Trh-M-500051.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangRAL_Trh-M-500051.CNG_min5"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangRAL"),
    },
        'initRef': "Trh-M-500051",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "blastneuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

cases = [case1, case2, case3, case4]


voxelSize = 10

def saveData(outXLFile):

    metricsDF = pd.DataFrame()
    maxDistStatsDF = pd.DataFrame()

    for case in cases:

        resDirs = case["resDirs"]
        initRef = case["initRef"]
        expNameLambdas = case['expNameLambdas']

        for (resDirLabel, resDir) in resDirs.items():

            outFiles = []
            expNameLambda = expNameLambdas[resDirLabel]

            for expName in expNames:

                outFile = os.path.join(resDir, "{}.swc".format(expNameLambda(expName)))
                if os.path.isfile(outFile):
                    outFiles.append(outFile)
                else:
                    print(("{} not found. Ignoring it.".format(outFile)))

            if outFiles:

                print(("Collecting data for resDirLabel={}, initRef={}".format(resDirLabel, initRef)))

                metric = occupancyEMD(outFiles, voxelSize)

                tempDict = {"Initial Reference": initRef,
                            "Occupancy Based Dissimilarity Measure": metric,
                            "Method": resDirLabel}

                metricsDF = metricsDF.append(tempDict, ignore_index=True)


                # crdMaxDistsStatsDFFull = maxDistStats(outFiles)
                # aggDictRename = {"mean": "mean of \nmaximum distances",
                #            "std": "standard deviation of \nmaximum distances"}
                # crdMaxDistsStatsDF = crdMaxDistsStatsDFFull.loc[:, ("maximum distance", "source point")]
                # crdMaxDistsStatsDF.set_index("source point", inplace=True)
                # crdMaxDistMeanStd = crdMaxDistsStatsDF.groupby("source point")["maximum distance"]\
                #     .aggregate([np.mean, np.std])
                # crdMaxDistMeanStd = crdMaxDistMeanStd.rename(columns=aggDictRename)
                # tempDF = crdMaxDistMeanStd.reset_index()
                # tempDF['Initial Reference'] = initRef
                # tempDF['Method'] = resDirLabel
                # maxDistStatsDF = maxDistStatsDF.append(tempDF, ignore_index=True)

            else:
                print(("No usable SWCs found in {}".format(resDir)))

    metricsDF.to_excel(outXLFile)

def plotData(inFile):


    metricsDF = pd.read_excel(inFile)
    fig1, ax1 = plt.subplots(figsize=(14, 11.2))
    sns.barplot(data=metricsDF, x="Initial Reference",
                y="Occupancy Based Dissimilarity Measure", hue="Method",
                ax=ax1, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
                                   "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
    ax1.legend(loc='best', ncol=3)
    ax1.set_ylabel("Occupancy Based Dissimilarity Measure")

    # fig2, ax2 = plt.subplots(figsize=(14, 11.2))
    # sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="mean of \nmaximum distances",
    #             hue="Method", whis=np.inf,
    #             ax=ax2, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
    #                                "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
    # ax2.legend(loc="best", ncol=3)
    #
    # fig3, ax3 = plt.subplots(figsize=(14, 11.2))
    # sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="standard deviation of \nmaximum distances",
    #             hue="Method", whis=np.inf,
    #             ax=ax3, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
    #                                "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
    # ax3.legend(loc="best", ncol=3)


    # for fig in [fig1, fig2, fig3]:
    for fig in [fig1]:
        fig.tight_layout()

    return fig1

if __name__ == "__main__":

    assert len(sys.argv) == 3, "Improper Usage! Please use as:\n" \
                               "python {fName} save <outFile> or python {fName} plot <inFile>".format(fName=sys.argv[0])

    if sys.argv[1] == "save":
        saveData(sys.argv[2])
    elif sys.argv[1] == "plot":
        fig = plotData(sys.argv[2])
    else:
        raise ValueError
