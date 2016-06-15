import os
import numpy as np
import json
from RegMaxSCore.swcFuncs import transSWC

homeFolder = os.path.expanduser('~')

# ----------------------------------------------------------------------------------------------------------------------
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOMB/'
# expNames = [
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
# # refInd = 12
# # resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOMB/'
#
# # refInd = 2
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB3/'
#
# refInd = 6
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB4/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOPSInt/'
# expNames = [
#             'Trh-F-000047.CNG',
#             'Trh-M-000143.CNG',
#             'Trh-F-000092.CNG',
#             'Trh-F-700009.CNG',
#             'Trh-M-000013.CNG',
#             'Trh-M-000146.CNG',
#             # 'Trh-M-100009.CNG',
#             'Trh-F-000019.CNG',
#             'Trh-M-000081.CNG',
#             'Trh-M-900003.CNG',
#             'Trh-F-200035.CNG',
#             'Trh-F-200015.CNG',
#             'Trh-M-000040.CNG',
#             'Trh-M-600023.CNG',
#             'Trh-M-100048.CNG',
#             'Trh-M-700019.CNG',
#             'Trh-F-100009.CNG',
#             'Trh-M-400000.CNG',
#             'Trh-M-000067.CNG',
#             'Trh-M-000114.CNG',
#             'Trh-M-100018.CNG',
#             'Trh-M-000141.CNG',
#             'Trh-M-900019.CNG',
#             'Trh-M-800002.CNG'
# ]
# # refInd = 12
# # resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOPSInt/'
#
# # refInd = 12
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt4_newXRev/'
#
# # refInd = 0
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt3_newXRev/'
#
# refInd = 17
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt5_newXRev/'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [x[:-4] for x in os.listdir(dirPath) if x.endswith('.swc')]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLALInt'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLLC/'
# expNames = [
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
# # refInd = 4
# refInd = 7
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Foragers/'



# ----------------------------------------------------------------------------------------------------------------------
#
dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1_NE/'

expNames = [

                'HB130523-3',
                'HB130605-1',
                'HB130605-2',
                # 'HB140701-1',
                'HB140813-3',
                'HB140917-1',
                'HB140930-1',
                'HB141030-1',
              ]

# refInd = 1
refInd = 3
resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_NE/'


# ----------------------------------------------------------------------------------------------------------------------

refName = expNames[refInd]

iters = sorted([int(fle[3:-4]) for fle in os.listdir(resDir) if fle.find('ref') >= 0])

totalTrans = np.eye(4)

for iter in iters:

    solFle = os.path.join(resDir, refName + str(iter) + 'Sol.txt')

    if os.path.isfile(solFle):

        with open(solFle, 'r') as f:
            pars = json.load(f)
            totalTrans = np.dot(pars['finalTransMat'], totalTrans)

iTrans = np.linalg.inv(totalTrans)

for expName in expNames:

    ipFile = os.path.join(resDir, expName + '.swc')
    opFile = os.path.join(resDir, expName + '_norm.swc')
    transSWC(ipFile, iTrans[:3, :3], iTrans[:3, 3], opFile)

    partsDir = os.path.join(resDir, expName)

    if os.path.isdir(partsDir):

        normedPartsDir = partsDir + '_norm'
        os.mkdir(normedPartsDir)
        swcs = [x for x in os.listdir(partsDir) if x.endswith('.swc')]
        for swc in swcs:
            opPart = os.path.join(normedPartsDir, expName + swc[len(expName):-4] + '_norm.swc')
            ipPart = os.path.join(partsDir, swc)
            transSWC(ipPart, iTrans[:3, :3], iTrans[:3, 3], opPart)


