import os
from RegMaxSCore.plotDensities import DensityVizualizations, writeTIFF
import numpy as np
from matplotlib import pyplot as plt
homeFolder = os.path.expanduser('~')

part = ''

#-------------------------------------------------------------------------------------------------------------------

# expNames = [
#                 'HB130523-3',
#                 'HB130605-1',
#                 'HB130605-2',
#                 'HB140813-3',
#                 'HB140917-1',
#                 'HB140930-1',
#                 'HB141030-1',
#               ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1/'
#
# gridUnitSize = 0.5
# extraDialiation = 5
#
# label = 'NewlyEmerged'
# # part = '-VB'
# part = '-DB'
#
#


#-------------------------------------------------------------------------------------------------------------------


# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/DL-Int-1_Foragers/'
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
# refInd = 4
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Foragers/'
#
# gridUnitSize = 1
# extraDialiation = 8
# resampleLen = 0.5
#
# label = 'Foragers'
# # part = '-VB'
# part = '-DB'
# # part = ''
#
#
#-------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-2/')
# expNames = [
#             'HB121224-1-WNC10S10x20',
#             'HB121224-1-WNC10S10x40',
#             ]
# refInd = 0
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/DL-Int-2/')

#-------------------------------------------------------------------------------------------------------------------

# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSNR/'
# gridUnitSize = 1
# extraDialiation = 6
#
# label = 'HSNR'
# part = ''
#-------------------------------------------------------------------------------------------------------------------

# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSNR/'
# gridUnitSize = 1
# extraDialiation = 6
#
# label = 'HSNR'
# part = ''
# #-------------------------------------------------------------------------------------------------------------------

# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSNL/'
# gridUnitSize = 1
# extraDialiation = 6
#
# label = 'HSNL'
# part = ''

#-------------------------------------------------------------------------------------------------------------------

# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSNL/'
# gridUnitSize = 1
# extraDialiation = 11

#-------------------------------------------------------------------------------------------------------------------
# expNames = [
#             'HSE-fluoro01.CNG',
#             'HSE-fluoro03.CNG',
#             'HSE-fluoro05.CNG',
#             'HSE-fluoro07.CNG',
#             'HSE-fluoro09.CNG',
#             'HSE-fluoro10.CNG',
#             'HSE-fluoro15.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/borstHSE/'
# gridUnitSize = 0.5
# extraDialiation = 5

#-------------------------------------------------------------------------------------------------------------------


# expNames = [
#             'HSE-fluoro01.CNG',
#             'HSE-fluoro03.CNG',
#             'HSE-fluoro05.CNG',
#             'HSE-fluoro07.CNG',
#             'HSE-fluoro09.CNG',
#             'HSE-fluoro10.CNG',
#             'HSE-fluoro15.CNG',
#             ]
#
# resDir = homeFolder + '/DataAndResults/morphology/OriginalData/borstHSE/'
# gridUnitSize = 0.5
# extraDialiation = 5

#-------------------------------------------------------------------------------------------------------------------

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
# gridUnitSize = 0.5
# extraDialiation = 3
#
# # label = 'vVL1-orig'
# label = 'vVL1-JBF3LLHSKELETON.CNG-aligned'
# # label = 'vVL1-orig'
# # label = 'vVL1-orig'
# part = ''
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/JefferisvPN'

# ----------------------------------------------------------------------------------------------------------------------


# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [x[:-4] for x in os.listdir(dirPath) if x.endswith('.swc')]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLALInt'
# refInd = 0
#
# gridUnitSize = 2
# extraDialiation = 11
#
# # label = 'LALInt-' + expNames[refInd] + '-alignPCA'
# label = 'LALInt-' + expNames[refInd] + '-align'
#
# part = ''

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
#
# gridUnitSize = 1
# extraDialiation = 11
#
# label = 'HSN'
#
# part = ''

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
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
#
# gridUnitSize = 1
# extraDialiation = 6
#
# label = 'LACC'
#
# part = ''

# ----------------------------------------------------------------------------------------------------------------------
#
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
#
# # # # refInd = 0
# # # # resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOPSInt/'
# # #
# # # refInd = 0
# # # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt3_newXRev/'
# # #
# # # refInd = 12
# # # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt4_newXRev/'
# #
# # refInd = 17
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOPSInt5_newXRev/'
# #
# # label = 'OPSInt'
# #
# #
# # basicScale = [1, 1, 1]
# # gridUnitSize = 0.25 * np.array(basicScale)
# # sigmas = np.array([1, 1, 1]) * np.array(basicScale)
# # resampleLen = 0.1
# # initTrans = np.diag([1, 1, 1])
# # #
# # # ---------------------------------------------------------------------------------
# #
# # refInd = 0
# # resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangOPSInt/'
# #
# # refInd = 0
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOPSInt3/'
#
# # refInd = 12
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOPSInt4/'
#
# # refInd = 17
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOPSInt5/'
#
# refInd = 14
# resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOPSInt6/'
#
# label = 'OPSIntRefPCA'
#
# gridUnitSize = [0.25] * 3
# sigmas = [1, 1, 1]
# resampleLen = 0.1
# initTrans = np.diag([1, 1, 1])
# #
# # # ---------------------------------------------------------------------------------
# # # resDir = homeFolder + '/DataAndResults/morphology/Registered/chiangOPSInt/'
# # # label = 'OPSInt_Registered'
# # #
# # # gridUnitSize = [0.25] * 3
# # # sigmas = [0.75, 0.75, 0.75]
# # # resampleLen = 0.1
# # # initTrans = np.diag([1, 1, 1])
# # # ---------------------------------------------------------------------------------
# part = '_part0'
# # part = '_part1'
# # part = ''
#
# refSWC = os.path.join(homeFolder, 'DataAndResults/morphology/Registered/chiangOPSInt/', expNames[0] + '.swc')
# ----------------------------------------------------------------------------------------------------------------------

dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOMB/'
expNames = [
 'VGlut-F-700500.CNG',
 'VGlut-F-700567.CNG',
 'VGlut-F-500471.CNG',
 'Cha-F-000353.CNG',
 'VGlut-F-600253.CNG',
 'VGlut-F-400434.CNG',
 'VGlut-F-600379.CNG',
 'VGlut-F-700558.CNG',
 'VGlut-F-500183.CNG',
 'VGlut-F-300628.CNG',
 'VGlut-F-500085.CNG',
 'VGlut-F-500031.CNG',
 'VGlut-F-500852.CNG',
 'VGlut-F-600366.CNG'
            ]

refInd = 10
# ---------------------------------------------------------------------------------
resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangOMB/'
initTrans = np.diag([1, 1, 1])
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB_OneError/'
# initTrans = np.diag([-1, 1, -1])
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB1/'
# initTrans = np.diag([-1, 1, -1])
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB2/'
# initTrans = np.diag([1, 1, -1])
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB3/'
# initTrans = np.diag([1, 1, -1])
# resDir = homeFolder + '/DataAndResults/morphology/Backups/directPixelBased/chiangOMB4/'
# initTrans = np.diag([1, 1, -1])
label = 'OMB'

# basicScale = [2.99398499,  4.58172834,  3.79382382]
basicScale = [1, 1, 1]
gridUnitSize = 0.25 * np.array(basicScale)
sigmas = [1.25] * 3
resampleLen = 0.1

# # ---------------------------------------------------------------------------------
#
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangOMB/'
# initTrans = np.diag([1, 1, 1])
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOMB1/'
# # initTrans = np.diag([-1, 1, -1])
# # resDir = homeFolder + '/DataAndResults/morphology/Backups/RefPCA/chiangOMB2/'
# # initTrans = np.diag([1, 1, -1])
# label = 'OMBRefPCA'
# basicScale = [1, 1, 1]
# gridUnitSize = [0.25] * 3
# sigmas = [1.25] * 3
# resampleLen = 0.1

#---------------------------------------------------------------------------------
# resDir = homeFolder + '/DataAndResults/morphology/Registered/chiangOMB/'
# label = 'OMB_Registered'
#
# basicScale = [1, 1, 1]
# gridUnitSize = [0.25] * 3
# sigmas = [0.75, 0.75, 0.75]
# resampleLen = 0.1
# initTrans = np.diag([1, 1, 1])
# ---------------------------------------------------------------------------------

refSWC = os.path.join(homeFolder, 'DataAndResults/morphology/Registered/chiangOMB/', expNames[refInd] + '.swc')

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [x[:-4] for x in os.listdir(dirPath) if x.endswith('.swc')]
# refInd = 0
#
# # ---------------------------------------------------------------------------------
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLALInt/'
# label = 'LALInt'
#
# basicScale = 1 / np.array([0.32, 0.32, 1/3.785])
# gridUnitSize = 0.25 * basicScale
# sigmas = np.array([1, 1, 1]) * basicScale
# resampleLen = 0.1 * np.mean(basicScale)
# initTrans = np.diag([1, 1, 1])
# # ---------------------------------------------------------------------------------
#
# # resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLALInt/'
# # label = 'LALInt_RefPCA'
# # basicScale = 1 / np.array([0.32, 0.32, 1/3.785])
# # gridUnitSize = 0.25 * basicScale
# # sigmas = np.array([1, 1, 1]) * basicScale
# # resampleLen = 0.1 * np.mean(basicScale)
# # initTrans = np.diag([1, 1, 1])
# # ---------------------------------------------------------------------------------
# # resDir = homeFolder + '/DataAndResults/morphology/Registered/chiangLALInt/'
# # label = 'LALInt_Registered'
# #
# # basicScale = [1, 1, 1]
# # gridUnitSize = [0.25] * 3
# # sigmas = [0.75, 0.75, 0.75]
# # resampleLen = 0.1
# # initTrans = np.diag([1, 1, 1])
# # ---------------------------------------------------------------------------------
#
# refSWC = os.path.join(homeFolder, 'DataAndResults/morphology/Registered/chiangLALInt/', expNames[0] + '.swc')

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLLC/'
# expNames = [
#             # 'Gad1-F-000062_Standardized',
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
#
# # # ---------------------------------------------------------------------------------
# # resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/chiangLLC/'
# # # initTrans = np.diag([1, 1, -1])
# # initTrans = np.diag([1, 1, 1])
# # label = 'LLC'
# # basicScale = [1, 1, 1]
# # gridUnitSize = [0.25] * 3
# # sigmas = [0.75] * 3
# # resampleLen = 0.1
# # # ---------------------------------------------------------------------------------
# # resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLLC/'
# # initTrans = np.diag([1, 1, 1])
# # label = 'LLCRefPCA'
# # basicScale = [1, 1, 1]
# # gridUnitSize = [0.25] * 3
# # sigmas = [0.75] * 3
# # resampleLen = 0.1
# # # ---------------------------------------------------------------------------------
# resDir = homeFolder + '/DataAndResults/morphology/Registered/chiangLLC/'
# initTrans = np.diag([1, 1, 1])
# label = 'LLC_Registered'
# basicScale = [1, 1, 1]
# gridUnitSize = [0.25] * 3
# sigmas = [0.75, 0.75, 0.75]
# resampleLen = 0.1
# # # ---------------------------------------------------------------------------------
# refSWC = os.path.join(homeFolder, 'DataAndResults/morphology/Registered/chiangLLC/', expNames[refInd] + '.swc')
# ----------------------------------------------------------------------------------------------------------------------
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
# refInd = 1
#
# #
# #
# # # ---------------------------------------------------------------------------------
# resDir = homeFolder + '/DataAndResults/morphology/directPixelBased/DL-Int-1_Foragers/'
# initTrans = np.diag([1, 1, 1])
# label = 'Foragers'
# basicScale = [1, 1, 1]
# gridUnitSize = [1] * 3
# sigmas = [5, 5, 5]
# resampleLen = 0.5
# # # ---------------------------------------------------------------------------------
# refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
# ----------------------------------------------------------------------------------------------------------------------
# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/OriginalData/DL-Int-1_Foragers_2015/')
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
# refInd = 4
# # ---------------------------------------------------------------------------------
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/DL-Int-1_Foragers_2015/')
# part = '-VB'
# initTrans = np.diag([1, 1, 1])
# label = 'Foragers'
# basicScale = [1, 1, 1]
# gridUnitSize = [1] * 3
# sigmas = [3, 3, 3]
# resampleLen = 0.5
# # ---------------------------------------------------------------------------------
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/DL-Int-1_Foragers_2015/')
# part = '-DB'
# initTrans = np.diag([1, 1, 1])
# label = 'Foragers'
# basicScale = [1, 1, 1]
# gridUnitSize = [1] * 3
# sigmas = [2, 2, 2]
# resampleLen = 0.5
# # ---------------------------------------------------------------------------------
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/DL-Int-1_Foragers_2015/')
# initTrans = np.diag([1, 1, 1])
# label = 'Foragers'
# basicScale = [1, 1, 1]
# gridUnitSize = [1] * 3
# sigmas = [2, 2, 2]
# resampleLen = 0.5
# # # ---------------------------------------------------------------------------------
# # refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
# refSWC = os.path.join(dirPath, expNames[refInd], expNames[refInd] + part + '.swc')
# ----------------------------------------------------------------------------------------------------------------------

refF = lambda dirPath, fName, resDir: os.path.join(dirPath, fName + '.swc')
origF = lambda dirPath, fName, resDir: os.path.join(dirPath, fName + '.swc')
regF = lambda dirPath, fName, resDir: os.path.join(resDir, fName + '.swc')
regFNorm = lambda dirPath, fName, resDir: os.path.join(resDir, fName + '_norm.swc')
regABF = lambda A, B, resDir: os.path.join(resDir, A + '-' + B + '.swc')
startPt = lambda dirPath, fName, resDir: os.path.join(resDir, fName + 'trans', '0.swc')
startPtAB = lambda A, B, resDir: os.path.join(resDir, A + '-' + B + 'trans', '0.swc')
regIt = lambda resDir, expName, iterNo: os.path.join(resDir, expName + str(iterNo) + '.swc')
intermediateFIt = lambda itert, fName, resDir, iterNo: os.path.join(resDir, fName + str(iterNo)
                                                                    + 'trans', itert + '.swc')
regPart = lambda fName, resDir, part: os.path.join(resDir, fName, fName + part + '.swc')
regPartNorm = lambda fName, resDir, part: os.path.join(resDir, fName, fName + part + '_norm.swc')
regPartIt = lambda fName, resDir, part, iterNo: os.path.join(resDir, fName + str(iterNo), fName + part + '.swc')
swcFiles = []

for expInd, expName in enumerate(expNames):
    # swcFiles.append(regIt(resDir, expName, 1))
    # swcFiles.append(regPartIt(expName, resDir, '_part1', 0))
    # swcFiles.append(intermediateFIt('0', expName, resDir, 0))
    # swcFiles.append(origF(dirPath, expName, resDir))
    # swcFiles.append(regF(dirPath, expName, resDir))
    swcFiles.append(regFNorm(dirPath, expName, resDir))
    # swcFiles.append(regPart(expName, resDir, part))
    # swcFiles.append(regPartNorm(expName, resDir, part))

    # if expInd == refInd:
    #     swcFiles.append(refF(dirPath, expName, resDir))
    # else:
    #     # swcFiles.append(origF(dirPath, expName, resDir))
    #     # swcFiles.append(regABF(expName, expNames[refInd], resDir))
    #     # swcFiles.append(startPtAB(expName, expNames[refInd], resDir))
    #     swcFiles.append(regIt(resDir, expName, 0))



#------------
# # Only tips
# label = label + '_Tips'
# masks = []
# for swcFile in swcFiles:
#
#     data = np.loadtxt(swcFile)
#     mask = map(lambda ptInd: ptInd not in data[:, 6], data[:, 0])
#     masks.append(mask)
#
# densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen, masks=masks,
#                                    pcaView=True, refSWC=refSWC, initTrans=initTrans)
# density, bins = densityViz.calculateDensity(swcFiles, sigmas)
#------------
# # All points
# densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
#                                    pcaView='closestPCMatch', refSWC=refSWC, initTrans=initTrans)
densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
                                   pcaView='assumeRegistered', refSWC=refSWC, initTrans=initTrans)
density, bins = densityViz.calculateDensity(swcFiles, sigmas)
# density, bins = calcMorphDensity(swcFiles, sigmas, gridUnitSize, resampleLen, pcaView=False, refSWC=refSWC)
#------------


# fig1, ax1 = plt.subplots(figsize=(10, 8))
density01 = np.max(density, axis=2)
# im1 = ax1.imshow(density01, interpolation='none',
#              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
#
#
# fig1.colorbar(im1, ax=ax1, use_gridspec=True)
# ax1.set_ylabel('Axis 1')
# ax1.set_xlabel('Axis 2')
# ax1.set_xticklabels([str(x * gridUnitSize[1]) for x in ax1.get_xticks()])
# ax1.set_yticklabels([str(x * gridUnitSize[0]) for x in ax1.get_yticks()])
#
#
#
# fig2, ax2 = plt.subplots(figsize=(10, 8))
density02 = np.max(density, axis=1)
# im2 = ax2.imshow(density02, interpolation='none',
#              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
#
#
# fig2.colorbar(im2, ax=ax2, use_gridspec=True)
# ax2.set_xlabel('Axis 3')
# ax2.set_ylabel('Axis 1')
# ax2.set_xticklabels([str(x * gridUnitSize[2]) for x in ax2.get_xticks()])
# ax2.set_yticklabels([str(x * gridUnitSize[0]) for x in ax2.get_yticks()])
#
# for fig in [fig1, fig2]:
#     fig.tight_layout()
#     fig.canvas.draw()

# scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
# ax1.add_artist(scaleBar)
# scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
# ax2.add_artist(scaleBar)

densityDir = os.path.join(resDir, 'DensityResults')
if not os.path.isdir(densityDir):
    os.mkdir(densityDir)

outFile = os.path.join(densityDir, label + part)
plt.imsave(outFile + '12' + '.png', density01, dpi=300, format='png', cmap=plt.cm.jet, vmax=1, vmin=0)
plt.imsave(outFile + '13' + '.png', density02, dpi=300, format='png', cmap=plt.cm.jet, vmax=1, vmin=0)

densityViz.generateDensityColoredSSWC(swcFiles, [os.path.join(densityDir, x + '_density.sswc') for x in expNames],
                                      density)

writeTIFF(density, outFile)
np.savez_compressed(outFile, density=density, bins=bins, expNames=swcFiles)




