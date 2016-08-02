import os
import numpy as np
from RegMaxSCore.iterativeRegistration import IterativeRegistration, composeRefSWC, calcOverlap
import shutil
import json
import sys
from RegMaxSCore.transforms import decompose_matrix

homeFolder = os.path.expanduser('~')


def getRemainderScale(scale, oldScale):

    toReturn = []
    for s, oldS in zip(scale, oldScale):

        toReturn.append([min(oldS[0] / s, 1), max(oldS[1] / s, 1)])

    return toReturn

# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1/'
#
# expNames = [
#                 'HB130313-4',
#                 'HB130322-1',
#                 'HB130326-2',
#                 'HB130408-1',
#                 'HB130425-1',
#                 'HB130501-2',
#                 'HB130705-1',
#                 'HB140424-1',
#                 'HB130523-3',
#                 'HB130605-1',
#                 'HB130605-2',
#                 'HB140701-1',
#                 'HB140813-3',
#                 'HB140917-1',
#                 'HB140930-1',
#                 'HB141030-1',
#               ]
#
# refInd = 4
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1/'


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1_Foragers/'
#
# expNames = [
#                 'HB130313-4',
#                 'HB130322-1',
#                 'HB130326-2',
#                 'HB130408-1',
#                 'HB130425-1',
#                 'HB130501-2',
#                 'HB130705-1',
#                 'HB140424-1',
#               ]
#
# refInd = 7
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Foragers/'



# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1_NE/'
#
# expNames = [
#
#                 'HB130523-3',
#                 'HB130605-1',
#                 'HB130605-2',
#                 # 'HB140701-1',
#                 'HB140813-3',
#                 'HB140917-1',
#                 'HB140930-1',
#                 'HB141030-1',
#               ]
#
# refInd = 3
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_NE/'


# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/Tests'
# # dirPath = 'tmp'
# expNames = [
#             'HB130313-4',
#             'HB130313-4RandTrans',
#             'HB130313-4RandTrans1',
#             'HB130313-4RandTrans2',
#             'HB130313-4RandTrans3',
#             'HB130313-4RandTrans4',
#             'HB130313-4RandTrans5',
#             'HB130313-4RandTrans6',
#             'HB130313-4RandTrans7',
#             'HB130313-4RandTrans8',
#             'HB130313-4RandTrans9',
#             # 'HB130313-4NoiseStd1RandTrans',
#             # 'HB130313-4NoiseStd2RandTrans',
#             # 'HB130313-4NoiseStd3RandTrans',
#             # 'HB130313-4NoiseStd4RandTrans',
#             # 'HB130313-4NoiseStd5RandTrans',
#             # 'HB130313-4NoiseStd6RandTrans',
#             # 'HB130313-4NoiseStd7RandTrans',
#             # 'HB130313-4NoiseStd8RandTrans',
#             # 'HB130313-4NoiseStd9RandTrans',
#
#
#             # 'HSN-fluoro01.CNG',
#             # 'HSN-fluoro01.CNGRandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd1RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd2RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd3RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd4RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd5RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd6RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd7RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd8RandTrans',
#             # 'HSN-fluoro01.CNGNoiseStd9RandTrans',
#             ]
#
# #
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/Tests/'
# # resDir = 'tmp/directPixelBased'

# ----------------------------------------------------------------------------------------------------------------------


# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/peng/'
#
# expNames = [
#             'C150.CNG',
#             # 'C155.CNG',
#             # 'C158.CNG',
#             'C159.CNG',
#             # 'C160.CNG',
#             # 'C168.CNG',
#             # 'C169.CNG',
#             # 'C171.CNG',
#             # 'C175.CNG',
#             # 'C180.CNG',
#             # 'C200.CNG',
#             # 'C201.CNG',
#             ]
#
#
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/peng/'

# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSNR/'
# #
# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
#
#
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSNR/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSNL/'
# #
# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
#
#
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSNL/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSN/'
# #
# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro09.CNG',
#             ]
#
#
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSN/'


# ----------------------------------------------------------------------------------------------------------------------
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSE/'
#
# expNames = [
#             'HSE-fluoro01.CNG',
#             'HSE-fluoro03.CNG',
#             'HSE-fluoro05.CNG',
#             'HSE-fluoro07.CNG',
#             'HSE-fluoro09.CNG',
#             'HSE-fluoro10.CNG',
#             'HSE-fluoro15.CNG',
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSE/'


# ----------------------------------------------------------------------------------------------------------------------


# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/Mustaparta_Lofaldi'
#
# expNames = [
#             'Nevron-komplett-08-02-28-2a.CNG',
#             'Nevron-komplett-08-03-13-2a.CNG',
#             'Nevron-komplett-08-08-28-1a-A.CNG',
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/Mustaparta_Lofaldi/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/sztarkerLGMD/'
#
# expNames = [
#             '1st-instar-LGMD1.CNG',
#             '2nd-instar-LGMD1.CNG',
#             '3rd-instar-LGMD1.CNG',
#             '4th-instar-LGMD1.CNG',
#             '5th-instar-LGMD1.CNG',
#
#             # '1st-instar-LGMD2.CNG',
#             # '2nd-instar-LGMD2.CNG',
#             # '3rd-instar-LGMD2.CNG',
#             # '4th-instar-LGMD2.CNG',
#             # '5th-instar-LGMD2.CNG',
#             ]
# refInd = 4
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/sztarkerLGMD/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/ChalupaRGCBi'
# expNames = [
#             'cell-116-trace.CNG',
#             'cell-122-trace.CNG',
#             'cell-126-trace.CNG',
#             'cell-129-trace.CNG',
#
#             'cell-213-trace.CNG',
#             'cell-123-trace.CNG',
#             'cell-188-trace.CNG',
#             'cell-169-trace.CNG',
#
#             'cell-177-trace.CNG',
#             'cell-183-trace.CNG',
#             'cell-206-trace.CNG',
#             'cell-232-trace.CNG',
#
#             ]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/ChalupaRGCBi'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/JefferisvPN'
# expNames = [
#             'JBF3LLHSKELETON.CNG',  #0
#             'WKA7L.CNG',            #0.6758241758241759
#             'JBD2LLHskeleton.CNG',  #0.6029411764705883
#             'LHD1RLHSKELETON.CNG',  #0.6386138613861386
#
#             # 'KLA2L.CNG',            #0.8031914893617021
#             # 'LBE4R.CNG',            #0.8305084745762712
#             # 'LLA2RLHSKELETON.CNG',  #0.7555555555555555
#             # 'NBA8L.CNG',            #0.7531914893617021
#             # 'NCB7L.CNG',            #0.746031746031746
#             # 'JCB4LLHSKELETON.CNG',  #0.7552742616033755
#             #
#             # 'LHA3LLHskeleton.CNG',  #0.7837837837837838
#             # 'LHE7LLHskeleton.CNG',  #0.7559808612440191
#             # 'UQB5R.CNG',            #0.7362637362637363
#             # 'LHD6RLHSKELETON.CNG',  #0.7743589743589744
#             # 'LHD6LHskeleton.CNG',   #0.84375
#             #
#             # 'LHA5LLHSKELETON.CNG',  #0.856353591160221
#             # 'UQB5L.CNG',            #0.827906976744186
#             ]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/JefferisvPN'


# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/ChiangRAL/'
#
# expNames = [
#                 'Trh-F-700063803.CNG',
#                 'Trh-F-500154803.CNG',
#                 'Trh-F-600071803.CNG',
#                 'Trh-F-500050803.CNG',
#                 'Trh-F-500093803.CNG',
#                 'Trh-F-700018803.CNG',
#                 'Trh-M-500051803.CNG',
#                 'Trh-F-500148803.CNG',
#                 'Trh-F-500106803.CNG',
#                 'fru-F-500008803.CNG',
#
#                 'Trh-F-500188804.CNG',
#                 'fru-M-100085804.CNG',
#                 'Trh-F-500010804.CNG',
#                 'fru-M-200080804.CNG',
#                 'Trh-F-000018804.CNG',
#                 'fru-M-100090804.CNG',
#                 'Trh-M-100056804.CNG',
#                 'Trh-F-600083804.CNG',
#                 'Trh-M-400048804.CNG',
#                 'Trh-M-900048804.CNG',
#
#                 'Trh-F-600102801.CNG',
#                 'Trh-M-600091801.CNG',
#                 'Trh-F-600074801.CNG',
#                 'Trh-F-300082801.CNG',
#                 'Trh-F-600093801.CNG',
#                 'Trh-M-600089801.CNG',
#                 'Trh-M-500058801.CNG',
#                 'Trh-F-600085801.CNG',
#                 'Trh-M-600010801.CNG',
#                 'Trh-M-600074801.CNG',
#             ]
#
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/ChiangRAL'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [x[:-4] for x in os.listdir(dirPath) if x.endswith('.swc')]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLALInt'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLACC/'
#
# expNames = [
#             'fru-M-100030.CNG',
#             'fru-M-700043.CNG',
#             'VGlut-F-000600.CNG',
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLACC/'


# ----------------------------------------------------------------------------------------------------------------------

dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOPSInt/'
expNames = [
            'Trh-F-000047_registered',
            'Trh-F-000047.CNG',
            'Trh-M-000143.CNG',
            'Trh-F-000092.CNG',
            'Trh-F-700009.CNG',
            'Trh-M-000013.CNG',
            'Trh-M-000146.CNG',
            # 'Trh-M-100009.CNG',
            'Trh-F-000019.CNG',
            'Trh-M-000081.CNG',
            'Trh-M-900003.CNG',
            'Trh-F-200035.CNG',
            'Trh-F-200015.CNG',
            'Trh-M-000040.CNG',
            'Trh-M-600023.CNG',
            'Trh-M-100048.CNG',
            'Trh-M-700019.CNG',
            'Trh-F-100009.CNG',
            'Trh-M-400000.CNG',
            'Trh-M-000067.CNG',
            'Trh-M-000114.CNG',
            'Trh-M-100018.CNG',
            'Trh-M-000141.CNG',
            'Trh-M-900019.CNG',
            'Trh-M-800002.CNG'
]
refInd = 0
resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOPSInt/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOMB/'
# expNames = [
# 'VGlut-F-500085_registered',
#  'VGlut-F-700500.CNG',
#  'VGlut-F-700567.CNG',
#  'VGlut-F-500471.CNG',
#  'Cha-F-000353.CNG',
#  'VGlut-F-600253.CNG',
#  'VGlut-F-400434.CNG',
#  'VGlut-F-600379.CNG',
#  'VGlut-F-700558.CNG',
#  'VGlut-F-500183.CNG',
#  'VGlut-F-300628.CNG',
#  'VGlut-F-500085.CNG',
#  'VGlut-F-500031.CNG',
#  'VGlut-F-500852.CNG',
#  'VGlut-F-600366.CNG'
#             ]
#
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOMB/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLLC/'
# expNames = [
#             'Gad1-F-000062_Standardized',
#             'Gad1-F-000062.CNG',
#             'Cha-F-000012.CNG',
#             'Cha-F-300331.CNG',
#             'Gad1-F-600000.CNG',
#             'Cha-F-000018.CNG',
#             'Cha-F-300051.CNG',
#             'Cha-F-400051.CNG',
#             'Cha-F-200000.CNG'
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLLC/'
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




