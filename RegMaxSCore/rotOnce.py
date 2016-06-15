from SWCTransforms import SWCRotate, ArgGenIterator, objFun
import multiprocessing as mp
import numpy as np
import json
import sys
from itertools import product
from transforms import compose_matrix


assert len(sys.argv) == 2, 'Only one argument, the path of the swcfile expected, ' + str(len(sys.argv)) + 'found'

parFile = sys.argv[1]
with open(parFile, 'r') as fle:
    pars = json.load(fle)

refSWC, SWC2Align, outFiles, gridSizes, bounds, minRes, nCPU = pars

data = np.loadtxt(SWC2Align)[:, 2:5]
dataCentered = data - data.mean(axis=0)
maxDist = np.linalg.norm(data, axis=1).max()
pool = mp.Pool(processes=nCPU)

SWCDatas = [SWCRotate(refSWC, SWC2Align, x) for x in gridSizes]
stepSizes = [max(x / maxDist, minRes) for x in gridSizes]

bestSol = [0, 0, 0]

for gridInd, gridSize in enumerate(gridSizes):

    # print('Gridsize:' + str(gridSize))
    stepSize = stepSizes[gridInd]
    # print('Stepsize: ' + str(np.rad2deg(stepSize)))
    bounds = (np.array(bounds).T - np.array(bestSol)).T
    boundsRoundedUp = np.sign(bounds) * np.ceil(np.abs(bounds) / stepSize) * stepSize
    possiblePts1D = [np.round(bestSol[ind] + np.arange(x[0], x[1] + stepSize, stepSize), 3).tolist()
                     for ind, x in enumerate(boundsRoundedUp)]
    # print(np.rad2deg([bestSol[ind] + x for ind, x in enumerate(boundsRoundedUp)]))
    possiblePts3D = np.round(list(product(*possiblePts1D)), 6).tolist()
    argGen = ArgGenIterator(possiblePts3D, SWCDatas[gridInd])
    funcVals = pool.map(objFun, argGen)
    minimum = min(funcVals)
    minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]

    if not gridInd:
        distFrom0 = np.linalg.norm(minimzers, axis=1)
        bestSol = minimzers[np.argmin(distFrom0)]
    else:

        prevVals = [objFun((x, SWCDatas[gridInd - 1])) for x in minimzers]
        bestSol = minimzers[np.argmin(prevVals)]
    bounds = map(lambda x: [x - np.sqrt(2) * stepSize, x + np.sqrt(2) * stepSize], bestSol)
    bestVal = objFun((bestSol, SWCDatas[gridInd]))
    # print(np.rad2deg(bestSol), bestVal)


if minRes < (2 * gridSizes[-1] / maxDist):

    # print('Stepsize: ' + str(np.rad2deg(minRes)))
    bounds = (np.array(bounds).T - np.array(bestSol)).T
    boundsRoundedUp = np.sign(bounds) * np.ceil(np.abs(bounds) / minRes) * minRes
    # print(np.rad2deg([bestSol[ind] + x for ind, x in enumerate(boundsRoundedUp)]))
    possiblePts1D = [np.round(bestSol[ind] + np.arange(x[0], x[1] + minRes, minRes), 3).tolist()
                     for ind, x in enumerate(boundsRoundedUp)]
    possiblePts3D = np.round(list(product(*possiblePts1D)), 6).tolist()

    argGen = ArgGenIterator(possiblePts3D, SWCDatas[-1])
    funcVals = pool.map(objFun, argGen)
    minimum = min(funcVals)
    minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]
    prevVals = [objFun((x, SWCDatas[-2])) for x in minimzers]
    bestSol = minimzers[np.argmin(prevVals)]
    # print(np.rad2deg(bestSol), bestVal)

bestVal = objFun((bestSol, SWCDatas[-1]))
nochange = objFun(([0, 0, 0], SWCDatas[-1]))
# print(np.rad2deg(bestSol), bestVal, nochange)

done = bestVal >= nochange

if bestVal > nochange:
    bestSol = [0, 0, 0]
    bestVal = nochange

# done = bestVal == nochange

SWCDatas[-1].writeSolution(outFiles[0], bestSol)
matrix = compose_matrix(angles=bestSol).tolist()
with open(outFiles[1], 'w') as fle:
    json.dump({'type': 'XYZ Euler Angles in radians','bestSol': bestSol,
               'transMat': matrix, 'done': done, 'bestVal': bestVal}, fle)


