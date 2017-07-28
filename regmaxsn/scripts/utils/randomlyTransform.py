# Ajayrama Kumaraswamy, 2017, LMU Munich

"""
Description:        This script is used to randomly transform a list of SWCs. Sets of rotation, translation and
                    scaling transform parameters are drawn independently from uniform distributions with specified
                    bounds. Each transform is then applied with to each SWC in the list.
                    The transform parameters and the order of application are as below:
                    (i) scaling centering at the centroid and along XYZ axes. Values must be in (0, 1]
                    (ii) Euler angles in radians, XYZ rotations about centroid
                    (iii) translations in micrometers along XYZ axes


Usage:              python <path to file>randomlyTransform.py

Action:             Transforms SWCs using N sets of independently drawn transform paramters.
                    For every SWC with name in expNames and in the folder dirPath, N number of correspondingly
                    transformed SWC files with names <swc name><suffix><transform set #>.swc are created in the folder
                    outPath.
                    For each such SWC, a json file is also created with the input parameters, i.e.,
                    swc being transformed, euler angles, scalings and translations.


Usage guidelines:   Edit the variables dirPath, expNames, outPath, N, suffix, transBounds, rotBounds, scaleBounds and
                    run this script.
"""

import numpy as np
import os
from regmaxsn.core.transforms import compose_matrix
from regmaxsn.core.swcFuncs import transSWC_rotAboutPoint
import json

# ----------------------------------------------------------------------------------------------------------------------
temp = os.path.split(__file__)[0]
dirPath = os.path.join(os.path.split(temp)[0], 'TestFiles')
expNames = [
                'HSN-fluoro01.CNG',
                # 'HSN-fluoro01.CNGNoiseStd1',
                # 'HSN-fluoro01.CNGNoiseStd2',
                # 'HSN-fluoro01.CNGNoiseStd3',
                # 'HSN-fluoro01.CNGNoiseStd4',
                # 'HSN-fluoro01.CNGNoiseStd5',
              ]

outPath = dirPath
N = 1
# ----------------------------------------------------------------------------------------------------------------------

# suffix = 'RandTrans'
#
# transBounds = [-20, 20]
# rotBounds = [-np.pi / 6, np.pi / 6]
# scaleBounds = [0.5, 1 / 0.5]
# ----------------------------------------------------------------------------------------------------------------------
# suffix = 'RandRot'
#
# transBounds = [0, 0]
# rotBounds = [-np.pi / 6, np.pi / 6]
# scaleBounds = [1, 1]
# ----------------------------------------------------------------------------------------------------------------------
# suffix = 'RandScale'
#
# transBounds = [0, 0]
# rotBounds = [0, 0]
# scaleBounds = [0.5, 1 / 0.5]
# ----------------------------------------------------------------------------------------------------------------------
suffix = 'RandTranslate'

transBounds = [-20, 20]
rotBounds = [0, 0]
scaleBounds = [1, 1]
# ----------------------------------------------------------------------------------------------------------------------


for ind in range(N):
    translation = np.random.rand(3) * (transBounds[1] - transBounds[0]) + transBounds[0]
    scale = np.random.rand(3) * (scaleBounds[1] - scaleBounds[0]) + scaleBounds[0]
    rots = np.random.rand(3) * (rotBounds[1] - rotBounds[0]) + rotBounds[0]

    rotMat = compose_matrix(angles=rots, scale=scale)[:3, :3]

    for expName in expNames:
        inFile = os.path.join(dirPath, expName + '.swc')
        outFile = os.path.join(outPath, expName + suffix + str(ind) + '.swc')

        rotCenter = np.loadtxt(inFile)[:, 2:5].mean(axis=0)

        transSWC_rotAboutPoint(inFile, rotMat, translation, outFile, rotCenter)

        with open(os.path.join(outPath, expName + suffix + str(ind) + '.json'), 'w') as fle:
            toWrite = {'inFile': inFile,
                       'translation': translation.tolist(), 'angles': rots.tolist(), 'scale': scale.tolist(),
                       'comments': 'rotation and scaling about inFile centroid'}
            json.dump(toWrite, fle)
