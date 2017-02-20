import os
from core.plotDensities import DensityVizualizations, writeTIFF
import numpy as np
from matplotlib import pyplot as plt
homeFolder = os.path.expanduser('~')

plt.ion()


# ----------------------------------------------------------------------------------------------------------------------
# # resDir = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/HB121224-1_80402010_1p0')
# # resDir = os.path.join(homeFolder, 'DataAndResults/morphology/Backups/directPixelBased/HB121224-1_80402010_noScale')
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/HB121224-1')
# expNames1 = ['HB121224-1-WNC10S10x20']
# expNames2 = ['HB121224-1-WNC10S10x40']
#

# part = ''
# label1 = 'x20'
# label2 = 'x40'

# swcSet1 = [os.path.join(resDir, x + '.swc') for x in expNames1]
# swcSet2 = [os.path.join(resDir, x + '.swc') for x in expNames2]

# gridUnitSize = [1] * 3
# sigmas = [5, 5, 5]
# resampleLen = 0.5
# initTrans = np.diag([1, 1, 1])
# ----------------------------------------------------------------------------------------------------------------------
resDir = os.path.join(homeFolder, 'DataAndResults/morphology/directPixelBased/DL-Int-1_Forager_NE/Forager_NE_norm/')

# Foragers
expNames1 = [
    'HB130313-4',
    'HB130322-1',
    'HB130326-2',
    'HB130408-1',
    'HB130425-1',
    'HB130501-2',
    'HB130705-1',
    'HB140424-1',
    # 'HB140701-1'
]

# newlyEmerged
expNames2 = [
    'HB130523-3',
    'HB130605-1',
    'HB130605-2',
    'HB140813-3',
    'HB140917-1',
    'HB140930-1',
    'HB141030-1',
    # 'HB140701-1'
]

part = '-DB'
# part = '-VB'
swcSet1 = [os.path.join(resDir, x + '_norm_norm', x + part + '_norm_norm.swc') for x in expNames1]
swcSet2 = [os.path.join(resDir, x + '_norm_norm', x + part + '_norm_norm.swc') for x in expNames2]

label1 = 'Forager'
label2 = 'NewlyEmerged'

gridUnitSize = [10] * 3
sigmas = [10] * 3
resampleLen = 1
initTrans = np.diag([1, 1, 1])
# ----------------------------------------------------------------------------------------------------------------------

densityDir = os.path.join(resDir, 'DensityDiffResults')
if not os.path.isdir(densityDir):
    os.mkdir(densityDir)

outFile = os.path.join(densityDir, label1 + '-' + label2 + '-' + part)


densityViz = DensityVizualizations(swcSet2 + swcSet1, gridUnitSize, resampleLen)

d1, bins = densityViz.calculateDensity(swcSet1, sigmas)
d2, bins = densityViz.calculateDensity(swcSet2, sigmas)

d1Md2 = d1 - d2

d1Md2Norm = d1Md2.copy()
d1Md2Norm += 1
d1Md2Norm /= 2


densityViz.generateDensityColoredSSWC(swcSet1,
                                      [os.path.join(densityDir, x + part + '_density.sswc') for x in expNames1],
                                      d1Md2Norm)
densityViz.generateDensityColoredSSWC(swcSet2,
                                      [os.path.join(densityDir, x + part + '_density.sswc') for x in expNames2],
                                      d1Md2Norm)


np.savez_compressed(outFile, density1=d1, density2=d2, bins=bins, swcSet1=swcSet1, swcSet2=swcSet2)
