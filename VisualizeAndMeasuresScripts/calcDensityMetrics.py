import numpy as np
import os
import operator
from matplotlib import  pyplot as plt
# plt.ion()

homeFolder = os.path.expanduser('~')


def getDensityData(npzFile):

    try:
        data = np.load(npzFile)
    except Exception as e:
        raise(IOError('Problem reading ' + npzFile + ' as a compressed numpy file.'))

    return data['bins'], data['density']

def calcCorrCoeff(density1, density2):

    assert isinstance(density1, np.ndarray) and isinstance(density2, np.ndarray), \
        'density1 and density2 must be numpy arrays'
    assert density1.shape == density2.shape, 'density1 and density2 must have identical shapes'

    density1Mean = density1.mean()
    density2Mean = density2.mean()
    density1Std = density1.std()
    density2Std = density2.std()

    return ((density1 - density1Mean) * (density2 - density2Mean)).mean() / (density1Std * density2Std)


# ----------------------------------------------------------------------------------------------------------------------
# refDensityNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                               'chiangOMB_commonRef_1', 'OMB_Registered.npz')
# testDensityNPZs = [
#                     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                                  'chiangOMB_commonRef_1', 'OMBRefPCA.npz'),
#                     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                                  'chiangOMB_commonRef_1', 'OMB.npz')
#
#                     ]
# outDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                       'chiangOMB_commonRef_1', )

# ----------------------------------------------------------------------------------------------------------------------
# refDensityNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                               'chiangLLC_commonRef_1', 'LLC_Registered.npz')
# testDensityNPZs = [
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangLLC_commonRef_1', 'LLCRefPCA.npz'),
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangLLC_commonRef_1', 'LLC.npz')
#
# ]
# outDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                       'chiangLLC_commonRef_1', )
# ----------------------------------------------------------------------------------------------------------------------
# refDensityNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                               'chiangOPSInt_commonRef_1', 'OPSInt_Registered_part0.npz')
# testDensityNPZs = [
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangOPSInt_commonRef_1', 'OPSIntRefPCA_part0.npz'),
#     os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                  'chiangOPSInt_commonRef_1', 'OPSInt_part0.npz')
#
# ]
#
# outDir = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
#                       'chiangOPSInt_commonRef_1', )

# ----------------------------------------------------------------------------------------------------------------------
#
refDensityNPZ = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                              'chiangOPSInt_commonRef_1', 'OPSInt_Registered_part1.npz')
testDensityNPZs = [
    os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                 'chiangOPSInt_commonRef_1', 'OPSIntRefPCA_part1.npz'),
    os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                 'chiangOPSInt_commonRef_1', 'OPSInt_part1.npz')
]

outDir  = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                              'chiangOPSInt_commonRef_1',)
# ----------------------------------------------------------------------------------------------------------------------


refBins, refDensity = getDensityData(refDensityNPZ)
refBinSizes = [x[1] - x[0] for x in refBins]

testBins = []


for npzf in testDensityNPZs:

    b, d = getDensityData(npzf)
    testBins.append(b)
    testBinSizes = [x[1] - x[0] for x in b]
    assert all(x == y for x, y in zip(testBinSizes, refBinSizes)), 'Bin sizes are not equal for ' + npzf
    del d

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

del refDensity
refName = os.path.split(refDensityNPZ)[1][:-4]

rmses = []
for testInd, testBound in enumerate(testBounds):

    testName = os.path.split(testDensityNPZs[testInd])[1][:-4]
    bins, testDensity = getDensityData(testDensityNPZs[testInd])

    newTestDensity = np.zeros(newDensityShape)
    newTestStartStopInds = [[int((x[0] - y[0]) / z), int((x[1] - y[1]) / z)]
                       for x, y, z in zip(testBound, bounds, refBinSizes)]
    newTestDensity[newTestStartStopInds[0][0]: newTestStartStopInds[0][1] + newDensityShape[0],
                   newTestStartStopInds[1][0]: newTestStartStopInds[1][1] + newDensityShape[1],
                   newTestStartStopInds[2][0]: newTestStartStopInds[2][1] + newDensityShape[2]] = testDensity
    del testDensity
    
    densityDiff = newTestDensity - newRefDenstiy
    rmse = np.sqrt(np.power(densityDiff, 2).mean())
    rmses.append(rmse)

    whereRef0 = newRefDenstiy == 0
    whereTestNonZero = newTestDensity > 0
    temp = np.logical_and(whereRef0, whereTestNonZero)
    sharpness = (np.array(temp, np.float) * densityDiff).sum() / temp.sum()

    # import ipdb
    # ipdb.set_trace()

    refProjs = [newRefDenstiy.max(axis=2), newRefDenstiy.max(axis=1)]
    testProjs = [newTestDensity.max(axis=2), newTestDensity.max(axis=1)]

    plt.imsave(refDensityNPZ[:-4] + '12_common.png', refProjs[0], dpi=300, format='png',
               cmap=plt.cm.jet, vmax=1, vmin=0)
    plt.imsave(refDensityNPZ[:-4] + '13_common.png', refProjs[1], dpi=300, format='png',
               cmap=plt.cm.jet, vmax=1, vmin=0)

    plt.imsave(testDensityNPZs[testInd][:-4] + '12_common.png', testProjs[0], dpi=300, format='png',
               cmap=plt.cm.jet, vmax=1, vmin=0)
    plt.imsave(testDensityNPZs[testInd][:-4] + '13_common.png', testProjs[1], dpi=300, format='png',
               cmap=plt.cm.jet, vmax=1, vmin=0)

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 11.2))
    ax[0, 0].imshow(refProjs[0], vmax=1, vmin=0, interpolation='None')
    ax[1, 0].imshow(testProjs[0], vmax=1, vmin=0, interpolation='None')

    ax[0, 1].imshow(refProjs[1], vmax=1, vmin=0, interpolation='None')
    ax[1, 1].imshow(testProjs[1], vmax=1, vmin=0, interpolation='None')

    ax[0, 0].set_title('Ref')
    ax[1, 0].set_xlabel('Y')
    ax[1, 0].set_ylabel('X')
    ax[1, 0].set_title('Test; Root-Mean-Square differences=' + str(rmse))

    ax[0, 1].set_title('Ref')
    ax[1, 1].set_xlabel('Z')
    ax[1, 1].set_ylabel('X')
    ax[1, 1].set_title('Test; Fuzziness=' + str(sharpness))

    fig.tight_layout()
    fig.canvas.draw()

    fig.savefig(os.path.join(outDir, refName + '-' + testName + '.jpg'), dpi=300)



