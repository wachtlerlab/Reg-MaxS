import os
import shutil
from RegMaxSCore.iterativeRegistration import IterativeRegistration
from RegMaxSCore.swcFuncs import transSWC_rotAboutPoint



# ----------------------------------------------------------------------------------------------------------------------
#
dirPath = 'TestFiles'

expNames = [

            'HSN-fluoro01.CNG',
            'HSN-fluoro01.CNGRandTrans',
            'HSN-fluoro01.CNGRandTrans1',
            'HSN-fluoro01.CNGRandTrans2',
            'HSN-fluoro01.CNGRandTrans3',
            'HSN-fluoro01.CNGRandTrans4',
            'HSN-fluoro01.CNGRandTrans5',
            'HSN-fluoro01.CNGRandTrans6',
            'HSN-fluoro01.CNGRandTrans7',
            'HSN-fluoro01.CNGRandTrans8',
            'HSN-fluoro01.CNGRandTrans9',

            # 'HSN-fluoro01.CNGNoiseStd1RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd2RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd3RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd4RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd5RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd6RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd7RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd8RandTrans',
            # 'HSN-fluoro01.CNGNoiseStd9RandTrans',
            ]


refInd = 0
resDir = os.path.join('Results', 'Reg-MaxS')
if not os.path.isdir(resDir):
    os.mkdir(resDir)

# --------------------------------------------------------------------------------------
#
# gridSizes = [40.0, 20.0, 10.0]
# # gridSizes = [20.0, 10.0]
# transBounds = [[-30, 30], [-30, 30], [-30, 30]]
# transMinRes = 1
# rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
# rotMinRes = np.deg2rad(1).round(4)
# scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
# minScaleStepSize = 1.005
# nCPU = 6
# nIter = 100

if os.path.isdir(resDir):

    ch = raw_input('Folder exists: ' + resDir + '\nDelete(y/n)?')
    if ch == 'y':
        shutil.rmtree(resDir)
    else:
        quit()

os.mkdir(resDir)


refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')


iterReg = IterativeRegistration(refSWC, None, None, None, None, None, None, None)

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

    totalTransform = iterReg.pca_based(SWC2Align, [outSWCFile, outBSFile], tempDir, 5)

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
    [os.remove(x) for x in tempOutFiles[g] if os.path.exists(x)]
if os.path.exists(ipParFile):
    os.remove(ipParFile)
