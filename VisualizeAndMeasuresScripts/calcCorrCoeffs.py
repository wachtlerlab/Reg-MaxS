import numpy as np
import os
import operator
from matplotlib import  pyplot as plt
plt.ion()

homeFolder = os.path.expanduser('~')


def getDensityData(npzFile):

    try:
        data = np.load(npzFile)
    except Exception as e:
        raise(IOError('Problem reading ' + npzFile + ' as a compressed numpy file.'))

    return data['bins'], data['density']

def calcCorrCoef(density1, density2):

    assert isinstance(density1, np.ndarray) and isinstance(density2, np.ndarray), 'density1 and density2 must be numpy arrays'
    assert density1.shape == density2.shape, 'density1 and density2 must have identical shapes'

    density1Mean = density1.mean()
    density2Mean = density2.mean()
    density1Std = density1.std()
    density2Std = density2.std()

    return ((density1 - density1Mean) * (density2 - density2Mean)).mean() / (density1Std * density2Std)

refDensitiyNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                              'chiangOMB_commonRef_1', 'OMB_Registered.npz')
testDensityNPZs = [
                    os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                                 'chiangOMB_commonRef_1', 'OMBRefPCA.npz'),
                    # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                    #              'chiangOMB_commonRef_1', 'OMB.npz')

                    ]

# refDensitiyNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                               'chiangLLC_commonRef_1', 'LLC_Registered.npz')
# testDensityNPZs = [
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangLLC_commonRef_1', 'LLCRefPCA.npz'),
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangLLC_commonRef_1', 'LLC.npz')
#
# ]


refBins, refDensity = getDensityData(refDensitiyNPZ)
refBinSizes = [x[1] - x[0] for x in refBins]

testBins = []
testDensities = []

for npzf in testDensityNPZs:

    b, d = getDensityData(npzf)
    testBins.append(b)
    testDensities.append(d)
    testBinSizes = [x[1] - x[0] for x in b]
    assert all(x == y for x, y in zip(testBinSizes, refBinSizes)), 'Bin sizes are not equal for ' + npzf

refBounds = [(min(x), max(x)) for x in refBins]
testBounds = [[(min(x), max(x)) for x in y] for y in testBins]

bounds = [(min([y[0] for y in x]), max([y[1] for y in x])) for x in zip(refBounds, *testBounds)]
newDensityShape = [int((x[1] - x[0]) / y) for x, y in zip(bounds, refBinSizes)]

newRefDenstiy = np.zeros(newDensityShape)
newRefStartStopInds = [[int((x[0] - y[0]) / z), int((x[1] - y[1]) / z)]
                       for x, y, z in zip(refBounds, bounds, refBinSizes)]

newRefDenstiy[newRefStartStopInds[0][0]: newRefStartStopInds[0][1] + newDensityShape[0],
              newRefStartStopInds[1][0]: newRefStartStopInds[1][1] + newDensityShape[1],
              newRefStartStopInds[2][0]: newRefStartStopInds[2][1] + newDensityShape[2]] = refDensity

corrCoeffs = []
for testInd, testBound in enumerate(testBounds):

    newTestDensity = np.zeros(newDensityShape)
    newTestStartStopInds = [[int((x[0] - y[0]) / z), int((x[1] - y[1]) / z)]
                       for x, y, z in zip(testBound, bounds, refBinSizes)]
    newTestDensity[newTestStartStopInds[0][0]: newTestStartStopInds[0][1] + newDensityShape[0],
                   newTestStartStopInds[1][0]: newTestStartStopInds[1][1] + newDensityShape[1],
                   newTestStartStopInds[2][0]: newTestStartStopInds[2][1] + newDensityShape[2]] = testDensities[testInd]

    corrCoeff = calcCorrCoef(newRefDenstiy, newTestDensity)
    corrCoeffs.append(corrCoeff)

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 11.2))
    ax[0, 0].imshow(newRefDenstiy.max(axis=2), vmax=1, vmin=0, interpolation='None')
    ax[1, 0].imshow(newTestDensity.max(axis=2), vmax=1, vmin=0, interpolation='None')

    ax[0, 1].imshow(newRefDenstiy.max(axis=1), vmax=1, vmin=0, interpolation='None')
    ax[1, 1].imshow(newTestDensity.max(axis=1), vmax=1, vmin=0, interpolation='None')

    ax[0, 0].set_title('Ref')
    ax[1, 0].set_xlabel('Y')
    ax[1, 0].set_ylabel('X')
    ax[1, 0].set_title('Test')

    ax[0, 1].set_title('Ref')
    ax[1, 1].set_xlabel('Z')
    ax[1, 1].set_ylabel('X')
    ax[1, 1].set_title('Test')

for testNPZ, corrCoeff in zip(testDensityNPZs, corrCoeffs):
    print(testNPZ, corrCoeff)
