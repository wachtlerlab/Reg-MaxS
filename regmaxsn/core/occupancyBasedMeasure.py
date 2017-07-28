import numpy as np
from collections import Counter
from pyemd import emd

def calcOccupancyDistribution(swcList, voxelSize):
    """
    Returns the distribution of the sum of voxel occupancies across swcs in swcList.
    Voxel occupancy of a voxel is 1 if an swc has an node in the voxel, otherwise 0.
    :param swcList: list of valid SWC files on the file system
    :param voxelSize: float, voxel size to discretize space.
    :return: dict with voxel occupancy and its normalized frequency as key-value pairs
    """

    voxels = []
    for swc in swcList:
        aPts = np.loadtxt(swc)[:, 2:5]
        aVox = np.array(aPts / voxelSize, np.int32)
        aVoxSet = set(map(tuple, aVox))
        voxels.extend(list(aVoxSet))

    voxelCounter = Counter(voxels)
    counts = voxelCounter.values()

    bins = np.arange(1, len(swcList) + 2) - 0.5

    hist, bins = np.histogram(counts, bins)

    histNormed = hist / float(sum(hist))

    return dict(zip(np.arange(1, len(swcList) + 1), histNormed))


def occupancyEMD(swcList, voxelSize):
    """
    Calculate the EMD between the occupancy distributions (see calcOccupancyDistribution above) of
    swcList and that of perfect overlap (1 at len(swcList) and zero elsewhere)
    :param swcList: list of valid SWC files on the file system
    :param voxelSize: float, voxel size for discretizing space.
    :return: float, emd value
    """

    occupancyDistributionDict = calcOccupancyDistribution(swcList, voxelSize)
    bins = np.arange(1, len(swcList) + 1)
    occupancyDistribution = [occupancyDistributionDict[x] for x in bins]
    perfectOverlapDist = np.zeros(bins.shape)
    perfectOverlapDist[-1] = 1

    binsRow = bins.reshape((1, bins.shape[0]))
    distMetric = np.dot(np.ones((bins.shape[0], 1)), binsRow) - binsRow.T

    emd_val = emd(np.asarray(occupancyDistribution, dtype=np.float64),
                  np.asarray(perfectOverlapDist, dtype=np.float64),
                  np.asarray(distMetric, dtype=np.float64))
    return emd_val


