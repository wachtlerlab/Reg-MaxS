import json
import numpy as np
import pandas as pd
from statsmodels.sandbox.descstats import sign_test
import os


def pairwiseDistanceStats(parFile, anisotropicScalingThresh):


    with open(parFile) as fle:
        parsList = json.load(fle)

    transErrs = pd.DataFrame()
    signStats = pd.DataFrame()
    allSizes = []
    allThreshs = []


    for parInd, par in enumerate(parsList):

        refSWC = par['refSWC']
        resFile = par['resFile']
        testSWC = par['testSWC']

        testName = resFile[:-4]
        thresh = par['gridSizes'][-1]

        print(('Doing ' + repr((refSWC, resFile))))

        refPts = np.loadtxt(refSWC)[:, 2:5]
        testPtsFull = np.loadtxt(resFile)
        testPts = testPtsFull[:, 2:5]


        if refPts.shape[0] != testPts.shape[0]:

            print(('Number of points do not match for ' + refSWC + 'and' + resFile))
            continue

        allSizes.append(refPts.shape[0])
        allThreshs.append(thresh)
        ptDiff = np.linalg.norm(refPts - testPts, axis=1)

        origJSON = testSWC[:-4] + '.json'

        if os.path.isfile(origJSON):
            with open(origJSON, 'r') as fle:
                pars = json.load(fle)
                scales = np.array(pars['scale'])
        else:
            raise IOError

        scalesOrdered = np.sort(scales)
        scalesRelative = np.mean([scalesOrdered[0] / scalesOrdered[1],
                                  scalesOrdered[0] / scalesOrdered[2],
                                  scalesOrdered[1] / scalesOrdered[2]])
        tempDF = pd.DataFrame()
        tempDF['Pairwise Distance in $\mu$m'] = ptDiff
        tempDF['Exp. Name'] = testName
        tempDF["Node ID"] = testPtsFull[:, 0]
        tempDF['Anisotropic Scaling Level'] = scalesRelative

        transErrs = transErrs.append(tempDF, ignore_index=True)

        t, p = sign_test(ptDiff, thresh)
        oneSidedP = 0.5 * p
        signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.01

        notSignFartherThanSVS = not (t > 0 and oneSidedP < 0.01)

        tempDict = {"Job Number": parInd, "resFile": resFile, "refSWC": refSWC,
                    "t Statistic": t, "One Sided p value": oneSidedP,
                    "Pairwise distance significantly smaller than smallest voxel size":
                        signCloserThanSmallestVoxelSize,
                    "Pairwise distance not significantly larger than smallest voxel size":
                        notSignFartherThanSVS,
                    "Anisotropic Scaling Level": scalesRelative
                    }
        signStats = signStats.append(tempDict, ignore_index=True)


    allEqualSizeThresh = (allSizes.count(allSizes[0]) == len(allSizes)) and \
                         (allThreshs.count(allThreshs[0]) == len(allThreshs))

    nodeWiseStatsDF = pd.DataFrame()

    if allEqualSizeThresh:

        transErrsAnisoThresh = transErrs.loc[transErrs['Anisotropic Scaling Level'] >= anisotropicScalingThresh, :]
        transErrsGBNodeID = transErrs.groupby("Node ID")
        transErrsGBNodeIDAnisoThresh = transErrsAnisoThresh.groupby("Node ID")

        for nodeInd, (node, nodeDistsDF) in enumerate(transErrsGBNodeID):

            print(("Doing node {}, {} of {}".format(node, nodeInd, len(transErrsGBNodeID.indices))))
            nodeDistsAll = nodeDistsDF['Pairwise Distance in $\mu$m'].astype(float)
            t, p = sign_test(nodeDistsAll, allThreshs[0])
            oneSidedP = 0.5 * p
            signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.05

            notSignFartherThanSVS = not (t > 0 and oneSidedP < 0.01)

            tempDict = {
                "[All] Pairwise distance significantly smaller than smallest voxel size": signCloserThanSmallestVoxelSize,
                "[All] Pairwise distance not significantly larger than smallest voxel size": notSignFartherThanSVS
                        }

            nodeDistsDFAnisoFiltered = transErrsGBNodeIDAnisoThresh.get_group(node)
            nodeDistsAnisoFiltered = nodeDistsDFAnisoFiltered['Pairwise Distance in $\mu$m'].astype(float)
            t, p = sign_test(nodeDistsAnisoFiltered,
                               allThreshs[0])
            oneSidedP = 0.5 * p
            signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.01

            notSignFartherThanSVS = not (t > 0 and oneSidedP < 0.01)

            tempDict["[AnisoFiltered] Pairwise distance significantly smaller than smallest voxel size"] =\
                signCloserThanSmallestVoxelSize
            tempDict["[AnisoFiltered] Pairwise distance not significantly larger than smallest voxel size"]=\
                notSignFartherThanSVS

            nodeWiseStatsDF = nodeWiseStatsDF.append(tempDict, ignore_index=True)

        nodesCloserThanCount = nodeWiseStatsDF["[All] Pairwise distance significantly smaller than smallest voxel size"].sum()
        nodesNotFartherThanCount = nodeWiseStatsDF["[All] Pairwise distance not significantly larger than smallest voxel size"].sum()

        nodesCloserThanCountAniso = nodeWiseStatsDF["[AnisoFiltered] Pairwise distance significantly smaller than smallest voxel size"].sum()
        nodesNotFartherThanCountAniso = nodeWiseStatsDF["[AnisoFiltered] Pairwise distance not significantly larger than smallest voxel size"].sum()

        print(("[All] Nodes with pairwise distance "
              "significantly smaller "
              "than lowest voxel size: {} out of {}, {}%".format(nodesCloserThanCount,
                                                            nodeWiseStatsDF.shape[0],
                                                                 100 * nodesCloserThanCount / nodeWiseStatsDF.shape[0])))
        print(("[All] Nodes with pairwise distance "
              "not significantly larger "
              "than lowest voxel size: {} out of {}, {}%".format(nodesNotFartherThanCount,
                                                            nodeWiseStatsDF.shape[0],
                                                            100 * nodesNotFartherThanCount / nodeWiseStatsDF.shape[0])))
        print(("[Aniso] Nodes with pairwise distance "
              "significantly smaller "
              "than lowest voxel size: {} out of {}, {}%".format(nodesCloserThanCountAniso,
                                                            nodeWiseStatsDF.shape[0],
                                                                 100 * nodesCloserThanCountAniso / nodeWiseStatsDF.shape[0])))
        print(("[Aniso] Nodes with pairwise distance "
              "not significantly larger "
              "than lowest voxel size: {} out of {}, {}%".format(nodesNotFartherThanCountAniso,
                                                            nodeWiseStatsDF.shape[0],
                                                            100 * nodesNotFartherThanCountAniso / nodeWiseStatsDF.shape[0])))

        signStatsAniso = signStats.loc[signStats["Anisotropic Scaling Level"] > anisotropicScalingThresh, :]
        signCloserThanAniso = signStatsAniso["Pairwise distance significantly smaller than smallest voxel size"]
        signCloserThanCountAniso = signCloserThanAniso.sum()

        notSignFartherAniso = signStatsAniso["Pairwise distance not significantly larger than smallest voxel size"]
        notSignFartherCountAniso = notSignFartherAniso.sum()

        print(("[Aniso Filtered] Jobs with "
              "pairwise distance "
              "significantly smaller "
              "than lowest voxel size: {} out of {}, {}%".format(signCloserThanCountAniso,
                                                            signStatsAniso.shape[0],
                                                            100 * signCloserThanCountAniso / signStatsAniso.shape[0])))
        print(("[Aniso Filtered] Jobs with "
              "pairwise distance "
              "not significantly larger "
              "than lowest voxel size: {} out of {}, {}%".format(notSignFartherCountAniso,
                                                            signStatsAniso.shape[0],
                                                                 100 * notSignFartherCountAniso / signStatsAniso.shape[0])))


    signCloserThan = signStats["Pairwise distance significantly smaller than smallest voxel size"]
    signCloserThanCount = signCloserThan.sum()

    notSignFarther = signStats["Pairwise distance not significantly larger than smallest voxel size"]
    notSignFartherCount = notSignFarther.sum()

    print(("[All] Jobs with "
          "pairwise distance "
          "significantly smaller "
          "than lowest voxel size: {} out of {}, {}%".format(signCloserThanCount, len(parsList),
                                                             100 * signCloserThanCount / len(parsList))))
    print(("[All] Jobs with "
          "pairwise distance "
          "not significantly larger "
          "than lowest voxel size: {} out of {}, {}%".format(notSignFartherCount, len(parsList),
                                                             100 * notSignFartherCount / len(parsList))))


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, 'Improper usage! Please use as \n' \
                               '\'python plotPairwiseDistance.py parFile <anisotropic scaling Thresholdx>\''

    parFile = sys.argv[1]
    figs = pairwiseDistanceStats(parFile, float(sys.argv[2]))

