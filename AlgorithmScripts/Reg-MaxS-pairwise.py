import os
from RegMaxSCore.iterativeRegistration import IterativeRegistration
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
testPath = '' # folder containing the test morphologies
refPath = '' # folder containing the corresponding reference morphologies
expNames = [

            ] # names of the swcs with the extension

resDir = '' # result directory; where the results will be generated
# ----------------------------------------------------------------------------------------------------------------------

if not os.path.isdir(resDir):
    os.mkdir(resDir)

# gridSizes = [20.0, 10.0, 5.0]
gridSizes = [40.0, 20.0, 10.0]
# gridSizes = [80.0, 40.0, 20.0, 10.0, 5.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
nCPU = 6
usePartsDir = True

# ----------------------------------------------------------------------------------------------------------------------

for expInd, expName in enumerate(expNames):
    refSWC = os.path.join(refPath, expName + '.swc')

    iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                transMinRes, minScaleStepSize, rotMinRes, nCPU)
    print('Doing ' + expName)

    SWC2Align = os.path.join(testPath, expName + '.swc')
    if usePartsDir:
        partsDir = os.path.join(testPath, expName)
    else:
        partsDir = None
    iterReg.performReg(SWC2Align, expName, resDir, scaleBounds=scaleBounds, partsDir=partsDir)