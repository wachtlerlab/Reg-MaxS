from regmaxsn.core.SWCTransforms import SWCRotate, ArgGenIterator, objFun
import multiprocessing as mp
import numpy as np
from itertools import product
import json
from matplotlib import pyplot as plt
import seaborn as sns
plt.ion()
import os
from regmaxsn.core.matplotlibRCParams import mplPars


sns.set(rc=mplPars)
# ----------------------------------------------------------------------------------------------------------------------
homeFolder = "/home/aj"
dirPath = os.path.join(homeFolder,'DataAndResults/morphology/OriginalData/borstHSN2D/')
#
expNames = [
            'HSN-fluoro01.CNG2D',
            'HSN-fluoro01.CNG2DRandRot',
            # 'HSN-fluoro01.CNG2DRandRot1',
            # 'HSN-fluoro01.CNG2DRandRot2',
            # 'HSN-fluoro01.CNG2DRandRot3',
            # 'HSN-fluoro01.CNG2DRandRot4',
            # 'HSN-fluoro01.CNG2DRandRot5',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot1',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot2',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot3',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot4',
            # 'HSN-fluoro01.CNGNoiseStd42DRandRot5',
            # 'HSN-fluoro02.CNG2D',
            # 'HSN-fluoro03.CNG',
            # 'HSN-fluoro04.CNG',
            # 'HSN-fluoro05.CNG2D',
            # 'HSN-fluoro06.CNG',
            # 'HSN-fluoro07.CNG',
            # 'HSN-fluoro08.CNG',
            # 'HSN-fluoro09.CNG',
            # 'HSN-fluoro10.CNG',
            ]


refInd = 0
resDir = os.path.join(homeFolder,'DataAndResults/morphology/directPixelBased/rotProfile2D/')
if not os.path.isdir(resDir):
    os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# gridSizes = [40.0, 20.0, 10.0]
gridSizes = [40.0]
# gridSizes = [20.0]
# gridSizes = [10.0]
bounds = [[0, 0], [0, 0], [-np.pi / 6, np.pi / 6]]

# bounds = [[0, 0], [-np.pi / 3, np.pi / 3], [-np.pi / 3, np.pi / 3]]


rotMinRes = np.deg2rad(1).round(4)
nCPU = 7

refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
SWC2Align = os.path.join(dirPath, expNames[1] + '.swc')
SWCRotCenter = np.loadtxt(SWC2Align)[:, 2:5].mean(axis=0)
data = np.loadtxt(SWC2Align)[:, 2:5] - SWCRotCenter
maxDist = np.linalg.norm(data, axis=1).max()
pool = mp.Pool(processes=nCPU)
with sns.axes_style('whitegrid'):
    # fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 5.6))

with open(os.path.join(dirPath, expNames[1] + '.json')) as fle:
    pars = json.load(fle)
    actualSol = -np.rad2deg(pars['angles'][2])


SWCDatas = [SWCRotate(refSWC, SWC2Align, x) for x in gridSizes]
noChangeVals = [objFun(([0, 0, 0], data)) for data in SWCDatas]
stepSizes = [2 * x / maxDist for x in gridSizes]

for gridInd, gridSize in enumerate(gridSizes):

    # print('Gridsize:' + str(gridSize))
    stepSize = stepSizes[gridInd]
    # print('Stepsize: ' + str(np.rad2deg(stepSize)))
    bounds = np.array(bounds)
    boundsRoundedUp = np.sign(bounds) * np.ceil(np.abs(bounds) / stepSize) * stepSize
    possiblePts1D = [np.round(np.arange(x[0], x[1] + 0.9 * stepSize, stepSize), 3).tolist() for x in boundsRoundedUp]
    possiblePts3D = np.round(list(product(*possiblePts1D)), 3).tolist()
    argGen = ArgGenIterator(possiblePts3D, SWCDatas[gridInd])
    funcVals = pool.map(objFun, argGen)
    outFile = os.path.join(resDir, expNames[refInd] + expNames[1] + str(int(gridSize)) + 'rot.json')
    with open(outFile, 'w') as fle:
        json.dump({'possiblePoints3D': possiblePts3D, 'funcVals': funcVals}, fle)
    with sns.axes_style('whitegrid'):

        # ax1 = ax[gridInd]
        ax1 = ax
        ax1.plot(np.rad2deg(possiblePts1D[2]), funcVals, 'b-o', lw=6, ms=12)
        ybounds = (0.1 * np.floor(min(funcVals)*10), 0.1 * np.ceil(max(funcVals)*10))
        ax1.set_ylim(ybounds)
        ax1.plot([actualSol] * 2, ybounds, 'r-', lw=6)
        ax1.set_ylabel(r'Dissimilarity')
        # ax1.set_title(r'GridSize=' + str(int(gridSize)) + '$\mu$m')
    if not gridInd:
        bestSol = possiblePts3D[np.argmin(funcVals)]
    else:
        minimum = min(funcVals)
        if minimum > noChangeVals[gridInd]:
            bestSol = [0, 0, 0]
        else:
        # if True:
            minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]
            prevVals = [objFun((x, SWCDatas[gridInd - 1])) for x in minimzers]
            bestSol = minimzers[np.argmin(prevVals)]

    bestVal = objFun((bestSol, SWCDatas[gridInd]))
    print(bestSol)

ax1.set_xlabel(r'rotation about Z in degrees')
fig.tight_layout()
fig.canvas.draw()