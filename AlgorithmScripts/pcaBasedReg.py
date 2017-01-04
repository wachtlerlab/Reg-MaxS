import os
from RegMaxSCore.swcFuncs import transSWC, getPCADetails
from RegMaxSCore.SWCTransforms import objFun, SWCTranslate
import json
import numpy as np
import sys


def pca_based(parFile, parNames):

    ch = raw_input('Using parameter File {}.\n Continue?(y/n)'.format(parFile))

    if ch != 'y':
        print('User Abort!')
        sys.exit()

    with open(parFile, 'r') as fle:
        parsList = json.load(fle)
        assert type(parsList) == list, 'Parameter file {} ' \
                                       'does not contain a list of ' \
                                       'dictionaries as is the requirement'.format(parFile)
        for parInd, par in enumerate(parsList):
            assert type(par) == dict, 'Parameter set # {} in {} not a list'.format(parInd, parFile)

            for pn in parNames:
                assert pn in par, 'Parameter {} not found in ' \
                                  'parameter set # {} of {}'.format(pn, parInd, parFile)

    for parInd, pars in enumerate(parsList):

        print('Current Parameters:')
        for parN, parV in pars.iteritems():
            print('{}: {}'.format(parN, parV))

        refSWC = pars['refSWC']
        SWC2Align = pars['testSWC']
        gridSizes = pars['gridSizes']
        resFile = pars['resFile']
        resDir, expName = os.path.split(resFile[:-4])

        resSolFile = os.path.join(resDir, expName + 'bestSol.txt')

        refPts = np.loadtxt(refSWC)[:, 2:5]
        refMean = refPts.mean(axis=0)
        SWC2AlignPts = np.loadtxt(SWC2Align)[:, 2:5]
        SWC2AlignMean = SWC2AlignPts.mean(axis=0)

        refEvecs, refNStds = getPCADetails(refSWC)
        STAEvecs, STANStds = getPCADetails(SWC2Align)

        scales = [x / y for x, y in zip(refNStds, STANStds)]

        totalTransform = np.eye(4)
        totalTransform[:3, 3] = -SWC2AlignMean

        temp = np.eye(4)
        temp[:3, :3] = STAEvecs.T
        totalTransform = np.dot(temp, totalTransform)

        temp = np.eye(4)
        temp[:3, :3] = np.diag(scales)
        totalTransform = np.dot(temp, totalTransform)

        temp = np.eye(4)
        temp[:3, :3] = refEvecs
        totalTransform = np.dot(temp, totalTransform)

        totalTranslation = refMean

        totalTransform[:3, 3] += totalTranslation

        transSWC(SWC2Align, totalTransform[:3, :3], totalTransform[:3, 3], resFile)

        trans = SWCTranslate(refSWC, resFile, gridSizes[-1])
        bestVal = objFun(([0, 0, 0], trans))

        with open(resSolFile, 'w') as fle:
            json.dump({'transMat': totalTransform.tolist(), 'bestVal': bestVal,
                       'refSWC': refSWC, 'testSWC': SWC2Align, 'gridSizes': gridSizes}, fle)


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    from RegMaxSCore.RegMaxSPars import pcaBasedParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python pcaBasedReg.py parFile\''

    parFile = sys.argv[1]

    pca_based(parFile, pcaBasedParNames)



