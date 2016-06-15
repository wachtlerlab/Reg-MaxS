import os
from scipy.spatial import cKDTree
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

homeFolder = os.path.expanduser('~')

mplPars = { 'text.usetex'       :    True,
            'axes.labelsize'    :   'large',
            'font.family'       :   'sans-serif',
            'font.sans-serif'   :   'computer modern roman',
            'font.size'         :    24,
            'font.weight'       :   'black',
            'xtick.labelsize'   :    20,
            'ytick.labelsize'   :    20,
            }


def transErrorDist(refPath, refExpNames, testPath, testExpNames, thresh):

    plt.ion()

    # Allow only two cases: same number of ref and test files and a single ref files
    assert (len(testExpNames) == len(refExpNames)) or (len(refExpNames) == 1), 'Invalid input'

    if len(refExpNames) == 1:
        refExpNames = [refExpNames[0]] * len(testExpNames)

    transErrs = []

    for fInd, refExpName in enumerate(refExpNames):

        refSWC = os.path.join(refPath, refExpName + '.swc')
        testSWC = os.path.join(testPath, testExpNames[fInd] + '.swc')

        print('Doing ' + repr((refSWC, testSWC)))

        refPts = np.loadtxt(refSWC)[:, 2:5]
        testPts = np.loadtxt(testSWC)[:, 2:5]

        if refPts.shape[0] != testPts.shape[0]:

            print('Number of points do not match for ' + refSWC + 'and' + testSWC)
            continue

        ptDiff = np.linalg.norm(refPts - testPts, axis=1)

        transErrs.append(ptDiff)

    regErrs = [100 * sum(x <= thresh) / float(len(x)) for x in transErrs]

    sns.set(rc=mplPars)
    with sns.axes_style('whitegrid'):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        sns.boxplot(ax=ax, data=transErrs, color='b', notch=True)
    with sns.axes_style('darkgrid'):
        fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
        sns.barplot(ax=ax1, x=range(len(testExpNames)), y=regErrs, color='b')

    ax.set_ylabel('Translation Error in $\mu$m')
    ax.set_xlim(-1, len(testExpNames))
    ax.set_ylim(0, 2 * thresh)


    ax1.set_ylabel('\% of points closer than lowest grid size')
    ax1.set_xlim(-1, len(testExpNames))
    ax1.set_ylim(85, 100)


    for ind, f in enumerate([fig, fig1]):
        f.tight_layout()
        f.canvas.draw()

    return fig, fig1

# ----------------------------------------------------------------------------------------------------------------------
refPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/Tests')

refExpNames = [
            # 'HB130313-4',
            # 'HB130313-4NoiseStd1',
            # 'HB130313-4NoiseStd2',
            # 'HB130313-4NoiseStd3',
            # 'HB130313-4NoiseStd4',
            # 'HB130313-4NoiseStd5',
            # 'HB130313-4NoiseStd6',
            # 'HB130313-4NoiseStd7',
            # 'HB130313-4NoiseStd8',
            # 'HB130313-4NoiseStd9',
            # 'HB130313-4NoiseStd1RandTrans',
            # 'HB130313-4NoiseStd2RandTrans',
            # 'HB130313-4NoiseStd3RandTrans',
            # 'HB130313-4NoiseStd4RandTrans',
            # 'HB130313-4NoiseStd5RandTrans',
            # 'HB130313-4NoiseStd6RandTrans',
            # 'HB130313-4NoiseStd7RandTrans',
            # 'HB130313-4NoiseStd8RandTrans',
            # 'HB130313-4NoiseStd9RandTrans',


            'HSN-fluoro01.CNG',
            # 'HSN-fluoro01.CNGNoiseStd1',
            # 'HSN-fluoro01.CNGNoiseStd2',
            # 'HSN-fluoro01.CNGNoiseStd3',
            # 'HSN-fluoro01.CNGNoiseStd4',
            # 'HSN-fluoro01.CNGNoiseStd5',
            # 'HSN-fluoro01.CNGNoiseStd6',
            # 'HSN-fluoro01.CNGNoiseStd7',
            # 'HSN-fluoro01.CNGNoiseStd8',
            # 'HSN-fluoro01.CNGNoiseStd9',
            ]




# ----------------------------------------------------------------------------------------------------------------------

testPath = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/Tests')
# testPath = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/Tests')


baseNames = [
            # 'HB130313-4',
            # 'HB130313-5',
            # 'HB130313-6',
            # 'HB130313-7',
            # 'HB130313-8',
            'HSN-fluoro01.CNG',
            # 'HSN-fluoro01.CNGNoiseStd1',
            # 'HSN-fluoro01.CNGNoiseStd2',
            # 'HSN-fluoro01.CNGNoiseStd3',
            # 'HSN-fluoro01.CNGNoiseStd4',
            # 'HSN-fluoro01.CNGNoiseStd5',
            # 'HSN-fluoro01.CNGNoiseStd6',
            # 'HSN-fluoro01.CNGNoiseStd7',
            # 'HSN-fluoro01.CNGNoiseStd8',
            # 'HSN-fluoro01.CNGNoiseStd9',
            ]

Ns = [20, 30]

if len(Ns) == 1:
    Ns = [Ns[0], Ns[0] + 1]

testExpNames = []

for n in range(Ns[0], Ns[1]):
    for bn in baseNames:
        testExpNames.append(bn + 'RandTrans' + str(n))

# ----------------------------------------------------------------------------------------------------------------------
gridSizes = [40.0, 20.0, 10.0]
# gridSizes = [20.0, 10.0, 5.0]


if __name__ == '__main__':
    figs = transErrorDist(refPath, refExpNames, testPath, testExpNames, gridSizes[-1])


