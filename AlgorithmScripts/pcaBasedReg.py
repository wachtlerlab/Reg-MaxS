import os
from RegMaxSCore.swcFuncs import transSWC, getPCADetails, transSWC_rotAboutPoint
from RegMaxSCore.SWCTransforms import objFun, SWCTranslate
from RegMaxSCore.misc import parFileCheck
import json
import numpy as np
import sys


def pca_based(parFile):

    ch = raw_input('Using parameter File {}.\n Continue?(y/n)'.format(parFile))

    if ch != 'y':
        print('User Abort!')
        sys.exit()

    from RegMaxSCore.RegMaxSPars import pcaBasedParNames
    parsList = parFileCheck(parFile, pcaBasedParNames)

    for parInd, pars in enumerate(parsList):

        print('Current Parameters:')
        for parN, parV in pars.iteritems():
            print('{}: {}'.format(parN, parV))

        refSWC = pars['refSWC']
        testSWC = pars['testSWC']
        gridSizes = pars['gridSizes']
        resFile = pars['resFile']
        usePartsDir = pars['usePartsDir']

        resDir, expName = os.path.split(resFile[:-4])

        resSolFile = os.path.join(resDir, expName + 'bestSol.txt')

        refPts = np.loadtxt(refSWC)[:, 2:5]
        refMean = refPts.mean(axis=0)
        SWC2AlignPts = np.loadtxt(testSWC)[:, 2:5]
        SWC2AlignMean = SWC2AlignPts.mean(axis=0)

        refEvecs, refNStds = getPCADetails(refSWC)
        STAEvecs, STANStds = getPCADetails(testSWC)

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

        transSWC(testSWC, totalTransform[:3, :3], totalTransform[:3, 3], resFile)

        trans = SWCTranslate(refSWC, resFile, gridSizes[-1])
        bestVal = objFun(([0, 0, 0], trans))

        if usePartsDir:

            inPartsDir = testSWC[:-4]
            if os.path.isdir(inPartsDir):

                dirList = os.listdir(inPartsDir)
                dirList = [x for x in dirList if x.endswith('.swc')]

                outPartsDir = resFile[:-4]
                if not os.path.isdir(outPartsDir):
                    os.mkdir(outPartsDir)

                for entry in dirList:
                    transSWC_rotAboutPoint(os.path.join(inPartsDir, entry),
                                           totalTransform[:3, :3], totalTransform[:3, 3],
                                           os.path.join(outPartsDir, entry),
                                           [0, 0, 0]
                                           )

            else:
                print('Specified partsDir {} not found'.format(inPartsDir))

        with open(resSolFile, 'w') as fle:
            json.dump({'transMat': totalTransform.tolist(), 'bestVal': bestVal,
                       'refSWC': refSWC, 'testSWC': testSWC, 'gridSizes': gridSizes}, fle)


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python pcaBasedReg.py parFile\''

    parFile = sys.argv[1]

    pca_based(parFile)



