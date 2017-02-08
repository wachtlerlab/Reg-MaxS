# Ajayrama Kumaraswamy, 2017, LMU Munich

"""
Description:        This script is used to adding spherical gaussian noise of different standard deviations
                    to the points of a list of SWCs.


Usage:              python <path to file>addRandomNoise.py

Action:             For each SWC in baseSWCs, and each value of standard deviation in noiseStds, draws a sample of
                    the same size as the number of points in the SWC from the same zero mean Gaussian distribution of
                    the specified standard deviation, adds it to the points and writes it to
                    <swc Name>NoiseStd<standard deviation>.swc in the folder outPath

Usage guidelines:   Edit the variables dirPath, expNames, outPath, noiseStds and run this script.
"""

import numpy as np
import os
from RegMaxSN.RegMaxSCore.swcFuncs import readSWC_numpy, writeSWC_numpy
# ----------------------------------------------------------------------------------------------------------------------
temp = os.path.split(__file__)[0]
dirPath = os.path.join(os.path.split(temp)[0], 'TestFiles')
expNames = [
                'HSN-fluoro01.CNG',
              ]

outPath = dirPath
noiseStds = range(1, 6)
# ----------------------------------------------------------------------------------------------------------------------

baseSWCs = [os.path.join(dirPath, expName + '.swc') for expName in expNames]

for baseSWC in baseSWCs:

    expName = os.path.split(baseSWC)[1][:-4]
    headr, data = readSWC_numpy(baseSWC)

    for std in noiseStds:

        noise = np.random.normal(0, std, (data.shape[0], 3))
        noisyData = data.copy()
        noisyData[:, 2:5] = data[:, 2:5] + noise
        outFile = os.path.join(outPath, expName + 'NoiseStd' + str(std) + '.swc')

        writeSWC_numpy(outFile, noisyData, headr)
# ----------------------------------------------------------------------------------------------------------------------

