import os
import numpy as np
from RegMaxSCore.iterativeRegistration import IterativeRegistration
import shutil
homeFolder = os.path.expanduser('~')




# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-1/')
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
# refInd = 0
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/DL-Int-1/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/Tests')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/Tests/'
# # resDir = 'tmp/directPixelBased'
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------


# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/peng/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/peng/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------
#
# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/borstHSNR/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/borstHSNR/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/borstHSNL/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/borstHSNL/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/borstHSE/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/borstHSE/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------


# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/Mustaparta_Lofaldi')
#
# expNames = [
#             'Nevron-komplett-08-02-28-2a.CNG',
#             'Nevron-komplett-08-03-13-2a.CNG',
#             'Nevron-komplett-08-08-28-1a-A.CNG',
#             ]
# refInd = 0
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/Mustaparta_Lofaldi/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/sztarkerLGMD/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/sztarkerLGMD/')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/ChalupaRGCBi')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/ChalupaRGCBi')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/JefferisvPN')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/JefferisvPN')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/ChiangRAL/')
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
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/ChiangRAL')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/chiangLALInt')
#
# expNames = [
#             'Trh-F-100085.CNG',
#             'Trh-F-100088.CNG',
#             'Trh-F-300133.CNG',
#             'Trh-F-500108.CNG',
#             'Trh-F-700065.CNG',
#             ]
# refInd = 0
#
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/chiangLALInt')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------
dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-1_Foragers_DB')

expNames = [
            'HB130425-1-DB',
            'HB130326-2-DB',
            'HB140424-1-DB',
            'HB130408-1-DB',
            'HB130322-1-DB',
            'HB130313-4-DB',
            'HB130501-2-DB',
            'HB130705-1-DB',
            ]
refInd = 0

resDir = os.path.join(homeFolder, 'DataAndResults/morphology/AllAll/DL-Int-Foragers_DB')
if not os.path.isdir(resDir):
    os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-1_Foragers_VB')
#
# expNames = [
#             'HB130425-1-VB',
#             'HB130326-2-VB',
#             'HB140424-1-VB',
#             'HB130408-1-VB',
#             'HB130322-1-VB',
#             'HB130313-4-VB',
#             'HB130501-2-VB',
#             'HB130705-1-VB',
#             ]
# refInd = 0
#
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/AllAll/DL-Int-Foragers_VB')
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------


gridSizes = [40.0, 20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
scaleBounds = [[0.75, 1 / 0.75], [0.75, 1 / 0.75], [0.75, 1 / 0.75]]
minScaleStepSize = 1.005
nCPU = 7
initGuessType = 'just_centroids'

# ----------------------------------------------------------------------------------------------------------------------



for refInd, expName in enumerate(expNames):

    refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')

    iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                    scaleBounds, transMinRes, minScaleStepSize, rotMinRes, nCPU)


    for expInd, expName in enumerate(expNames):
        if refInd != expInd:
            print('Doing ' + expName)

            SWC2Align = os.path.join(dirPath, expName + '.swc')
            iterReg.performReg(SWC2Align, expName + '-' + expNames[refInd], resDir, initGuessType=initGuessType)
        else:
            shutil.copyfile(refSWC, os.path.join(resDir, expNames[refInd] + '-' + expNames[refInd] + '.swc'))
