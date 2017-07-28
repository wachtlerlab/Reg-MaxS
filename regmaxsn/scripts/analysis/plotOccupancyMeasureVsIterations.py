from regmaxsn.core.occupancyBasedMeasure import occupancyEMD, calcOccupancyDistribution
from regmaxsn.core.matplotlibRCParams import mplPars
from matplotlib import pyplot as plt
from regmaxsn.core.misc import parFileCheck
import pandas as pd
import os
import seaborn as sns
import sys
import numpy as np


def plotMaxDistEMDVsIteration(parFile, parNames):

    sns.set(rc=mplPars)

    plt.ion()

    metricsDF = pd.DataFrame()


    parsList = parFileCheck(parFile, parNames)

    for parInd, pars in enumerate(parsList):
        resDir = pars['resDir']
        swcList = pars['swcList']
        gridSizes = pars["gridSizes"]
        expNames = [os.path.split(swc)[1][:-4] for swc in swcList]

        iters = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') == 0])
        nIter = max(iters)

        distributionsDF = pd.DataFrame()

        for iterInd in range(nIter + 1):
            print('Doing {}/{}'.format(iterInd + 1, nIter + 1))
            iterSWCs = [os.path.join(resDir, '{}{}.swc'.format(expName, iterInd)) for expName in expNames]

            for gridSize in gridSizes:
                metric = occupancyEMD(iterSWCs, gridSize)
                occupancyDist = calcOccupancyDistribution(iterSWCs, gridSize)
                tempDict = {}
                for k, v in occupancyDist.iteritems():
                    tempDict["Occupancy"] = k
                    tempDict["Occupancy PMF"] = v
                    tempDict["gridSize"] = gridSize
                    tempDict["Iteration"] = iterInd + 1
                    distributionsDF = distributionsDF.append(tempDict, ignore_index=True)

                tempDict = {"Job Number": parInd + 1, "Iteration Number": iterInd + 1,
                            "Occupancy based Metric": metric, "gridSize": gridSize}
                metricsDF = metricsDF.append(tempDict, ignore_index=True)

        distributionsDFGBGS = distributionsDF.groupby("gridSize")
        fig, axs = plt.subplots(figsize=(14, 11.2), nrows=len(distributionsDFGBGS.groups))
        for ax, (gridSize, distributionsDFGS) in zip(axs, distributionsDFGBGS):
            sns.pointplot(data=distributionsDFGS,
                          x="Occupancy", y="Occupancy PMF",
                          hue="Iteration",
                          palette=sns.diverging_palette(255, 133, l=60, n=7, center="dark"),
                          ci=0,
                          linestyles="-", markers="o", ax=ax)
            ax.set_ylabel("Occupancy PMF")
            ax.set_title("gridSize={}".format(gridSize))
        fig.suptitle("Job number {}".format(parInd + 1))
        fig.tight_layout()

    metricGBgridSize = metricsDF.groupby("gridSize")
    fig, axs = plt.subplots(figsize=(14, 11.2), nrows=len(metricGBgridSize.groups))

    for ax, (gridSize, metricsDFGS) in zip(axs, metricGBgridSize):

        sns.pointplot(data=metricsDFGS,
                      x="Iteration Number", y="Occupancy based Metric", hue="Job Number",
                      ci=None, linestyles="-", markers="o", ax=ax)
        ax.set_ylabel("Occupancy based Metric")
        ax.set_title("gridSize={}".format(gridSize))
    fig.tight_layout()
    return fig


if __name__ == '__main__':

    from regmaxsn.core.RegMaxSPars import RegMaxSNParNames

    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python {} parFile\''.format(sys.argv[1])

    parFile = sys.argv[1]
    figs = plotMaxDistEMDVsIteration(parFile, RegMaxSNParNames)
    raw_input('Press any key to close figures and quit:')




