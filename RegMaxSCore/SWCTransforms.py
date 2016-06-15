import os
import numpy as np
from transforms import compose_matrix
from swcFuncs import readSWC_numpy, writeSWC_numpy


def three32BitInt2complexList(arr):
    assert arr.dtype == np.int32, 'Only 32 bit ints allowed'
    assert arr.shape[1] == 3, 'only three ints per row allowed'
    temp = np.zeros((arr.shape[0], 4), dtype=np.int32)
    temp[:, 1:] = arr
    temp1 = temp.view(np.int64)
    j = complex(0, 1)
    return (temp1[:, 0] + j * temp1[:, 1]).tolist()


def objFun(y):

    x, data = y
    nrnPtsTrans = data.transform(x, data.SWC2AlignPts)
    nrnVox = np.array(np.round(nrnPtsTrans / data.gridSize), np.int32)
    nrnVoxSet = set(three32BitInt2complexList(nrnVox))
    nInter = len(nrnVoxSet.intersection(data.refVoxSet))
    nUnion = len(nrnVoxSet) + len(data.refVoxSet) - nInter
    sumOfDiffs = 1 - (nInter / float(nUnion))

    return sumOfDiffs



class BaseSWCTranform(object):

    def __init__(self, refSWC, SWC2Align, gridSize):

        super(BaseSWCTranform, self).__init__()

        if os.path.isfile(refSWC) and refSWC.endswith('.swc'):
            self.refSWCPts = np.loadtxt(refSWC)[:, 2:5]
        elif type(refSWC) == np.ndarray:
            self.refSWCPts = refSWC[:, 2:5]
        else:
            raise(ValueError('Unknown data in SWC2Align'))

        self.refCenter = self.refSWCPts.mean(axis=0)
        refVox = np.array(np.round(self.refSWCPts / gridSize), np.int32)
        self.gridSize = gridSize
        self.refVoxSet = set(three32BitInt2complexList(refVox))

        if os.path.isfile(SWC2Align) and SWC2Align.endswith('.swc'):
            self.headr, self.SWC2AlignFull = readSWC_numpy(SWC2Align)
        elif type(SWC2Align) == np.ndarray:
            assert type(SWC2Align['data']) == np.ndarray, 'Unknown data in SWC2Align'
            self.SWC2AlignFull = SWC2Align
            self.headr = ''
        else:
            raise(ValueError('Unknown data in SWC2Align'))
        self.SWC2AlignPts = self.SWC2AlignFull[:, 2:5]
        self.center = self.SWC2AlignPts.mean(axis=0)

    def transform(self, pars, data):

        return data

    def writeSolution(self, outFile, bestSol, inFile=None):

        if inFile:
            headr, data = readSWC_numpy(inFile)
        else:
            headr, data = self.headr, self.SWC2AlignFull

        data[:, 2:5] = self.transform(bestSol, data[:, 2:5])

        writeSWC_numpy(outFile, data, headr)


class SWCTranslate(BaseSWCTranform):

    def __init__(self, refSWC, SWC2Align, gridSize):

        super(SWCTranslate, self).__init__(refSWC, SWC2Align, gridSize)

    def transform(self, pars, data):

        return data + pars


class SWCRotate(BaseSWCTranform):

    def __init__(self, refSWC, SWC2Align, gridSize):

        super(SWCRotate, self).__init__(refSWC, SWC2Align, gridSize)


    def transform(self, pars, data):

        rotMat = compose_matrix(angles=pars)
        dataCentered = data - self.center
        return np.dot(rotMat[:3, :3], dataCentered.T).T + self.center


class SWCScale(object):

    def __init__(self, refSWC, SWC2Align, gridSize):

        super(SWCScale, self).__init__()

        self.gridSize = gridSize

        if os.path.isfile(refSWC) and refSWC.endswith('.swc'):
            self.refSWCPts = np.loadtxt(refSWC)[:, 2:5]
        elif type(refSWC) == np.ndarray:
            self.refSWCPts = refSWC[:, 2:5]
        else:
            raise(ValueError('Unknown data in SWC2Align'))

        refCenter = self.refSWCPts.mean(axis=0)
        refSWCPtsCentered = self.refSWCPts - refCenter
        refVox = np.array(np.round(refSWCPtsCentered / gridSize), np.int32)
        self.refVoxSet = set(three32BitInt2complexList(refVox))

        if os.path.isfile(SWC2Align) and SWC2Align.endswith('.swc'):
            self.headr, self.SWC2AlignFull = readSWC_numpy(SWC2Align)
        elif type(SWC2Align) == np.ndarray:
            assert type(SWC2Align['data']) == np.ndarray, 'Unknown data in SWC2Align'
            self.SWC2AlignFull = SWC2Align
            self.headr = ''
        else:
            raise(ValueError('Unknown data in SWC2Align'))

        self.SWC2AlignPts = self.SWC2AlignFull[:, 2:5].copy()
        self.center = self.SWC2AlignPts.mean(axis=0)
        self.SWC2AlignPts -= self.center



    def transform(self, pars, data):

        rotMat = compose_matrix(scale=pars)
        dataCentered = data
        return np.dot(rotMat[:3, :3], dataCentered.T).T

    def writeSolution(self, outFile, bestSol, inFile=None):

        if inFile:
            headr, data = readSWC_numpy(inFile)
        else:
            headr, data = self.headr, self.SWC2AlignFull

        data[:, 2:5] = self.transform(bestSol, data[:, 2:5] - self.center) + self.center

        writeSWC_numpy(outFile, data, headr)



class ArgGenIterator:

    def __init__(self, arg1, arg2):

        self.arg1 = arg1
        self.arg2 = arg2
        self.pointsDone = 0

    def __iter__(self):

        self.pointsDone = 0
        return self

    def next(self):

        if self.pointsDone < len(self.arg1):
            toReturn = (self.arg1[self.pointsDone], self.arg2)
            self.pointsDone += 1
            return toReturn
        else:
            raise StopIteration





































