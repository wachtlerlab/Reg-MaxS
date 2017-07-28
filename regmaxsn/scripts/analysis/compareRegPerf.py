import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from regmaxsn.core.matplotlibRCParams import mplPars
from regmaxsn.core.occupancyBasedMeasure import occupancyEMD
from regmaxsn.core.farthestPointStats import maxDistStats
import numpy as np

plt.ion()
sns.set(rc=mplPars)

def standardizedExpNameLambda(x):
    if x.endswith("_Standardized"):
        return x[:-len("_Standardized")]
    else:
        return x

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
homeFolder = "/media/ajay/ADATA_HD720/Ginjang/DataAndResults/morphology/"
case1 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC",),
    },
         'initRef': "Gad1-F-000062-Standardized",
         'expNameLambdas': [
             lambda x:x, lambda x:x, lambda x:x, lambda x:x, lambda x:x, standardizedExpNameLambda
         ]}

case2 = {'resDirs': {
    "PCA": os.path.join(homeFolder, "PCA-Based", "chiangLLC_Gad1-F-000062.CNG"),
    "blastneuron": os.path.join(homeFolder, "BlastNeuron", "chiangLLC_Gad1-F-000062.CNG"),
    "PCA + RobartsICP": os.path.join(homeFolder, "RobartsICP", "chiangLLC_Gad1-F-000062.CNG"),
    "Reg-MaxS": os.path.join(homeFolder, "Reg-MaxS", "chiangLLC_Gad1-F-000062.CNG"),
    "Reg-MaxS-N": os.path.join(homeFolder, "Reg-MaxS-N", "chiangLLC_Gad1-F-000062.CNG"),
    "Standardized": os.path.join(homeFolder, "Registered", "chiangLLC"),
    },
         'initRef': "Gad1-F-000062",
         'expNameLambdas': [
             lambda x:x, lambda x:x, lambda x:x, lambda x:x, lambda x:x, standardizedExpNameLambda
         ]}

cases = [case1, case2]

voxelSize = 10

metricsDF = pd.DataFrame()
maxDistStatsDF = pd.DataFrame()

for case in cases:

    resDirs = case["resDirs"]
    initRef = case["initRef"]
    expNameLambdas = case['expNameLambdas']

    for expNameLambda, (resDirLabel, resDir) in zip(expNameLambdas, resDirs.iteritems()):

        outFiles = []


        for expName in expNames:

            outFile = os.path.join(resDir, "{}.swc".format(expNameLambda(expName)))
            if os.path.isfile(outFile):
                outFiles.append(outFile)
            else:
                print("{} not found. Ignoring it.".format(outFile))

        if outFiles:

            print("Collecting data for resDirLabel={}, initRef={}".format(resDirLabel, initRef))

            metric = occupancyEMD(outFiles, voxelSize)

            tempDict = {"Initial Reference": initRef,
                        "Occupancy Based Similarity Measure": metric,
                        "Method": resDirLabel}

            metricsDF = metricsDF.append(tempDict, ignore_index=True)


            crdMaxDistsStatsDFFull = maxDistStats(outFiles)
            aggDictRename = {"mean": "mean of \nmaximum distances",
                       "std": "standard deviation of \nmaximum distances"}
            crdMaxDistsStatsDF = crdMaxDistsStatsDFFull.loc[:, ("maximum distance", "source point")]
            crdMaxDistsStatsDF.set_index("source point", inplace=True)
            crdMaxDistMeanStd = crdMaxDistsStatsDF.groupby("source point")["maximum distance"]\
                .aggregate([np.mean, np.std])
            crdMaxDistMeanStd = crdMaxDistMeanStd.rename(columns=aggDictRename)
            tempDF = crdMaxDistMeanStd.reset_index()
            tempDF['Initial Reference'] = initRef
            tempDF['Method'] = resDirLabel
            maxDistStatsDF = maxDistStatsDF.append(tempDF, ignore_index=True)

        else:
            print("No usable SWCs found in {}".format(resDir))

fig1, ax1 = plt.subplots(figsize=(14, 11.2))
sns.barplot(data=metricsDF, x="Initial Reference",
            y="Occupancy Based Similarity Measure", hue="Method",
            ax=ax1, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
                               "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
ax1.legend(loc='best', ncol=3)
ax1.set_ylabel("Occupancy Based Similarity Measure")


fig2, ax2 = plt.subplots(figsize=(14, 11.2))
sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="mean of \nmaximum distances",
            hue="Method", whis=np.inf,
            ax=ax2, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
                               "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
ax2.legend(loc="best", ncol=3)

fig3, ax3 = plt.subplots(figsize=(14, 11.2))
sns.boxplot(data=maxDistStatsDF, x="Initial Reference", y="standard deviation of \nmaximum distances",
            hue="Method", whis=np.inf,
            ax=ax3, hue_order=["PCA", "blastneuron","PCA + RobartsICP",
                               "Reg-MaxS", "Reg-MaxS-N", "Standardized"])
ax3.legend(loc="best", ncol=3)


for fig in [fig1, fig2, fig3]:
    fig.tight_layout()