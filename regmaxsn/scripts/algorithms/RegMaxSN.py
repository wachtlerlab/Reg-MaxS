import os
import numpy as np
from regmaxsn.core.iterativeRegistration import IterativeRegistration, composeRefSWC, calcOverlap, getRemainderScale
import shutil
import json
import sys
from regmaxsn.core.transforms import decompose_matrix
from regmaxsn.core.swcFuncs import transSWC
from regmaxsn.core.misc import parFileCheck
from regmaxsn.core.occupancyBasedMeasure import occupancyEMD

def normalizeFinally(ipFiles, resDir, opFiles, fnwrtName, maxIter):


    itersAll = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') == 0])

    iters = [x for x in itersAll if x <= maxIter]

    totalTrans = np.eye(4)

    for iter in iters:

        solFle = os.path.join(resDir, fnwrtName + str(iter) + 'Sol.txt')

        if os.path.exists(solFle):
            with open(solFle, 'r') as f:
                pars = json.load(f)
                totalTrans = np.dot(pars['finalTransMat'], totalTrans)


    iTrans = np.linalg.inv(totalTrans)

    for ipFile, opFile in zip(ipFiles, opFiles):

        transSWC(ipFile, iTrans[:3, :3], iTrans[:3, 3], opFile)

        ipDir, ipName = os.path.split(ipFile[:-4])
        partsDir = os.path.join(ipDir, ipName)

        if os.path.isdir(partsDir):

            normedPartsDir = opFile[:-4]
            os.mkdir(normedPartsDir)
            swcs = [x for x in os.listdir(partsDir) if x.endswith('.swc')]
            for swc in swcs:
                opPart = os.path.join(normedPartsDir, swc)
                ipPart = os.path.join(partsDir, swc)
                transSWC(ipPart, iTrans[:3, :3], iTrans[:3, 3], opPart)


def runRegMaxSN(parFile, parNames):

    assert os.path.isfile(parFile), "{} not found".format(parFile)

    ch = input('Using parameter File {}.\n Continue?(y/n)'.format(parFile))

    if ch != 'y':
        print('User Abort!')
        sys.exit()

    parsList = parFileCheck(parFile, parNames)

    for pars in parsList:
        resDir = pars['resDir']
        refSWC = pars['initRefSWC']
        swcList = pars['swcList']
        fnwrt = pars['finallyNormalizeWRT']

        if os.path.isdir(resDir):

            ch = input('Folder exists: ' + resDir + '\nDelete(y/n)?')
            if ch == 'y':
                shutil.rmtree(resDir)
            else:
                quit()
        try:
            os.mkdir(resDir)
        except Exception as e:
            raise IOError

        assert os.path.isfile(refSWC), 'Could  not find {}'.format(refSWC)

        for swc in swcList:
            assert os.path.isfile(swc), 'Could  not find {}'.format(swc)
            assert swc.endswith('.swc'), 'Elements of swcList must be of SWC format with extension \'.swc\''

        assert fnwrt in swcList, 'The parameter finallyNormalizeWRT must be an element of the parameter swcList'

    print('All parameters are acceptable. Starting the Reg-MaxS-N jobs...')

    for parInd, pars in enumerate(parsList):

        print(('Starting Job # {}'.format(parInd + 1)))

        print('Current Parameters:')
        for parN, parV in pars.items():
            print(('{}: {}'.format(parN, parV)))

        resDir = pars['resDir']
        refSWC = pars['initRefSWC']
        swcList = pars['swcList']
        fnwrt = pars['finallyNormalizeWRT']
        usePartsDir = pars['usePartsDir']
        nIter = pars['maxIter']
        gridSizes = pars['gridSizes']
        rotBounds = pars['rotBounds']
        transBounds = pars['transBounds']
        scaleBounds = pars['scaleBounds']
        transMinRes = pars['transMinRes']
        minScaleStepSize = pars['minScaleStepSize']
        rotMinRes = pars['rotMinRes']
        nCPU = pars['nCPU']

        shutil.copyfile(refSWC, os.path.join(resDir, 'ref' + str(-1) + '.swc'))

        if usePartsDir:
            for swc in swcList:
                dirPath, expName = os.path.split(swc[:-4])
                partsDirO = os.path.join(dirPath, expName)
                if os.path.isdir(partsDirO):
                    partsDirD = os.path.join(resDir, expName + str(-1))
                    shutil.copytree(partsDirO, partsDirD)

        prevAlignedSWCs = swcList

        occupancyMeasureLargestGridSize = []
        bestIterInd = nIter - 1

        nrnScaleBounds = {swc: scaleBounds[:] for swc in swcList}

        for iterInd in range(nIter):

            iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                        transMinRes, minScaleStepSize, rotMinRes, nCPU)

            presAlignedSWCs = []
            dones = []
            for swcInd, swc in enumerate(swcList):
                dirPath, expName = os.path.split(swc[:-4])

                print(('Doing Iter ' + str(iterInd) + ' : ' + expName))

                SWC2Align = prevAlignedSWCs[swcInd]

                if iterInd > 0:
                    initGuessTypeT = 'nothing'
                else:
                    initGuessTypeT = 'just_centroids'

                initVals = [calcOverlap(refSWC, SWC2Align, g) for g in gridSizes]

                if usePartsDir:
                    inPartsDir = os.path.join(resDir, expName + str(iterInd - 1))
                    outPartsDir = os.path.join(resDir, expName + str(iterInd))
                else:
                    inPartsDir = None
                    outPartsDir = None

                resFile = os.path.join(resDir, expName + str(iterInd) + '.swc')
                resSWC, resSol = iterReg.performReg(SWC2Align, resFile,
                                                    scaleBounds=nrnScaleBounds[swc],
                                                    inPartsDir=inPartsDir,
                                                    outPartsDir=outPartsDir,
                                                    initGuessType=initGuessTypeT,
                                                    retainTempFiles=True)

                finalVals = [calcOverlap(refSWC, resSWC, gridSize) for gridSize in gridSizes]

                considerIteration = False

                for iv, fv in zip(initVals, finalVals):

                    if fv < iv:
                        considerIteration = True
                        break

                    if fv > iv:
                        considerIteration = False
                        break

                if not considerIteration:

                    shutil.copy(SWC2Align, resSWC)
                    shutil.rmtree(os.path.join(resDir, expName + str(iterInd) + 'trans'))
                    if usePartsDir and os.path.exists(outPartsDir):
                        shutil.rmtree(outPartsDir)
                        shutil.copytree(inPartsDir, outPartsDir)
                    os.remove(resSol)
                    print(('finalVal (' + str(finalVals) + ') >= initVal (' + str(initVals) + '). Doing Nothing!'))
                    done = True
                else:
                    print(('finalVal (' + str(finalVals) + ') < initVal (' + str(initVals) + '). Keeping the iteration!'))
                    with open(resSol, 'r') as fle:
                        pars = json.load(fle)
                        totalTrans = np.array(pars['finalTransMat'])
                        done = np.allclose(np.eye(3), totalTrans[:3, :3], atol=1e-3)

                        scale, shear, angles, trans, persp = decompose_matrix(totalTrans)
                        nrnScaleBounds[swc] = getRemainderScale(scale, nrnScaleBounds[swc])
                dones.append(done)
                print(('Finished ' + expName + ' : ' + str(done)))

                print(('Remainder scale: ' + str(nrnScaleBounds[swc])))
                presAlignedSWCs.append(resSWC)


            newRefSWC = os.path.join(resDir, 'ref' + str(iterInd) + '.swc')
            overallOverlap = composeRefSWC(presAlignedSWCs, newRefSWC, gridSizes[-1])
            occupancyMeasure = occupancyEMD(presAlignedSWCs, gridSizes[-1])
            occupancyMeasureLargestGridSize.append(occupancyMeasure)
            refSWC = newRefSWC

            prevAlignedSWCs = presAlignedSWCs

            if all(dones):

                break

        bestIterInd = np.argmin(occupancyMeasureLargestGridSize)
        bestMeasure = min(occupancyMeasureLargestGridSize)

        shutil.copy(os.path.join(resDir, 'ref' + str(bestIterInd) + '.swc'), os.path.join(resDir, 'finalRef.swc'))

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
                       'bestIteration': int(bestIterInd)}, fle)

        print(('Finished Job # {}'.format(parInd + 1)))


if __name__ == '__main__':

    from regmaxsn.core.RegMaxSPars import RegMaxSNParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python RegMaxSN.py parFile\''

    parFile = sys.argv[1]

    runRegMaxSN(parFile, RegMaxSNParNames)

