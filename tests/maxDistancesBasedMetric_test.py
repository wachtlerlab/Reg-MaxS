from regmaxsn.core.maxDistanceBasedMetric import calcMaxDistanceDistribution, maxDistEMD, cdist_1d
import numpy as np

def calcMaxDistances_test():
    """Testing the calculation of maximum distances"""

    testFiles = [
        "tests/testFiles/toy1.swc",
        "tests/testFiles/toy2.swc"
        ]

    maxDistances = calcMaxDistanceDistribution(testFiles)
    assert np.allclose(maxDistances, np.array([ 73.37574531,  54.77225575,  53.85164807,  51.6139516 ,
        55.71355311,  62.80127387,  62.80127387,  73.37574531]), atol=1e-8)


def maxDistEMD_test():
    """Testing the calculation of EMD of maxDistances"""

    swcList1 = ["tests/testFiles/toy2.swc"]
    swcList2 = ["tests/testFiles/toy1.swc",
                "tests/testFiles/toy2.swc"]
    emd_val = maxDistEMD(swcList1, swcList2)
    assert False


def cdist_1d_test():
    "Testing cdist_1d"

    assert np.allclose(cdist_1d([1, 2, 3], [1, 2]), np.array([[0, 1], [-1, 0], [-2, -1]]))
