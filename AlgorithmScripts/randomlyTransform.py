import numpy as np
import os
from GJEMS.morph.transforms import compose_matrix
from RegMaxSCore.swcFuncs import transSWC_rotAboutPoint
import json

# ----------------------------------------------------------------------------------------------------------------------
temp = os.path.split(__file__)[0]
dirPath = os.path.join(os.path.split(temp)[0], 'TestFiles')
expNames = [
                'HSN-fluoro01.CNG',
              ]

outPath = dirPath
# ----------------------------------------------------------------------------------------------------------------------

# suffix = 'RandTrans'

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

translation = np.random.rand(3) * (transBounds[1] - transBounds[0]) + transBounds[0]
scale = np.random.rand(3) * (scaleBounds[1] - scaleBounds[0]) + scaleBounds[0]
rots = np.random.rand(3) * (rotBounds[1] - rotBounds[0]) + rotBounds[0]

rotMat = compose_matrix(angles=rots, scale=scale)[:3, :3]


for expName in expNames:
    inFile = os.path.join(dirPath, expName + '.swc')
    outFile = os.path.join(outPath, expName + suffix + '.swc')

    rotCenter = np.loadtxt(inFile)[:, 2:5].mean(axis=0)

    transSWC_rotAboutPoint(inFile, rotMat, translation, outFile, rotCenter)

    with open(os.path.join(outPath, expName + suffix + '.json'), 'w') as fle:
        toWrite = {'inFile': inFile,
                   'translation': translation.tolist(), 'angles': rots.tolist(), 'scale': scale.tolist(),
                   'comments': 'rotation and scaling about inFile centroid'}
        json.dump(toWrite, fle)

