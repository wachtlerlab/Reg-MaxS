import os
import json
import numpy as np
import pandas as pd
from statsmodels.sandbox.descstats import sign_test

homeFolder = os.path.expanduser('~')


def pairwiseDistanceStats(parFile):


    with open(parFile) as fle:
        parsList = json.load(fle)

    transErrs = pd.DataFrame()
    signCloserThanSmalledVoxelSizeDF = pd.DataFrame()
    allSizes = []
    allThreshs = []
    passCount = 0

    for parInd, par in enumerate(parsList):

        refSWC = par['refSWC']
        resFile = par['resFile']

        testName = resFile[:-4]
        thresh = par['gridSizes'][-1]

        print('Doing ' + repr((refSWC, resFile)))

        refPts = np.loadtxt(refSWC)[:, 2:5]
        testPtsFull = np.loadtxt(resFile)
        testPts = testPtsFull[:, 2:5]


        if refPts.shape[0] != testPts.shape[0]:

            print('Number of points do not match for ' + refSWC + 'and' + resFile)
            continue

        allSizes.append(refPts.shape[0])
        allThreshs.append(thresh)
        ptDiff = np.linalg.norm(refPts - testPts, axis=1)

        transErrs = transErrs.append(pd.DataFrame({'Pairwise Distance in $\mu$m': ptDiff,
                                      'Exp. Name': testName,
                                      "Node ID": testPtsFull[:, 0]}),
                                     ignore_index=True)

        t, p = sign_test(ptDiff, thresh)
        oneSidedP = 0.5 * p
        signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.05

        if signCloserThanSmallestVoxelSize:
            passCount += 1

        tempDict = {"Job Number": parInd, "resFile": resFile, "refSWC": refSWC,
                    "t Statistic": t, "One Sided p value": oneSidedP,
                    "Pairwise distance significantly smaller than than {}".format(thresh):
                        signCloserThanSmallestVoxelSize}
        signCloserThanSmalledVoxelSizeDF = signCloserThanSmalledVoxelSizeDF.append(tempDict,
                                                                                   ignore_index=True)

    print("Jobs with "
          "pairwise distance "
          "significantly smaller "
          "than lowest voxel size: {} out of {}".format(passCount, len(parsList)))

    allEqualSizeThresh = (allSizes.count(allSizes[0]) == len(allSizes)) and \
                         (allThreshs.count(allThreshs[0]) == len(allThreshs))

    nodeWiseSignCloserThanSmallestVoxelSize = []
    if allEqualSizeThresh:

        transErrsGBNodeID = transErrs.groupby("Node ID")

        for nodeInd, (node, nodeDistsDF) in enumerate(transErrsGBNodeID):

            print("Doing node {}, {} of {}".format(node, nodeInd, len(transErrsGBNodeID.indices)))
            t, p = sign_test(nodeDistsDF['Pairwise Distance in $\mu$m'].astype(float), allThreshs[0])
            oneSidedP = 0.5 * p
            signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.05
            nodeWiseSignCloserThanSmallestVoxelSize.append(signCloserThanSmallestVoxelSize)

        print("Jobs with "
              "pairwise distance "
              "significantly smaller "
              "than lowest voxel size: {} out of {}".format(passCount, len(parsList)))

        print("Nodes with pairwise distance "
          "significantly smaller "
          "than lowest voxel size: {} out of {}".format(sum(nodeWiseSignCloserThanSmallestVoxelSize),
                                                        len(nodeWiseSignCloserThanSmallestVoxelSize)))


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python plotPairwiseDistance.py parFile\''

    parFile = sys.argv[1]
    figs = pairwiseDistanceStats(parFile)

