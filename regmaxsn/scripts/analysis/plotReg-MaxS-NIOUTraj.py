import os
import numpy as np
from regmaxsn.core.misc import parFileCheck
from matplotlib import pyplot as plt
from regmaxsn.core.matplotlibRCParams import mplPars
import seaborn as sns
import sys
from functools import reduce


def plotIOUTraj(parFile, parNames):

    plt.ion()

    sns.set(rc=mplPars)

    parsList = parFileCheck(parFile, parNames)
    figs = []

    for parInd, pars in enumerate(parsList):

        gridSizes = pars['gridSizes']
        resDir = pars['resDir']
        swcList = pars['swcList']
        expNames = [os.path.split(swc)[1][:-4] for swc in swcList]

        iters = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') == 0])
        nIter = max(iters)

        cols = sns.color_palette('Set2', len(gridSizes))

        with sns.axes_style('darkgrid'):
            fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(14, 11.2))
            fig.suptitle('Job #{}'.format(parInd + 1))
        ax0, ax1, ax2 = axs
        figs.append(fig)

        for gridInd, gridSize in enumerate(gridSizes):
            print(('Doing gridSize = {} of {}'.format(gridSize, gridSizes)))
            nInts = []
            nUnions = []
            nIOUs = []

            for iterInd in range(nIter + 1):

                print(('Doing {}/{}'.format(iterInd + 1, nIter + 1)))
                alignedSWCs = [os.path.join(resDir, '{}{}.swc'.format(expName, iterInd)) for expName in expNames]

                indVoxs = []

                for aswc in alignedSWCs:
                    aPts = np.loadtxt(aswc)[:, 2:5]
                    aVox = np.array(aPts / gridSize, np.int32)
                    aVoxSet = set(map(tuple, aVox))
                    indVoxs.append(aVoxSet)

                aUnion = reduce(lambda x, y: x.union(y), indVoxs)
                aInt = reduce(lambda x, y: x.intersection(y), indVoxs)

                nInt = len(aInt)
                nUnion = len(aUnion)

                nIOU = 1 - nInt / float(nUnion)

                nInts.append(nInt)
                nUnions.append(nUnion)
                nIOUs.append(nIOU)

            with sns.axes_style('darkgrid'):
                ax0.plot(list(range(nIter + 1)), nInts, color=cols[gridInd], marker='o', ls='-', label=str(gridSize))
                ax0.set_xlim(-1, nIter + 2)
                ax0.set_xlabel('Iteration Number')
                ax0.set_ylabel('n(Intersection) (nI)')

                ax1.plot(list(range(nIter + 1)), nUnions, color=cols[gridInd], marker='o', ls='-', label=str(gridSize))
                ax1.set_xlim(-1, nIter + 2)
                ax1.set_xlabel('Iteration Number')
                ax1.set_ylabel('n(Union) (nU)')

                ax2.plot(list(range(nIter + 1)), nIOUs, color=cols[gridInd], marker='o', ls='-', label=str(gridSize))
                ax2.set_xlim(-1, nIter + 2)
                ax2.set_xlabel('Iteration Number')
                ax2.set_ylabel('1 - nI / nU')

    for fig in figs:
        fig.axes[0].legend()
        # fig.tight_layout()


    return figs

if __name__ == '__main__':

    from regmaxsn.core.RegMaxSPars import RegMaxSNParNames

    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python plotReg-MaxS-NIOUTraj.py parFile\''

    parFile = sys.argv[1]
    figs = plotIOUTraj(parFile, RegMaxSNParNames)
    input('Press any key to close figures and quit:')