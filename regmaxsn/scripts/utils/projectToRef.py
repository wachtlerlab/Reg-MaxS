import sys
from regmaxsn.core.swcFuncs import getPCADetails, writeSWC_numpy
from regmaxsn.core.RegMaxSPars import DensitySaveParNames
from regmaxsn.core.misc import parFileCheck
import numpy as np
import os

def projectToRef(parFile, sourceRefSWC, targetRefSWC, outDir):

    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    parsList = parFileCheck(parFile, DensitySaveParNames)

    refData = np.loadtxt(targetRefSWC)[:, 2:5]
    refEvecs, thrash1 = getPCADetails(None, center=True, data=refData)
    refMean = refData.mean(axis=0)
    refDataNoMean = refData - refMean

    intRefData = np.loadtxt(sourceRefSWC)[:, 2:5]
    intRefEvecs, thrash2 = getPCADetails(None, center=True, data=intRefData)
    intRefMean = intRefData.mean(axis=0)
    intRefDataNoMean = intRefData - intRefMean

    correlation = np.dot(intRefDataNoMean.T, refDataNoMean)
    u, s, v = np.linalg.svd(correlation)

    temp = np.dot(v, u.T)



    for pars in parsList:
        resFile = pars['resFile']
        resDataAll = np.loadtxt(resFile)
        resData = resDataAll[:, 2:5]


        resDataNoMean = resData - intRefMean

        # temp2 = np.dot(axesExchangeMat, intRefEvecs.T)
        # temp = np.dot(refEvecs, temp2)
        # temp1 = np.diag(np.sign(np.diag(temp)))
        # #
        # temp = np.dot(refEvecs, np.dot(axesExchangeMat, np.dot(temp1, intRefEvecs.T)))

        resDataTargetProj = np.dot(temp.T, resDataNoMean.T).T
        outSWCData = resDataAll.copy()
        outSWCData[:, 2:5] = resDataTargetProj + refMean

        resFileStub = os.path.split(resFile)[1][:-4]
        outSWC = os.path.join(outDir, "{}.swc".format(resFileStub))

        writeSWC_numpy(outSWC, outSWCData)


if __name__ == "__main__":

    assert len(sys.argv) == 5, "Improper Usage! Please use as:\n" \
                               "python {} <parFile> <source refSWC> <target refSWC> <outDir>".format(sys.argv[0])

    parFile = sys.argv[1]
    sourceRefSWC = sys.argv[2]
    targetRefSWC = sys.argv[3]
    outDir = sys.argv[4]
    projectToRef(parFile, sourceRefSWC, targetRefSWC, outDir)