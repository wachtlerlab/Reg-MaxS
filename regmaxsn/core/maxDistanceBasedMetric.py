from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from .swcFuncs import readSWC_numpy
import numpy as np
from pyemd import emd

def cdist_1d(list1, list2):
    """
    Return a matrix of pairwise distances between entries of list1 and list2
    :param list1: iterable of floats or ints
    :param list2: iterable of floats or ints
    :return: numpy.ndarray of shape (<len of list1>, <len of list2>)
    """

    assert all([isinstance(x, (float, int)) for x in list1])
    assert all([isinstance(x, (float, int)) for x in list2])

    return np.array([list2] * len(list1)) - np.array(list1).reshape((len(list1), 1))


def calcMaxDistanceDistribution(swcList):
    """
    Compute the convex hull of the union of points from all swcs in swcList. For each vertex of this
    convex hull, compute the distance of the farthest point among the vertices of the hull and return
    them.
    :param swcList: list of valid SWC files on the file system, list of strings.
    :return: list of maximum distances
    """

    swcPointSets = []
    for swc in swcList:
        headr, swcData = readSWC_numpy(swc)
        swcPointSets.append(swcData[:, 2:5])

    unionWithDuplicates = np.concatenate(swcPointSets, axis=0)
    if any(np.abs(unionWithDuplicates).max(axis=0) == 0):
        raise(ValueError("The list of SWCs all lie on a plane or on  a line and hence do not "
                         "for a 3D point cloud. Such SWCs are not supported."))

    hull = ConvexHull(unionWithDuplicates)

    vertices = unionWithDuplicates[hull.vertices, :]
    distMatrix = cdist(vertices, vertices)
    maxDistances = distMatrix.max(axis=0).tolist()

    return maxDistances


def maxDistEMD(swcList1, swcList2):
    """
    Calculate the Earth mover distance between the distributions of the maximum distances of the
    vertices of the hull each swcList (see calcMaxDistanceDistribution  above.)
    :param swcList1: list of valid swc files on the system, list of strings
    :param swcList2: list of valid swc files on the system, list of strings
    :return: float
    """

    maxDistances1 = calcMaxDistanceDistribution(swcList1)
    maxDistances2 = calcMaxDistanceDistribution(swcList2)

    minMaxDistance = min(maxDistances1 + maxDistances2)
    maxMaxDistance = max(maxDistances1 + maxDistances2)

    binWidth = 1
    bins = np.arange(minMaxDistance - 0.5 * binWidth, maxMaxDistance + 0.5 * binWidth, binWidth)

    hist1, bins1 = np.histogram(maxDistances1, bins)
    hist2, bins2 = np.histogram(maxDistances2, bins)

    emd_val = emd(hist1, hist2, cdist_1d(bins1, bins2))

    return emd_val