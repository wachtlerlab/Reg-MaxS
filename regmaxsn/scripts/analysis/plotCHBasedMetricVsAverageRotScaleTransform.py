import pandas as pd
from regmaxsn.core.maxDistanceBasedMetric import maxDistEMD
import pathlib2
import json
import numpy as np
import itertools
from matplotlib import pyplot as plt
import seaborn as sns
from regmaxsn.core.matplotlibRCParams import mplPars
import sys



dirPath = pathlib2.Path("/media/ajay/ADATA_HD720/Ginjang/DataAndResults/morphology/OriginalData/Tests")
expName = 'HSN-fluoro01.CNG'
swcSetSize = 20
N = 500

resDir = pathlib2.Path("/media/ajay/ADATA_HD720/Ginjang/DataAndResults/morphology/CHBasedMetricTests")

scaleDF = pd.DataFrame()
rotDF = pd.DataFrame()
transDF = pd.DataFrame()

suffixes = ("RandRotY", "RandScaleY", "RandTranslateY")
dfs = [rotDF, scaleDF, transDF]
labels = ("Rotation (degrees)", "Scale", "Translation (um)")
jsonKeys = ("angles", "scale", "translation")
parInds = (1, 1, 1)
figs = []


def saveData():
    for suffixInd, suffix in enumerate(suffixes):

        print(("Doing {}".format(labels[suffixInd])))

        parSWCDict = {}

        for ind in range(N):
            label = labels[suffixInd]
            jsonKey = jsonKeys[suffixInd]
            parInd = parInds[suffixInd]
            outFile = str(dirPath / '{}{}{}.swc'.format(expName, suffix, ind))
            transJSONFile = str(dirPath / '{}{}{}.json'.format(expName, suffix, ind))
            with open(transJSONFile, "r") as fle:
                transJSON = json.load(fle)
            jsonPars = transJSON[jsonKey]
            parSWCDict[jsonPars[1]] = outFile

        allPars = list(parSWCDict.keys())
        allParsSorted = np.sort(allPars)

        maxStepSize = int(np.floor(float(N) / float(swcSetSize)))
        baseSet = np.arange(0, swcSetSize)
        for stepSize in range(1, maxStepSize + 1):
            print(("Doing StepSize {}/{}".format(stepSize, maxStepSize)))
            windowSlideSize = int(stepSize * swcSetSize / 2)
            windowStarts = list(range(0, N - stepSize * swcSetSize + 1, windowSlideSize))
            for windowStart in windowStarts:
                print(("Doing Window start {}/{}".format(windowStart, windowStarts)))
                pars = allParsSorted[windowStart + stepSize * baseSet]
                swcFiles = [parSWCDict[par] for par in pars]
                metric = maxDistEMD(swcFiles)
                if suffix == "RandRotY":
                    pars = np.rad2deg(pars)
                tempDict = {"mean of {}".format(label): np.mean(pars),
                            "std of {}".format(label): np.std(pars),
                            "metric": metric}
                dfs[suffixInd] = dfs[suffixInd].append(tempDict, ignore_index=True)

        outFile = str(resDir / "metricVs{}.xlsx".format(suffix))
        dfs[suffixInd].to_excel(outFile)

def plotData():

    sns.set(rc=mplPars)
    figs = []
    for suffixInd, suffix in enumerate(suffixes):
        label = labels[suffixInd]
        dfXL = str(resDir / "metricVs{}.xlsx".format(suffix))
        df = pd.read_excel(dfXL)
        df["mean of {}".format(label)] = df["mean of {}".format(label)].apply(lambda x: round(x, 3))
        df["std of {}".format(label)] = df["std of {}".format(label)].apply(lambda x: round(x, 3))
        df2Plot = df.pivot(index="mean of {}".format(label),
                           columns="std of {}".format(label),
                           values="metric")
        fig, ax = plt.subplots(figsize=(14, 11.2))
        sns.heatmap(data=df2Plot, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation="vertical")
        ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
        fig.tight_layout()
        outFile = str(resDir / "metricVs{}.png".format(suffix))
        fig.savefig(outFile, dpi=150)
        figs.append(fig)


if __name__ == "__main__":

    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python {arg} save\' or' \
                               '\'python {arg} plot'.format(arg=sys.argv[0])

    if sys.argv[1] == "save":
        saveData()
    elif sys.argv[1] == "plot":
        plotData()
    else:
        raise ValueError