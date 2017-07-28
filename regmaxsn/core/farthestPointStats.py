from regmaxsn.core.swcFuncs import readSWC_numpy, resampleSWC
from scipy.spatial import ConvexHull
import pandas as pd
from scipy.spatial.distance import cdist


def maxDistStats(swcFiles):

    swcHullVerts = []
    swcDatas = []
    swcDataSeries =[]
    swcHullVertsSeries = []

    maxDistStatsDF = pd.DataFrame()

    for swcFile in swcFiles:
        totalLen, swcDataWithR = resampleSWC(swcFile, 0.5)
        swcData = swcDataWithR[:, :3]
        swcDatas.append(swcData)
        swcDataSeries.append(pd.Series([tuple(x) for x in swcData]))
        hull = ConvexHull(swcData)
        swcHullVert = swcData[hull.vertices, :]
        swcHullVerts.append(swcHullVert)
        swcHullVertsSeries.append(pd.Series([tuple(x) for x in swcHullVert]))

    for swcInd1, swcData1 in enumerate(swcDatas):

        swcInds = range(len(swcFiles))
        swcInds.remove(swcInd1)
        swcDataSeries1 = swcDataSeries[swcInd1]

        for swcInd2 in swcInds:
            swcHullVert2 = swcHullVerts[swcInd2]
            swcHullVertSeries2 = swcHullVertsSeries[swcInd2]

            distMat = cdist(swcData1, swcHullVert2)

            maxDistsInds = distMat.argmax(axis=1)

            tempDF = pd.DataFrame()
            tempDF["source point"] = swcDataSeries1
            tempDF["maximum distance"] = distMat.max(axis=1)
            tempDF["destination farthest point"] = swcHullVertSeries2[maxDistsInds].values
            tempDF["destination SWC"] = swcFiles[swcInd2]

            maxDistStatsDF = maxDistStatsDF.append(tempDF, ignore_index=True)

    return maxDistStatsDF


