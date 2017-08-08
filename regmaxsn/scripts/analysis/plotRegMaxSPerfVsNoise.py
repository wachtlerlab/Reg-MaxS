import os
import json
import numpy as np
import pandas as pd
from statsmodels.sandbox.descstats import sign_test
from matplotlib import pyplot as plt
from regmaxsn.core.matplotlibRCParams import mplPars
import seaborn as sns

sns.set(rc=mplPars)


def regmaxsPerfVsNoise(parFile, anisoThresh):
    plt.ion()

    with open(parFile) as fle:
        parsList = json.load(fle)

    transErrs = pd.DataFrame()
    perfDF = pd.DataFrame()

    for parInd, par in enumerate(parsList):

        refSWC = par['refSWC']
        resFile = par['resFile']
        testSWC = par["testSWC"]

        if testSWC.find("NoiseStd") < 0:
            print("{} has testSWC {} without noise.Ignoring it!".format(parFile, testSWC))
        else:

            NoiseStdStrInd = testSWC.find("NoiseStd")
            RandTransStdInd = testSWC.find("RandTrans")

            noiseStd = int(testSWC[NoiseStdStrInd + 8: RandTransStdInd])

            origJSON = '{}{}.json'.format(testSWC[:NoiseStdStrInd], testSWC[RandTransStdInd:-4])

            if os.path.isfile(origJSON):
                with open(origJSON, 'r') as fle:
                    pars = json.load(fle)
                    scales = np.array(pars['scale'])
            else:
                raise (IOError('File not found: {}'.format(origJSON)))

            scalesOrdered = np.sort(scales)
            scalesRelative = np.mean([scalesOrdered[0] / scalesOrdered[1],
                                      scalesOrdered[0] / scalesOrdered[2],
                                      scalesOrdered[1] / scalesOrdered[2]])


            testName = resFile[:-4]
            thresh = par['gridSizes'][-1]

            print('Doing ' + repr((refSWC, resFile)))

            refPts = np.loadtxt(refSWC)[:, 2:5]
            testPtsFull = np.loadtxt(resFile)
            testPts = testPtsFull[:, 2:5]


            if refPts.shape[0] != testPts.shape[0]:

                print('Number of points do not match for ' + refSWC + 'and' + resFile)
                continue


            ptDiff = np.linalg.norm(refPts - testPts, axis=1)

            transErrs = transErrs.append(pd.DataFrame({'Pairwise Distance in $\mu$m': ptDiff,
                                          'Exp. Name': testName,
                                          "Node ID": testPtsFull[:, 0],
                                          "Noise Std": noiseStd}),
                                         ignore_index=True)

            t, p = sign_test(ptDiff, thresh)
            oneSidedP = 0.5 * p
            signCloserThanSmallestVoxelSize = t < 0 and oneSidedP < 0.05

            notSignFartherThanSVS = not (t > 0 and oneSidedP < 0.01)


            tempDict = {"Job Number": parInd, "resFile": resFile, "refSWC": refSWC,
                        "t Statistic": t, "One Sided p value": oneSidedP,
                        "Pairwise distance significantly smaller than smallest voxel size":
                            signCloserThanSmallestVoxelSize,
                        "Pairwise distance not significantly larger than smallest voxel size":
                            notSignFartherThanSVS,
                        "Noise Std": noiseStd,
                        "Level of Anisotropic scaling": scalesRelative}
            perfDF = perfDF.append(tempDict, ignore_index=True)

    perfDFAnisoFiltered = perfDF.loc[perfDF["Level of Anisotropic scaling"] > anisoThresh, :]
    perfNoiseDF = perfDFAnisoFiltered[["Noise Std", "Pairwise distance significantly smaller than smallest voxel size"]]
    perfVsNoise = perfNoiseDF.groupby("Noise Std").agg(lambda x: 100 * x.sum() / float(x.shape[0]))
    worstPerfNoiseDF = perfDFAnisoFiltered[["Noise Std", "Pairwise distance not significantly larger than smallest voxel size"]]
    worstPerfVsNoise = worstPerfNoiseDF.groupby("Noise Std").agg(lambda x: 100 * x.sum() / float(x.shape[0]))

    fig, ax = plt.subplots(figsize=(14, 11.2))
    # ax.bar(perfVsNoise.index.values, perfVsNoise.values, width=1.5)
    ax.plot(perfVsNoise.index.values, perfVsNoise.values, 'r-o',
            label="\% of tests with significant number \nof pairwise distances smaller than \nlowest voxel size")
    ax.plot(worstPerfVsNoise.index.values, worstPerfVsNoise.values, 'b-s',
            label="\% of tests with significant number \nof pairwise distances not greater than \nlowest voxel size")
    ax.set_xticks(perfVsNoise.index.values)
    ax.set_xlabel("Noise Standard deviation ($\mu$ m)")
    ax.legend(loc='best')
    ax.set_ylim(-10, 110)
    fig.tight_layout()
    return fig

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, 'Improper usage! Please use as \n' \
                               '\'python {} <parFile> <minimum allowed level of anisotropic scaling>\''.format(sys.argv[1])

    parFile = sys.argv[1]
    anisoThesh = float(sys.argv[2])
    fig = regmaxsPerfVsNoise(parFile, anisoThesh)
    raw_input("Press any key to close the figure and exit....")