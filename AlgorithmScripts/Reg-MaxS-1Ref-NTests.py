import os
from RegMaxSCore.iterativeRegistration import IterativeRegistration
import numpy as np

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
gridSizes = [40.0, 20.0, 10.0, 5.0]
# gridSizes = [40.0, 20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
# --------------------------------------------------------------------------------------

nCPU = 6
# usePartsDir = False
usePartsDir = True

# ----------------------------------------------------------------------------------------------------------------------

refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')

iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                transMinRes, minScaleStepSize, rotMinRes, nCPU)


for expInd, expName in enumerate(expNames):
    if refInd != expInd:
        print('Doing ' + expName)

        SWC2Align = os.path.join(dirPath, expName + '.swc')
        if usePartsDir:
            partsDir = os.path.join(dirPath, expName)
        else:
            partsDir = None
        iterReg.performReg(SWC2Align, expName, resDir, scaleBounds, partsDir)

