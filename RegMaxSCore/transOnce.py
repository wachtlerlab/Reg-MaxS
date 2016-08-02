from SWCTransforms import SWCTranslate, ArgGenIterator, objFun
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

SWCDatas = [SWCTranslate(refSWC, SWC2Align, x) for x in gridSizes]
pool = mp.Pool(processes=nCPU)
bestSol = [0, 0, 0]

for gridInd, gridSize in enumerate(gridSizes):

    # print('Gridsize:' + str(gridSize))
    bounds = (np.array(bounds).T - np.array(bestSol)).T
    boundsRoundedUp = np.sign(bounds) * np.ceil(np.abs(bounds) / gridSize) * gridSize
    possiblePts1D = [(bestSol[ind] + np.arange(x[0], x[1] + gridSize, gridSize)).tolist()
                     for ind, x in enumerate(boundsRoundedUp)]
    # print([bestSol[ind] + x for ind, x in enumerate(boundsRoundedUp)])
    possiblePts3D = list(product(*possiblePts1D))
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
    bounds = map(lambda x: [x - gridSize, x + gridSize], bestSol)
    # bestVal = objFun((bestSol, SWCDatas[gridInd]))
    # print(bestSol, bestVal)

if minRes < gridSizes[-1]:

    bounds = (np.array(bounds).T - np.array(bestSol)).T
    boundsRoundedUp = np.sign(bounds) * np.ceil(np.abs(bounds) / minRes) * minRes
    # print([bestSol[ind] + x for ind, x in enumerate(boundsRoundedUp)])
    possiblePts1D = [(bestSol[ind] + np.arange(x[0], x[1] + minRes, minRes)).tolist()
                     for ind, x in enumerate(boundsRoundedUp)]
    possiblePts3D = list(product(*possiblePts1D))

    argGen = ArgGenIterator(possiblePts3D, SWCDatas[-1])
    funcVals = pool.map(objFun, argGen)

    minimum = min(funcVals)

    minimzers = [y for x, y in enumerate(possiblePts3D) if funcVals[x] == minimum]
    prevVals = [objFun((x, SWCDatas[-2])) for x in minimzers]
    bestSol = minimzers[np.argmin(prevVals)]

bestVal = objFun((bestSol, SWCDatas[-1]))
nochange = objFun(([0, 0, 0], SWCDatas[-1]))
# bestVals = [objFun((bestSol, x)) for x in SWCDatas]
# print(bestSol, bestVals, noChangeVals[-1])

done = False

# all values are worse than doing nothing
if bestVal > nochange:

    done = True
    bestSol = [0, 0, 0]
    bestVal = nochange

# best solution and no change are equally worse
elif bestVal == nochange:

    # the solution is very close to zero or there is already an exact overlap
    if np.abs(bestSol).max() <= min(minRes, gridSizes[-1]) or bestVal == 0:

        done = True
        bestSol = [0, 0, 0]
        bestVal = nochange



SWCDatas[-1].writeSolution(outFiles[0], bestSol)
matrix = compose_matrix(translate=bestSol).tolist()
with open(outFiles[1], 'w') as fle:
    json.dump({'type': 'XYZ Translations in um','bestSol': bestSol,
               'transMat': matrix, 'done': done, 'bestVal': bestVal}, fle)


