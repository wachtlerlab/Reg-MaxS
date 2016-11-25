import os
import numpy as np
from RegMaxSCore.iterativeRegistration import IterativeRegistration
import shutil

homeFolder = os.path.expanduser('~')

# ----------------------------------------------------------------------------------------------------------------------
# #
dirPath = 'TestFiles'
expNames = [
                'HB130313-4',
                'HB130313-4RandTrans1',
              ]
refInd = 0
resDir = os.path.join('Results', 'rotRefined')
if not os.path.isdir(resDir):
    os.mkdir(resDir)
# ----------------------------------------------------------------------------------------------------------------------

gridSizes = [40.0, 20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6], [-np.pi / 6, np.pi / 6]]
rotMinRes = np.deg2rad(1).round(4)
scaleBounds = [[0.5, 1/0.5], [0.5, 1/0.5], [0.5, 1/0.5]]
minScaleStepSize = 1.005
nCPU = 6


refSWC = os.path.join(dirPath, expNames[refInd] + '.swc')
iterReg = IterativeRegistration(refSWC, gridSizes, rotBounds, transBounds,
                                transMinRes, minScaleStepSize, rotMinRes, nCPU)

ipParFile = os.path.join(resDir, 'tmp.json')
vals = ['trans']
tempOutFiles = {}
for val in vals:
    fle1 = os.path.join(resDir, val + '.swc')
    fle2 = os.path.join(resDir, val + 'bestSol.json')
    tempOutFiles[val] = [fle1, fle2]

for expInd, expName in enumerate(expNames):
    if refInd != expInd:
        print('Doing ' + expName + ' Scale')

        SWC2Align = os.path.join(dirPath, expName + '.swc')

        iterReg.transOnce(SWC2Align, tempOutFiles['trans'], ipParFile)

        shutil.copyfile(tempOutFiles['trans'][0], os.path.join(resDir, '{}.swc'.format(expName)))
        shutil.copyfile(tempOutFiles['trans'][1], os.path.join(resDir, '{}bestSol.json'.format(expName)))

        for g in vals:
            [os.remove(x) for x in tempOutFiles[g]]
        os.remove(ipParFile)





