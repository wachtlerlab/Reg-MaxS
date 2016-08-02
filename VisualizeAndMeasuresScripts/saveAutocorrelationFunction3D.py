import sys
import os
import numpy as np
from itertools import product
import time

def getDensityData(npzFile):

    try:
        data = np.load(npzFile)
    except Exception as e:
        raise(IOError('Problem reading ' + npzFile + ' as a compressed numpy file.'))

    return data['bins'], data['density']

def getMinBoundingBox(density):

    nonZero = np.where(density != 0)
    return [(min(x), max(x)) for x in nonZero]

def calcACF(density, shifts):
    '''
    calculates the auto corrlation function of a 3D density represented as a 3d numpy array
    :param density: numpy.ndarray, 3 dimensional
    :param shifts: 3 member list, each member is a list of floats representing the shifts per dimension
    :return: shifts, acfs; list of numpy.ndarrays, numpy.ndarrays;
    The auto correlation at the shift (shifts[0][i], shifts[1][j], shifts[2][k]) is acfs[i, j, k].
    Auto correlation for all other shifts is equal to zero.

    Ref: https://en.wikipedia.org/wiki/Autocorrelation#Estimation
    '''

    meanDensity = density.mean()
    varDensity = density.var()
    sizeDensity = np.prod(density.shape)
    zeroMeanDensity = density - meanDensity
    acfDenom = sizeDensity * varDensity


    bb = getMinBoundingBox(density)
    print(bb, density.shape)
    acfs = np.empty(map(len, shifts))

    print('total Points:', np.prod(acfs.shape))
    done = False

    for xInd, yInd, zInd in product(*map(xrange, acfs.shape)):

        shiftX = int(shifts[0][xInd])
        shiftY = int(shifts[1][yInd])
        shiftZ = int(shifts[2][zInd])

        # if not done:
            # t1 = time.time()
        unshiftedIndRanges = [(max(bb[i][0], bb[i][0] + sh), min(bb[i][1], bb[i][1] + sh) + 1)
                            for i, sh in enumerate((shiftX, shiftY, shiftZ))]
        shiftedIndRanges = [(max(bb[i][0], bb[i][0] - sh), min(bb[i][1], bb[i][1] - sh) + 1)
                            for i, sh in enumerate((shiftX, shiftY, shiftZ))]
        # print(shiftX, shiftY, shiftZ)
        # print(unshiftedIndRanges)
        # print(shiftedIndRanges)

        unshiftedSlice = zeroMeanDensity[
                                            unshiftedIndRanges[0][0]: unshiftedIndRanges[0][1],
                                            unshiftedIndRanges[1][0]: unshiftedIndRanges[1][1],
                                            unshiftedIndRanges[2][0]: unshiftedIndRanges[2][1],
                                        ]
        shiftedSlice = zeroMeanDensity[
                         shiftedIndRanges[0][0]: shiftedIndRanges[0][1],
                         shiftedIndRanges[1][0]: shiftedIndRanges[1][1],
                         shiftedIndRanges[2][0]: shiftedIndRanges[2][1],
                         ]

        acf = (unshiftedSlice * shiftedSlice).sum() / acfDenom

        acfs[xInd, yInd, zInd] = acf

        # if not done:
        #     t2 = time.time()
        #     print(t2 - t1, (t2 - t1) * np.prod(acfs.shape), 's')
        #     done = True

    return shifts, acfs


if __name__ == '__main__':

    from matplotlib import pyplot as plt

    homeFolder = os.path.expanduser('~')
    minAC = 0.5
    ACFStepSize = 2

    densityFiles = [
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #              'chiangOMB_commonRef_1', 'OMBRefPCA.npz'),
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #              'chiangOMB_commonRef_1', 'OMB.npz'),
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #             'chiangOMB_commonRef_1', 'OMB_Registered.npz')

                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #                  'chiangLLC_commonRef_1', 'LLCRefPCA.npz'),
                            # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                            #              'chiangLLC_commonRef_1', 'LLC.npz'),
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #               'chiangLLC_commonRef_1', 'LLC_Registered.npz'),

                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #                  'chiangOPSInt_commonRef_1', 'OPSIntRefPCA_part0.npz'),
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #              'chiangOPSInt_commonRef_1', 'OPSInt_part0.npz'),
                        # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #              'chiangOPSInt_commonRef_1', 'OPSInt_Registered_part0.npz'),

                        os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                                         'chiangOPSInt_commonRef_1', 'OPSIntRefPCA_part1.npz'),
                        #     # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #     #              'chiangOPSInt_commonRef_1', 'OPSInt_part1.npz'),
                        #     # os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Results',
                        #     #              'chiangOPSInt_commonRef_1', 'OPSInt_Registered_part1.npz'),
                    ]


    for ind, densityFile in enumerate(densityFiles):

        bins, density = getDensityData(densityFile)
        binSizes = [x[1] - x[0] for x in bins]
        shiftSizes = [int(round(ACFStepSize / x)) for x in binSizes]
        bb = getMinBoundingBox(density)
        # print(bb)
        shiftBounds = [(0.5 * (x[0] - x[1]), 0.5 * (x[1] - x[0])) for x in bb]
        shiftBoundsRoundedUp = np.sign(shiftBounds) * np.ceil(np.abs(shiftBounds) / ACFStepSize) * ACFStepSize
        print(shiftBoundsRoundedUp)
        shifts = [np.arange(bounds[0], bounds[1], stepSize)
                  for bounds, stepSize in zip(shiftBoundsRoundedUp, shiftSizes)]
        print(time.asctime())
        t1 = time.time()
        # shifts, acf = calcACF(density, bins)
        shifts, acf = calcACF(density, shifts)
        print(time.asctime())
        t2 = time.time()
        print(t2 - t1)

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 11.2))
        ax[0].imshow(acf.max(axis=2), vmax=1, vmin=0, interpolation='None')
        ax[0].set_ylabel('X')
        ax[0].set_xlabel('Y')
        im1 = ax[1].imshow(acf.max(axis=1), vmax=1, vmin=0, interpolation='None')
        ax[1].set_ylabel('X')
        ax[1].set_xlabel('Z')
        ax[1].set_title('Sharpness(' + str(minAC) + '): ' + str((acf >= minAC).sum()))

        fig.colorbar(im1, ax=ax[1], use_gridspec=True)

        fig.tight_layout()
        fig.canvas.draw()

        fig.savefig(densityFile[:-4] + '_ACR.jpg', dpi=300)
        np.savez(densityFile[:-4] + '_ACR', shifts=shifts, acf=acf)


