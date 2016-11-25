import os
import numpy as np
import json
from RegMaxSCore.swcFuncs import transSWC

# ----------------------------------------------------------------------------------------------------------------------
dirPath = 'TestFiles'
expNames = [
            'Gad1-F-000062.CNG',
            'Cha-F-000012.CNG',
            'Cha-F-300331.CNG',
            'Gad1-F-600000.CNG',
            'Cha-F-000018.CNG',
            'Cha-F-300051.CNG',
            'Cha-F-400051.CNG',
            'Cha-F-200000.CNG'
            ]
refInd = 0
resDir = os.path.join('Results', 'Reg-MaxS-N')
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


