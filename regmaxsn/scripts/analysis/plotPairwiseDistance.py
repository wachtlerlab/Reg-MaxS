import os
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from regmaxsn.core.matplotlibRCParams import mplPars

homeFolder = os.path.expanduser('~')


def plotPairwiseDistances(parFile):

    plt.ion()
    sns.set(rc=mplPars)

    with open(parFile) as fle:
        parsList = json.load(fle)

    transErrs = pd.DataFrame(None, columns=['Exp. Name', 'Pairwise Distance in $\mu$m'])


    for par in parsList:

        refSWC = par['refSWC']
        resFile = par['resFile']

        testName = resFile[:-4]
        thresh = par['gridSizes'][-1]

        print('Doing ' + repr((refSWC, resFile)))

        refPts = np.loadtxt(refSWC)[:, 2:5]
        testPts = np.loadtxt(resFile)[:, 2:5]

        if refPts.shape[0] != testPts.shape[0]:

            print('Number of points do not match for ' + refSWC + 'and' + resFile)
            continue

        ptDiff = np.linalg.norm(refPts - testPts, axis=1)

        transErrs = transErrs.append(pd.DataFrame({'Pairwise Distance in $\mu$m': ptDiff,
                                                   'Exp. Name': testName}),
                                     ignore_index=True)

    transErrsGr = transErrs.groupby(by='Exp. Name')
    regErrs = transErrsGr['Pairwise Distance in $\mu$m'].agg({'\% of points closer than\n lowest grid size':
                                                         lambda x: 100 * ((x <= thresh).sum()) / float(len(x))})

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 11.2))
    fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 11.2))


    with sns.axes_style('darkgrid'):

        sns.boxplot(x='Exp. Name', y='Pairwise Distance in $\mu$m',
                    ax=ax, data=transErrs, whis='range', color=sns.color_palette()[0])
        ax1.plot(range(regErrs.size), regErrs['\% of points closer than\n lowest grid size'],
                 color=sns.color_palette()[0], marker='o', linestyle='-', ms=10)

    ax.set_xlim(-1, len(regErrs))
    ax.plot(ax.get_xlim(), [thresh, thresh], 'r--')
    ax.set_ylim(0, 40)
    ax.set_xticklabels(['job {}'.format(x) for x in range(len(parsList))], rotation=90)
    ax.set_xlabel('')


    ax1.set_xlim(-1, len(regErrs))
    ax1.set_ylim(-10, 110)
    ax1.set_xticks(range(regErrs.size))
    ax1.set_xticklabels(['par{}'.format(x) for x in range(len(parsList))], rotation=90)
    ax1.set_ylabel('\% of points closer than\n lowest grid size')



    for ind, f in enumerate([fig, fig1]):
        # f.canvas.draw()
        f.tight_layout()


    return fig, fig1

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python plotPairwiseDistance.py parFile\''

    parFile = sys.argv[1]
    figs = plotPairwiseDistances(parFile)
    raw_input('Press any key to close figures and quit:')

