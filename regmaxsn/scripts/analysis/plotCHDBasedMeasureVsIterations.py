from regmaxsn.core.maxDistanceBasedMetric import maxDistEMD
from regmaxsn.core.matplotlibRCParams import mplPars
from matplotlib import pyplot as plt
from regmaxsn.core.misc import parFileCheck
import pandas as pd
import os
import seaborn as sns
import sys


def plotMaxDistEMDVsIteration(parFile, parNames):

    sns.set(rc=mplPars)

    plt.ion()

    metricsDF = pd.DataFrame()

    parsList = parFileCheck(parFile, parNames)

    for parInd, pars in enumerate(parsList):
        resDir = pars['resDir']
        swcList = pars['swcList']
        expNames = [os.path.split(swc)[1][:-4] for swc in swcList]

        iters = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') == 0])
        nIter = max(iters)

        centroidAlignedSWCs = [os.path.join(resDir, '{}{}.swc'.format(expName, 0)) for expName in expNames]

        for iterInd in range(nIter + 1):
            print('Doing {}/{}'.format(iterInd + 1, nIter + 1))
            iterSWCs = [os.path.join(resDir, '{}{}.swc'.format(expName, iterInd)) for expName in expNames]

            metric = maxDistEMD(iterSWCs, centroidAlignedSWCs)

            tempDict = {"Job Number": parInd + 1, "Iteration Number": iterInd,
                        "CH based Metric": metric}
            metricsDF = metricsDF.append(tempDict, ignore_index=True)

    fig, ax = plt.subplots(figsize=(14, 11.2))
    sns.pointplot(data=metricsDF,
                  x="Iteration Number", y="CH based Metric", hue="Job Number",
                  ci=None, linestyles="-", markers="o", ax=ax)
    fig.tight_layout()
    return fig


if __name__ == '__main__':

    from regmaxsn.core.RegMaxSPars import RegMaxSNParNames

    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python {} parFile\''.format(sys.argv[1])

    parFile = sys.argv[1]
    figs = plotMaxDistEMDVsIteration(parFile, RegMaxSNParNames)
    raw_input('Press any key to close figures and quit:')




