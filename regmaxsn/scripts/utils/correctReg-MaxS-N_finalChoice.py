import sys
from regmaxsn.scripts.algorithms.RegMaxSN import normalizeFinally
import os
from regmaxsn.core.misc import parFileCheck
from regmaxsn.core.RegMaxSPars import RegMaxSNParNames
from regmaxsn.core.occupancyBasedMeasure import occupancyEMD
import numpy as np
import json


def getRegMaxSNIterVsMeasure(resDir, swcList, voxelSize):

    itersAll = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') == 0])
    itersAll = [x for x in itersAll if x >= 0]
    occupancyMeasures = []

    for iterInd in itersAll:

        iterSWCs = []
        for swc in swcList:

            swcStem = os.path.split(swc)[1][:-4]

            iterSWC = os.path.join(resDir, "{}{}.swc".format(swcStem, iterInd))
            iterSWCs.append(iterSWC)

        occupancyMeasures.append(occupancyEMD(iterSWCs, voxelSize))
    return itersAll, occupancyMeasures





def correctRegMaxSNChoice(parFile, parNames):
    assert os.path.isfile(parFile), "{} not found".format(parFile)

    ch = input('Using parameter File {}.\n Continue?(y/n)'.format(parFile))

    if ch != 'y':
        print('User Abort!')
        sys.exit()

    parsList = parFileCheck(parFile, parNames)

    for pars in parsList:
        refSWC = pars['initRefSWC']
        swcList = pars['swcList']
        fnwrt = pars['finallyNormalizeWRT']

        assert os.path.isfile(refSWC), 'Could  not find {}'.format(refSWC)

        for swc in swcList:
            assert os.path.isfile(swc), 'Could  not find {}'.format(swc)
            assert swc.endswith('.swc'), 'Elements of swcList must be of SWC format with extension \'.swc\''

        assert fnwrt in swcList, 'The parameter finallyNormalizeWRT must be an element of the parameter swcList'


    for pars in parsList:
        refSWC = pars['initRefSWC']
        swcList = pars['swcList']
        fnwrt = pars['finallyNormalizeWRT']
        voxelSizes = pars['gridSizes']
        resDir = pars["resDir"]

        if os.path.isdir(resDir):

            iters, measures = getRegMaxSNIterVsMeasure(resDir=resDir, swcList=swcList, voxelSize=voxelSizes[-1])

            bestIterInd = iters[int(np.argmin(measures))]
            bestMeasure = min(measures)


            ipFiles = []
            opFiles = []
            thrash, fnwrtName = os.path.split(fnwrt[:-4])
            for swc in swcList:
                dirPath, expName = os.path.split(swc[:-4])
                ipFiles.append(os.path.join(resDir, '{}{}.swc'.format(expName, bestIterInd)))
                opFiles.append(os.path.join(resDir, '{}.swc'.format(expName)))
            normalizeFinally(ipFiles, resDir, opFiles, fnwrtName, bestIterInd)

            finalSolFile = os.path.join(resDir, "bestIterInd.json")

            with open(finalSolFile, 'w') as fle:
                json.dump({'finalVal': bestMeasure,
                           'bestIteration': bestIterInd}, fle)

if __name__ == "__main__":

    assert len(sys.argv) == 2, "Improper usage! Please use as: \n " \
                               "python {} <Reg-MaxS-N Par File>".format(sys.argv[1])


    correctRegMaxSNChoice(sys.argv[1], RegMaxSNParNames)