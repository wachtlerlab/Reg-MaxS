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

homeFolder = "/media/ajay/ADATA_HD720/Ginjang/DataAndResults/morphology/"

expNames = [
            'Gad1-F-000062_Standardized',
            'Gad1-F-000062.CNG',
            'Cha-F-000012.CNG',
            'Cha-F-300331.CNG',
            'Gad1-F-600000.CNG',
            'Cha-F-000018.CNG',
            'Cha-F-300051.CNG',
            'Cha-F-400051.CNG',
            'Cha-F-200000.CNG'
            ]

case1 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC"),
    "BlastNeuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC",),
    },
        'initRef': "Gad1-F-000062\n-Standardized",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "BlastNeuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case2 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC_Gad1-F-000062.CNG"),
    "BlastNeuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC_Gad1-F-000062.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC_Gad1-F-000062.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC_Gad1-F-000062.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC_Gad1-F-000062.CNG"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC"),
    },
        'initRef': "Gad1-F-000062",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "BlastNeuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case3 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC_Cha-F-000018.CNG"),
    "BlastNeuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC_Cha-F-000018.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC_Cha-F-000018.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC_Cha-F-000018.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC_Cha-F-000018.CNG"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC"),
    },
        'initRef': "Cha-F-000018",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "BlastNeuron": lambda x: x,
            "PCA + RobartsICP": lambda x: x,
            "Reg-MaxS": lambda x: x,
            "Reg-MaxS-N": lambda x: x,
            "Standardized": standardizedExpNameLambda}
}

case4 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC_Cha-F-300331.CNG"),
    "BlastNeuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC_Cha-F-300331.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC_Cha-F-300331.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC_Cha-F-300331.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC_Cha-F-300331.CNG"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC"),
    },
        'initRef': "Cha-F-300331",
        'expNameLambdas': {
            "PCA": lambda x: x,
            "BlastNeuron": lambda x: x,
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

        for (resDirLabel, resDir) in resDirs.iteritems():

            outFiles = []
            expNameLambda = expNameLambdas[resDirLabel]

            for expName in expNames:

                outFile = os.path.join(resDir, "{}.swc".format(expNameLambda(expName)))
                if os.path.isfile(outFile):
                    outFiles.append(outFile)
                else:
                    print("{} not found. Ignoring it.".format(outFile))

            if outFiles:

                print("Collecting data for resDirLabel={}, initRef={}".format(resDirLabel, initRef))

                metric = occupancyEMD(outFiles, voxelSize)

                if resDirLabel == "Reg-MaxS-N":
                    finalRef = os.path.join(resDir, "finalRef.swc")
                    initialRef = os.path.join(resDir, "ref-1.swc")

                    runtime = os.stat(finalRef).st_mtime - os.stat(initialRef).st_mtime
                else:
                    outFileModTimes = [os.stat(outFile).st_mtime for outFile in outFiles]
                    outFileModTimesSorted = sorted(outFileModTimes)
                    nFiles = float(len(outFiles))
                    runtime = (outFileModTimesSorted[-1] - outFileModTimesSorted[0]) * nFiles / (nFiles - 1)

                tempDict = {"Initial Reference": initRef,
                            "Occupancy Based Dissimilarity Measure": metric,
                            "Total runtime (s)": runtime,
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
                print("No usable SWCs found in {}".format(resDir))

    metricsDF.to_excel(outXLFile)

def plotData(inFile):
    [darkblue, green, red, violet, yellow, lightblue] = sns.color_palette()

    metricsDF = pd.read_excel(inFile)
    fig1, ax1 = plt.subplots(figsize=(14, 11.2))
    sns.barplot(data=metricsDF, x="Initial Reference",
                y="Occupancy Based Dissimilarity Measure", hue="Method",
                ax=ax1, hue_order=["PCA", "PCA + RobartsICP", "BlastNeuron",
                                   "Reg-MaxS", "Reg-MaxS-N", "Standardized"],
                palette=[red, violet, yellow, lightblue, darkblue, green])
    ax1.legend(loc='best', ncol=3)
    ax1.set_ylabel("Occupancy Based Dissimilarity Measure")
    temp = ax1.get_ylim()
    ax1.set_ylim(temp[0], temp[1] + 2)

    # fig2, ax2 = plt.subplots(figsize=(14, 11.2))
    # sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="mean of \nmaximum distances",
    #             hue="Method", whis=np.inf,
    #             ax=ax2, hue_order=["PCA", "BlastNeuron","PCA + RobartsICP",
    #                                "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
    # ax2.legend(loc="best", ncol=3)
    #
    # fig3, ax3 = plt.subplots(figsize=(14, 11.2))
    # sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="standard deviation of \nmaximum distances",
    #             hue="Method", whis=np.inf,
    #             ax=ax3, hue_order=["PCA", "BlastNeuron","PCA + RobartsICP",
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
        raise(ValueError("Improper Usage! Please use as:\n"
                         "python {fName} save <outFile> or python {fName} plot <inFile>".format(fName=sys.argv[0])))