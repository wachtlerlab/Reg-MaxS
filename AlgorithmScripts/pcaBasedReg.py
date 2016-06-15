import os
import shutil
from RegMaxSCore.iterativeRegistration import IterativeRegistration
from RegMaxSCore.swcFuncs import transSWC_rotAboutPoint
import numpy as np

homeFolder = os.path.expanduser('~')


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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/DL-Int-1/'


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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/Tests/'
# # resDir = 'tmp/RefPCA'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/peng/'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/borstHSNR/'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/borstHSNL/'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/borstHSN/'


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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/borstHSE/'


# ----------------------------------------------------------------------------------------------------------------------


# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/Mustaparta_Lofaldi'
#
# expNames = [
#             'Nevron-komplett-08-02-28-2a.CNG',
#             'Nevron-komplett-08-03-13-2a.CNG',
#             'Nevron-komplett-08-08-28-1a-A.CNG',
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/Mustaparta_Lofaldi/'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/sztarkerLGMD/'


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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/ChalupaRGCBi'

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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/JefferisvPN'


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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/ChiangRAL'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [
#                 'VGlut-F-200277.CNG',
#                 'Trh-M-100050.CNG',
#                 'Trh-M-100088.CNG',
#                 'Trh-M-200056.CNG',
#                 'Trh-M-100073.CNG',
#                 'Trh-M-100036.CNG',
#                 'Trh-F-100071.CNG',
#                 'Trh-M-100090.CNG',
#                 'Trh-M-200010.CNG',
#                 'Gad1-F-500040.CNG',
#                 'Trh-F-100086.CNG',
#                 'Trh-F-100088.CNG',
#                 'VGlut-F-200266.CNG',
#                 'VGlut-F-100293.CNG',
#                 'VGlut-F-100223.CNG',
#                 'Trh-M-100046.CNG',
#                 'Trh-M-100096.CNG',
#                 'VGlut-F-800029.CNG',
#                 'Trh-M-100051.CNG',
#                 'Trh-M-100086.CNG',
#                 'Trh-M-100094.CNG',
#                 'Trh-M-200004.CNG',
#                 'Trh-F-100087.CNG',
#                 'VGlut-F-100238.CNG',
#                 'Trh-F-100085.CNG',
#             ]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLALInt'


# ----------------------------------------------------------------------------------------------------------------------

# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLACC/'
#
# expNames = [
#             'fru-M-100030.CNG',
#             'fru-M-700043.CNG',
#             'VGlut-F-000600.CNG',
#             ]
# refInd = 0
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLACC/'


# ----------------------------------------------------------------------------------------------------------------------

dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangOPSInt/'
expNames = [
            'Trh-F-000047.CNG',
            'Trh-M-000143.CNG',
            'Trh-F-000092.CNG',
            'Trh-F-700009.CNG',
            'Trh-M-000013.CNG',
            'Trh-M-000146.CNG',
            'Trh-M-100009.CNG',
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
refInd = 14
resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangOPSInt/'

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
# refInd = 6
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangOMB/'
# ----------------------------------------------------------------------------------------------------------------------
# dirPath = homeFolder + '/DataAndResults/morphology/OriginalData/chiangLALInt'
#
# expNames = [x[:-4] for x in os.listdir(dirPath) if x.endswith('.swc')]
# refInd = 0
#
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLALInt'
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
# resDir = homeFolder + '/DataAndResults/morphology/RefPCA/chiangLLC/'
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

if os.path.isdir(resDir):

    ch = raw_input('Folder exists: ' + resDir + '\nDelete(y/n)?')
    if ch == 'y':
        shutil.rmtree(resDir)
    else:
        quit()

os.mkdir(resDir)


refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')


iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                scaleBounds, transMinRes, minScaleStepSize, rotMinRes, nCPU)

ipParFile = os.path.join(resDir, 'tmp.json')
vals = ['rot', 'scale', 'trans']
tempOutFiles = {}
for val in vals:
    fle1 = os.path.join(resDir, val + '.swc')
    fle2 = os.path.join(resDir, val + 'bestSol.txt')
    tempOutFiles[val] = [fle1, fle2]



for expInd, expName in enumerate(expNames):

    print('Doing ' + expName)

    SWC2Align = os.path.join(dirPath, expName + '.swc')

    tempDir = os.path.join(resDir, expName + 'trans')
    if not os.path.isdir(tempDir):
        os.mkdir(tempDir)

    outSWCFile = os.path.join(resDir, expName + '.swc')
    outBSFile = os.path.join(resDir, expName + 'BS.swc')

    totalTransform = iterReg.createInitGuess(SWC2Align, [outSWCFile, outBSFile], tempDir, tempOutFiles, ipParFile,
                            gridSizes[-1], typ='pca_rev')

    partsDir = os.path.join(dirPath, expName)

    if os.path.isdir(partsDir):

        dirList = os.listdir(partsDir)
        dirList = [x for x in dirList if x.endswith('swc')]

        resPartsDir = os.path.join(resDir, expName)
        if not os.path.isdir(resPartsDir):
            os.mkdir(resPartsDir)

        for entry in dirList:
            transSWC_rotAboutPoint(os.path.join(partsDir, entry),
                                   totalTransform[:3, :3], totalTransform[:3, 3],
                                   os.path.join(resPartsDir, entry),
                                   [0, 0, 0]
                                   )

    shutil.rmtree(tempDir)
    os.remove(outBSFile)

for g in vals:
    [os.remove(x) for x in tempOutFiles[g]]
os.remove(ipParFile)
