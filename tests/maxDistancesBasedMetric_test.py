from regmaxsn.core.maxDistanceBasedMetric import calcMaxDistances, maxDistEMD, cdist_1d_centripetal
import numpy as np


def calcMaxDistances_test():
    """Testing the calculation of maximum distances"""

    testFiles = [
        "tests/testFiles/toy1.swc",
        "tests/testFiles/toy2.swc"
        ]

    maxDistances = calcMaxDistances(testFiles)
    assert np.allclose(maxDistances, np.array([73.37574531,  54.77225575,  53.85164807,
                                               51.6139516, 55.71355311,  62.80127387,
                                               62.80127387,  73.37574531]))


def maxDistEMD_test():
    """Testing the calculation of EMD of maxDistances"""

    swcList1 = ["tests/testFiles/toy2.swc",
                "tests/testFiles/toy3.swc"]
    emd_val = maxDistEMD(swcList1)
    assert np.allclose(emd_val, 35.99999099999999)


def cdist_1d_test():
    "Testing cdist_1d"

    temp = cdist_1d_centripetal([1, 2, 3], [1, 2], center=2)
    assert np.allclose(temp,
                       np.array([[0, -1], [1, 0], [0, -1]]))


if __name__ == "__main__":
    maxDistEMD_test()