import os
import numpy as np
from RegMaxSCore.iterativeRegistration import IterativeRegistration, composeRefSWC, calcOverlap, getRemainderScale
import shutil
import json
import sys
from RegMaxSCore.transforms import decompose_matrix


# ----------------------------------------------------------------------------------------------------------------------
dirPath = 'TestFiles'
expNames = [
            'Gad1-F-000062.CNG',
            'Cha-F-000012.CNG',
            'Cha-F-300331.CNG',
            'Gad1-F-600000.CNG',
            'Cha-F-000018.CNG',
            'Cha-F-300051.CNG',
            'Cha-F-400051.CNG',
            'Cha-F-200000.CNG'
            ]
refInd = 0
resDir = os.path.join('Results', 'Reg-MaxS-N')
# ----------------------------------------------------------------------------------------------------------------------

gridSizes = [40.0, 20.0, 10.0]
# gridSizes = [20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
scaleBounds = [[0.75, 1 / 0.75], [0.75, 1 / 0.75], [0.75, 1 / 0.75]]
minScaleStepSize = 1.005
nCPU = 6
nIter = 100

usePartsDir = True
# usePartsDir = False
# ----------------------------------------------------------------------------------------------------------------------

ch = raw_input('Checked params? Continue?(y/n)')

if ch != 'y':
    sys.exit()

if os.path.isdir(resDir):

    ch = raw_input('Folder exists: ' + resDir + '\nDelete(y/n)?')
    if ch == 'y':
        shutil.rmtree(resDir)
    else:
        quit()

os.mkdir(resDir)

refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
shutil.copyfile(refSWC, os.path.join(resDir, 'ref' + str(-1) + '.swc'))

if usePartsDir:
    for expName in expNames:
        partsDirO = os.path.join(dirPath, expName)
        if os.path.isdir(partsDirO):
            partsDirD = os.path.join(resDir, expName + str(-1))
            shutil.copytree(partsDirO, partsDirD)

prevAlignedSWCs = [os.path.join(dirPath, expName + '.swc') for expName in expNames]

overallOverlaps = []
bestInd = nIter

nrnScaleBounds = {k: scaleBounds for k in expNames}

for iterInd in range(nIter):

    iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                transMinRes, minScaleStepSize, rotMinRes, nCPU)

    presAlignedSWCs = []
    dones = []
    for expInd, expName in enumerate(expNames):

        partsDirO = os.path.join(dirPath, expName)

        print('Doing Iter ' + str(iterInd) + ' : ' + expName)

        SWC2Align = prevAlignedSWCs[expInd]

        if iterInd > 0:
            initGuessTypeT = 'nothing'
        else:
            initGuessTypeT = 'just_centroids'


        initVals = [calcOverlap(refSWC, SWC2Align, g) for g in gridSizes]

        if usePartsDir:
            prevPartsDir = os.path.join(resDir, expName + str(iterInd - 1))
        else:
            prevPartsDir = None

        resSWC, resSol = iterReg.performReg(SWC2Align, expName + str(iterInd),
                                            scaleBounds=nrnScaleBounds[expName],
                                            partsDir=prevPartsDir,
                                            resDir=resDir, initGuessType=initGuessTypeT)

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
            newPartsDir = os.path.join(resDir, expName + str(iterInd))
            if usePartsDir and os.path.exists(newPartsDir):
                shutil.rmtree(newPartsDir)
                shutil.copytree(prevPartsDir, newPartsDir)
            os.remove(resSol)
            print('finalVal (' + str(finalVals) + ') >= initVal (' + str(initVals) + '). Doing Nothing!')
            done = True
        else:
            print('finalVal (' + str(finalVals) + ') < initVal (' + str(initVals) + '). Keeping the iteration!')
            with open(resSol, 'r') as fle:
                pars = json.load(fle)
                totalTrans = np.array(pars['finalTransMat'])
                done = np.allclose(np.eye(3), totalTrans[:3, :3], atol=1e-3)

                scale, shear, angles, trans, persp = decompose_matrix(totalTrans)
                nrnScaleBounds[expName] = getRemainderScale(scale, nrnScaleBounds[expName])
        dones.append(done)
        print('Finished ' + expName + ' : ' + str(done))

        print('Remainder scale: ' + str(nrnScaleBounds[expName]))
        presAlignedSWCs.append(resSWC)


    newRefSWC = os.path.join(resDir, 'ref' + str(iterInd) + '.swc')
    overallOverlap = composeRefSWC(presAlignedSWCs, newRefSWC, gridSizes[-1])
    overallOverlaps.append(overallOverlap)
    refSWC = newRefSWC

    prevAlignedSWCs = presAlignedSWCs

    if all(dones):

        bestInd = iterInd
        break

    else:
        bestInd = None


if bestInd is None:
    bestInd = np.argmin(overallOverlaps)

for expName in expNames:
    shutil.copy(os.path.join(resDir, expName + str(bestInd) + '.swc'),
                os.path.join(resDir, expName + '.swc'))
    shutil.copy(os.path.join(resDir, 'ref' + str(bestInd) + '.swc'), os.path.join(resDir, 'finalRef.swc'))
    bestPartsDir = os.path.join(resDir, expName + str(bestInd))
    if usePartsDir and os.path.isdir(bestPartsDir):
        shutil.copytree(bestPartsDir, os.path.join(resDir, expName))




