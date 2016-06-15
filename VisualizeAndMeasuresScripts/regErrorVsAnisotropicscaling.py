import os
from GJEMS.morph.funcs import getEulerAnglesWithStartTargetVector
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import json

homeFolder = os.path.expanduser('~')

plt.ion()
mplPars = { 'text.usetex'       :    True,
            'axes.labelsize'    :   'large',
            'font.family'       :   'sans-serif',
            'font.sans-serif'   :   'computer modern roman',
            'font.size'         :    24,
            'font.weight'       :   'black',
            'xtick.labelsize'   :    20,
            'ytick.labelsize'   :    20,
            }
# for key, val in mplPars.items():
#     plt.rcParams[key] = val

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

# testPath = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/Tests')
testPath = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/Tests')
origPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/Tests')
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

Ns = [0, 50]
highlightRange = [40, 50]

if len(Ns) == 1:
    Ns = [Ns[0], Ns[0] + 1]

testExpNames = []
cols = []

for n in range(Ns[0], Ns[1]):

    if highlightRange[0] <= n <= highlightRange[1]:
        col = 'r'
    else:
        col = 'b'
    for bn in baseNames:
        testExpNames.append(bn + 'RandTrans' + str(n))
        cols.append(col)


thresh = 10
# ----------------------------------------------------------------------------------------------------------------------

assert (len(testExpNames) == len(refExpNames)) or (len(refExpNames) == 1), 'Invalid input'

if len(refExpNames) == 1:
    refExpNames = [refExpNames[0]] * len(testExpNames)

# Axis 1: neuron pairs; Axis 2: (reg accuracy, anisotropic scaling)
translErrStats = np.empty((len(refExpNames),2))


for fInd, refExpName in enumerate(refExpNames):

    refSWC = os.path.join(refPath, refExpName + '.swc')
    testSWC = os.path.join(testPath, testExpNames[fInd] + '.swc')
    origJSON = os.path.join(origPath, testExpNames[fInd] + '.json')
    with open(origJSON, 'r') as fle:
        pars = json.load(fle)
        scales = np.array(pars['scale'])

    scalesOrdered = np.sort(scales)
    scalesRelative = np.mean([scalesOrdered[0] / scalesOrdered[1],
                              scalesOrdered[0] / scalesOrdered[2],
                              scalesOrdered[1] / scalesOrdered[2]])

    print('Doing ' + repr((refSWC, testSWC)))

    refPts = np.loadtxt(refSWC)[:, 2:5]
    testPts = np.loadtxt(testSWC)[:, 2:5]

    if refPts.shape[0] != testPts.shape[0]:

        print('Number of points do not match for ' + refSWC + 'and' + testSWC)
        continue


    ptDiff = np.linalg.norm(refPts - testPts, axis=1)
    translErrStats[fInd, 0] = 100 * sum(ptDiff <= thresh) / float(ptDiff.shape[0])
    translErrStats[fInd, 1] = scalesRelative

sns.set(rc=mplPars)
with sns.axes_style('whitegrid'):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

    for fInd, vals in enumerate(translErrStats):
        ax.plot(vals[1], vals[0], color=cols[fInd], marker='o', ls='None', ms=10)

ax.set_xlabel('measure of anisotropic scaling')
ax.set_ylabel('\% points closer than the lowest grid size')
ax.set_ylim(-10, 110)

fig.tight_layout()
fig.canvas.draw()

