from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from .swcFuncs import readSWC_numpy
import numpy as np
from pyemd import emd

def cdist_1d_centripetal(list1, list2, center):
    """
    Return a matrix of pairwise displacements of entries of list1 from corresponding
     entries in list2, with displacements
    towards center having positive value and those away having negative values
    :param list1: iterable of floats or ints
    :param list2: iterable of floats or ints
    :param center: float or int
    :return: numpy.ndarray of shape (<len of list1>, <len of list2>)
    """

    assert all([isinstance(x, (float, int)) for x in list1])
    assert all([isinstance(x, (float, int)) for x in list2])
    assert isinstance(center, (float, int))

    mesh2 = np.array([list2] * len(list1))
    mesh1 = np.array([list1] * len(list2)).T

    mesh1CenteredAbs = np.abs(mesh1 - center)
    mesh2CenteredAbs = np.abs(mesh2 - center)

    return mesh2CenteredAbs - mesh1CenteredAbs

def calcMaxDistances(swcList):
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
    distMatrix = cdist(unionWithDuplicates, vertices)
    maxDistances = distMatrix.max(axis=1).tolist()

    return maxDistances


def maxDistEMD(swcList):
    """
    Calculate the maxDistance based metric. It is the size normalized Earth mover distance
    between the distribution of maxDistances (see calcMaxDistances above)
    of the pooled collection of points of all swcs in swcList and the distribution of
    pooled diagonal maxDistances of individual swcs in swcList
    :param swcList: list of valid swc files on the system, list of strings
    :return: float
    """

    individualMaxDistances = [calcMaxDistances([swc]) for swc in swcList]
    pooledIndividualMaxDistances = np.concatenate(individualMaxDistances, axis=0)

    meanPIMD = pooledIndividualMaxDistances.mean()

    PIMDNorm = (pooledIndividualMaxDistances - meanPIMD) / meanPIMD

    maxDistancesAllPts = np.array(calcMaxDistances(swcList))

    MDAPNorm = (maxDistancesAllPts - meanPIMD) / meanPIMD

    binWidth = 1 / meanPIMD

    bins = np.arange(MDAPNorm.min() - 0.5 * binWidth,
                     MDAPNorm.max() + 0.5 * binWidth,
                     binWidth)

    hist1, bins1 = np.histogram(MDAPNorm, bins)
    hist2, bins2 = np.histogram(PIMDNorm, bins1)

    hist1Normed = hist1 / float(hist1.sum())
    hist2Normed = hist2 / float(hist2.sum())

    dist_metric = cdist_1d_centripetal(bins1, bins2, center=0)
    emd_val = emd(np.asarray(hist2Normed, dtype=np.float64), np.asarray(hist1Normed, dtype=np.float64),
                  np.asarray(dist_metric, dtype=np.float64))

    return emd_val