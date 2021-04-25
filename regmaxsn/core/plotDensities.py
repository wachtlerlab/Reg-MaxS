from .swcFuncs import resampleSWC, digitizeSWCXYZ, getPCADetails, readSWC_numpy, writeSWC_numpy
import numpy as np
import os
from scipy.ndimage import gaussian_filter
import tifffile


class DensityVizualizations(object):

    def __init__(self, swcSet, gridUnitSizes, resampleLen,
                 masks=None, pcaView=None, refSWC=None, initTrans=None):
        if initTrans is None:
            initTrans = np.eye(3)

        self.gridUnitSizes = np.array(gridUnitSizes)

        if masks is None:
            masks = [None] * len(swcSet)
        else:
            assert len(masks) == len(swcSet), 'Improper value for masks1'


        minXYZs = []
        maxXYZs = []
        self.transMat = np.eye(4)
        datas = {}

        for swcInd, swcFile in enumerate(swcSet):
            print(('Resamping ' + swcFile))
            totalLen, data = resampleSWC(swcFile, resampleLen, mask=masks[swcInd])
            dataT = np.dot(initTrans, data[:, :3].T).T
            datas[swcFile] = dataT
        self.transMat[:3, :3] = initTrans

        allData = np.concatenate(tuple(datas.values()), axis=0)
        self.allDataMean = allData.mean(axis=0)

        if pcaView == 'closestPCMatch':
            evecs, newStds = getPCADetails(None, center=True, data=allData)
            mean2Use = self.allDataMean

            if refSWC:
                refEvecs, thrash = getPCADetails(refSWC, center=True)
                fEvecs = np.empty_like(refEvecs)
                coreff = np.dot(refEvecs.T, evecs)
                possInds = list(range(refEvecs.shape[1]))
                for rowInd in range(refEvecs.shape[1]):
                    bestCorrInd = np.argmax(np.abs(coreff[rowInd, possInds]))
                    fEvecs[:, rowInd] = np.sign(coreff[rowInd, possInds[bestCorrInd]]) * evecs[:, possInds[bestCorrInd]]
                    possInds.pop(int(bestCorrInd))



            else:
                fEvecs = evecs

        elif pcaView == 'assumeRegistered':

            if refSWC:
                refEvecs, thrash = getPCADetails(refSWC, center=True)
                fEvecs = refEvecs
                mean2Use = np.loadtxt(refSWC)[:, 2:5].mean(axis=0)

            else:
                raise ValueError('RefSWC must be specified when pcaView == \'assumeRegistered\'')

        else:
            fEvecs = np.eye(3)
            mean2Use = self.allDataMean


        self.digDatas = {}
        for swcFile, data in datas.items():
            print(('Digitizing ' + swcFile))
            data -= mean2Use
            data = np.dot(fEvecs.T, data.T).T
            digData = digitizeSWCXYZ(data + mean2Use, gridUnitSizes)
            self.digDatas[swcFile] = digData
            minXYZs.append(digData[:, :3].min(axis=0))
            maxXYZs.append(digData[:, :3].max(axis=0))

        temp = np.eye(4)
        temp[:3, 3] = -mean2Use
        self.transMat = np.dot(temp, self.transMat)

        temp = np.eye(4)
        temp[:3, :3] = fEvecs.T
        self.transMat = np.dot(temp, self.transMat)

        self.transMat[:3, 3] += mean2Use

        self.minXYZ = np.array(minXYZs).min(axis=0) - 20
        self.maxXYZ = np.array(maxXYZs).max(axis=0) + 20

        self.bins = [np.arange(x, y + 1) * z for x, y, z in zip(self.minXYZ, self.maxXYZ, self.gridUnitSizes)]



    def calculateDensity(self, swcFiles, sigmas):

        assert all(np.greater_equal(sigmas, self.gridUnitSizes)), 'sigma along every dimenstion must be larger than gridUnitSize'

        digSigs = np.around(np.array(sigmas) / self.gridUnitSizes)

        densityMatSum = np.zeros(tuple((self.maxXYZ - self.minXYZ).tolist()))


        for swcFile in swcFiles:

            print(('Calculating Density for ' + swcFile))
            densityMat = np.zeros_like(densityMatSum)
            print(('Doing ' + os.path.split(swcFile)[1]))
            if swcFile in self.digDatas:
                digDataTranslated = self.digDatas[swcFile][:, :3] - self.minXYZ
            else:
                raise ValueError(swcFile + ' not initialized in constructing DensityVizualizations object')
            densityMat[digDataTranslated[:, 0], digDataTranslated[:, 1], digDataTranslated[:, 2]] = 1
            densityMatSum += densityMat
            del densityMat

        densityMatSum /= float(len(swcFiles))
        smoothDensityMat = gaussian_filter(densityMatSum, sigma=digSigs, truncate=3)
        del densityMatSum
        smoothDensityMat *= (2 ** 1.5) * digSigs.prod()

        smoothDensityMat[smoothDensityMat > 1] = 1
        smoothDensityMat[smoothDensityMat < 0] = 0

        return smoothDensityMat, self.bins

    def generateDensityColoredSSWC(self, swcFiles, outFiles, density=None, sigmas=None):

        if density is None:
            density, bins = self.calculateDensity(swcFiles, sigmas)

        for swcInd, swcFile in enumerate(swcFiles):

            headr, data = readSWC_numpy(swcFile)
            dataXYZ = data[:, 2:5]
            rotData = np.dot(self.transMat[:3, :3], dataXYZ.T).T + self.transMat[:3, 3]
            digData = digitizeSWCXYZ(rotData, self.gridUnitSizes)
            digDataTranslated = digData - self.minXYZ
            colorInds = [density[x[0], x[1], x[2]] for x in digDataTranslated]
            colorInds = np.reshape(colorInds, (len(colorInds), 1))
            colorInds[colorInds > 1] = 1
            colorInds[colorInds < 0] = 0

            # data[:, 2:5] = rotData
            outData = np.concatenate((data, colorInds), axis=1)

            writeSWC_numpy(outFiles[swcInd], outData, headr)


def writeTIFF(density, outFile):

    assert type(density) is np.ndarray, 'density must be a numpy ndarray'
    assert len(density.shape) == 3, 'density must a 3d numpy array'
    densityUInt8 = np.array(density * 255, dtype=np.uint8)
    tiffArgs = {
                'compress': 0,
                # 'planarconfig': 'planar',
                'photometric': 'minisblack'
                }
    tifffile.imsave(outFile + '.tiff', densityUInt8, **tiffArgs)