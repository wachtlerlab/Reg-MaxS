from SWCTransforms import SWCScale, SWCTranslate, ArgGenIterator, objFun
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

refSWC, SWC2Align, outFiles, gridSizes, bounds, minStepSize, nCPU = pars

initBounds = bounds
boundL = lambda x, y: max(y[0], min(y[1], x))
data = np.loadtxt(SWC2Align)[:, 2:5]
dataCentered = data - data.mean(axis=0)
maxDist = np.linalg.norm(dataCentered, axis=1).max()
pool = mp.Pool(processes=nCPU)

SWCDatas = [SWCScale(refSWC, SWC2Align, x) for x in gridSizes]

bestSol = [1.0, 1.0, 1.0]

stepSizes = [max(minStepSize, (maxDist / (maxDist - g))) for g in gridSizes]

overestimationError = lambda d, g: (d + g) / d
underestimationError = lambda d, g: ((d + 1.5 * g) * d) / ((d - 0.5 * g) * (d + g))

for gridInd, gridSize in enumerate(gridSizes):

    # print('Gridsize:' + str(gridSize))
    stepSize = stepSizes[gridInd]
    # print(stepSize)
    bounds = np.array(bounds)
    boundsExponents = np.log([x / y for x, y in zip(bounds, bestSol)]) / np.log(stepSize)
    boundsExponentsRoundedDown = np.sign(boundsExponents) * np.ceil(np.abs(boundsExponents))
    # print([bestSol[x] * (stepSize ** y) for x, y in enumerate(boundsExponentsRoundedDown)])
    possiblePts1D = [(bestSol[x] * (stepSize ** np.arange(int(y[0]), int(y[1]) + 1)))
        for x, y in enumerate(boundsExponentsRoundedDown)]
    possiblePts3D = np.round(list(product(*possiblePts1D)), 6).tolist()
    argGen = ArgGenIterator(possiblePts3D, SWCDatas[gridInd])
    funcVals = pool.map(objFun, argGen)
    minimum = min(funcVals)
    minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]

    if not gridInd:

        distFrom0 = [np.mean([max(x, 1 / x) for x in y]) for y in minimzers]
        bestSol = minimzers[np.argmin(distFrom0)]
    else:

        prevVals = [objFun((x, SWCDatas[gridInd - 1])) for x in minimzers]
        bestSol = minimzers[np.argmin(prevVals)]
    bounds = [[boundL(x / overestimationError(maxDist, gridSize), iB),
               boundL(x * underestimationError(maxDist, gridSize), iB)]
              for x, iB in zip(bestSol, initBounds)]
    # print(bestSol)


if stepSizes[-1] > minStepSize:

    stepSize = minStepSize
    bounds = np.array(bounds)
    boundsExponents = np.log([x / y for x, y in zip(bounds, bestSol)]) / np.log(stepSize)
    boundsExponentsRoundedDown = np.sign(boundsExponents) * np.ceil(np.abs(boundsExponents))
    # print([bestSol[x] * (stepSize ** y) for x, y in enumerate(boundsExponentsRoundedDown)])
    possiblePts1D = [(bestSol[x] * (stepSize ** np.arange(int(y[0]), int(y[1]) + 1)))
        for x, y in enumerate(boundsExponentsRoundedDown)]
    possiblePts3D = np.round(list(product(*possiblePts1D)), 6).tolist()
    argGen = ArgGenIterator(possiblePts3D, SWCDatas[-1])
    funcVals = pool.map(objFun, argGen)
    minimum = min(funcVals)
    minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]
    prevVals = [objFun((x, SWCDatas[-2])) for x in minimzers]
    bestSol = minimzers[np.argmin(prevVals)]
    # print(bestSol, min(funcVals))

bestVal = objFun((bestSol, SWCDatas[-1]))
nochange = objFun(([1, 1, 1], SWCDatas[-1]))
# bestVals = [objFun((bestSol, x)) for x in SWCDatas]
# print(bestSol, nochange, bestVal)
done = bestVal >= nochange
if done:
    bestSol = [1, 1, 1]
    bestVal = nochange

# done = bestVal == nochange

SWCDatas[-1].writeSolution(outFiles[0], bestSol)
temp = SWCTranslate(refSWC, outFiles[0], gridSizes[-1])
bestVal = objFun(([0, 0, 0], temp))
matrix = compose_matrix(scale=bestSol).tolist()
with open(outFiles[1], 'w') as fle:
    json.dump({'type': 'XYZ Scales', 'bestSol': bestSol,
               'transMat': matrix, 'done': done, 'bestVal': bestVal}, fle)


