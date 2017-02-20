import os
import numpy as np
from RegMaxSCore.iterativeRegistration import IterativeRegistration
import shutil
# ----------------------------------------------------------------------------------------------------------------------
# #
temp = os.path.split(__file__)[0]
temp1 = os.path.split(temp)[0]

dirPath = os.path.join(temp1, 'TestFiles')
expNames = [
                'HSN-fluoro01.CNG',
                'HSN-fluoro01.CNGRandRot',
              ]
refInd = 0
resDir = os.path.join(temp1, 'Results', 'rotRefined')
if not os.path.isdir(resDir):
    os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

gridSizes = [40.0, 20.0, 10.0]
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
nCPU = 6


refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, None,
                                None, None, rotMinRes, nCPU)

ipParFile = os.path.join(resDir, 'tmp.json')
vals = ['rot']
tempOutFiles = {}
for val in vals:
    fle1 = os.path.join(resDir, val + '.swc')
    fle2 = os.path.join(resDir, val + 'bestSol.json')
    tempOutFiles[val] = [fle1, fle2]

for expInd, expName in enumerate(expNames):
    if refInd != expInd:
        print('Doing ' + expName + ' Rot')

        SWC2Align = os.path.join(dirPath, expName + '.swc')

        iterReg.rotOnce(SWC2Align, tempOutFiles['rot'], ipParFile)

        shutil.copyfile(tempOutFiles['rot'][0], os.path.join(resDir, '{}.swc'.format(expName)))
        shutil.copyfile(tempOutFiles['rot'][1], os.path.join(resDir, '{}bestSol.json'.format(expName)))

        for g in vals:
            [os.remove(x) for x in tempOutFiles[g]]
        os.remove(ipParFile)





