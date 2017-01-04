# Based on D2 measure of the Peng lab, which first resamples all the swcs, then for each point of the reference swc
# finds the closest point in each test swc. The distances between the reference point and the closest test points are
# used to quantify the how well a method has worked.

import os
from RegMaxSCore.swcFuncs import resampleSWC
from scipy.spatial import cKDTree
import numpy as np
from multiprocessing import cpu_count
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

mplPars = {'text.usetex': True,
           'axes.labelsize': 'large',
           'font.family': 'sans-serif',
           'font.sans-serif': 'computer modern roman',
           'font.size': 42,
           'font.weight': 'black',
           'xtick.labelsize': 36,
           'ytick.labelsize': 36,
           'legend.fontsize': 36,
           }
homeFolder = os.path.expanduser('~')
plt.ion()
sns.set(rc=mplPars)

class DataSet(object):

    def __init__(self, label, refSWC, testSWCSets):

        self.label = label
        self.refSWC = refSWC
        self.testSWCSets = testSWCSets



    def calcMinDists(self, minLen):

        allMinDists = {}
        thrash, resamRefPts = resampleSWC(self.refSWC, minLen)

        for testSWCSetName, testSWCSet in self.testSWCSets.iteritems():

            minDists = np.empty((resamRefPts.shape[0], len(testSWCSet)))

            for testInd, testSWC in enumerate(testSWCSet):

                thrash, resampTestPts = resampleSWC(testSWC, minLen)
                testKDTree = cKDTree(resampTestPts, compact_nodes=True, leafsize=100)
                minDists[:, testInd] = testKDTree.query(resamRefPts, n_jobs=cpu_count() - 1)[0]

            allMinDists[testSWCSetName] = minDists

        return allMinDists








dataSets = {}

# ----------------------------------------------------------------------------------------------------------------------

refPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Registered', 'chiangOMB')
refExpName = 'VGlut-F-500085.CNG'
refSWC = os.path.join(refPath, refExpName + '.swc')
testSWCSets = {}
dataSetName = 'ALPN'

testExpNames = [
            # 'VGlut-F-500085_registered',
            'VGlut-F-700500.CNG',
            'VGlut-F-700567.CNG',
            'VGlut-F-500471.CNG',
            'Cha-F-000353.CNG',
            'VGlut-F-600253.CNG',
            'VGlut-F-400434.CNG',
            'VGlut-F-600379.CNG',
            'VGlut-F-700558.CNG',
            'VGlut-F-500183.CNG',
            'VGlut-F-300628.CNG',
            'VGlut-F-500085.CNG',
            'VGlut-F-500031.CNG',
            'VGlut-F-500852.CNG',
            'VGlut-F-600366.CNG'
            ]
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'directPixelBased', 'chiangOMB')
label = 'Reg-MaxS-N'
testSWCs = [os.path.join(testPath, x + '_norm.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'RefPCA', 'chiangOMB')
label = 'PCA-Based'
testSWCs = [os.path.join(testPath, x + '.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
dataSets[dataSetName] = DataSet(dataSetName, refSWC, testSWCSets)
# ----------------------------------------------------------------------------------------------------------------------

refPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Registered', 'chiangLLC')
refExpName = 'Gad1-F-000062.CNG'
refSWC = os.path.join(refPath, refExpName + '.swc')
testSWCSets = {}
dataSetName = 'LCInt'

testExpNames = [
            'Gad1-F-000062.CNG',
            'Cha-F-000012.CNG',
            'Cha-F-300331.CNG',
            'Gad1-F-600000.CNG',
            'Cha-F-000018.CNG',
            'Cha-F-300051.CNG',
            'Cha-F-400051.CNG',
            'Cha-F-200000.CNG'
            ]
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'directPixelBased', 'chiangLLC')
label = 'Reg-MaxS-N'
testSWCs = [os.path.join(testPath, x + '_norm.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'RefPCA', 'chiangLLC')
label = 'PCA-Based'
testSWCs = [os.path.join(testPath, x + '.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
dataSets[dataSetName] = DataSet(dataSetName, refSWC, testSWCSets)
# ----------------------------------------------------------------------------------------------------------------------

refPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'Registered', 'chiangOPSInt')
refExpName = 'Trh-F-000047.CNG'
testSWCSets = {}

testExpNames = [
            'Trh-F-000047.CNG',
            'Trh-M-000143.CNG',
            'Trh-F-000092.CNG',
            'Trh-F-700009.CNG',
            'Trh-M-000013.CNG',
            'Trh-M-000146.CNG',
            # 'Trh-M-100009.CNG',
            'Trh-F-000019.CNG',
            'Trh-M-000081.CNG',
            'Trh-M-900003.CNG',
            'Trh-F-200035.CNG',
            'Trh-F-200015.CNG',
            'Trh-M-000040.CNG',
            'Trh-M-600023.CNG',
            'Trh-M-100048.CNG',
            'Trh-M-700019.CNG',
            'Trh-F-100009.CNG',
            'Trh-M-400000.CNG',
            'Trh-M-000067.CNG',
            'Trh-M-000114.CNG',
            'Trh-M-100018.CNG',
            'Trh-M-000141.CNG',
            'Trh-M-900019.CNG',
            'Trh-M-800002.CNG'
]

dataSetName = 'OPInt'
refSWC = os.path.join(refPath, refExpName + '.swc')
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'directPixelBased', 'chiangOPSInt')
label = 'Reg-MaxS-N'
testSWCs = [os.path.join(testPath, x + '_norm.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
testPath = os.path.join(homeFolder, 'DataAndResults', 'morphology', 'RefPCA', 'chiangOPSInt')
label = 'PCA-Based'
testSWCs = [os.path.join(testPath, x + '.swc') for x in testExpNames]
testSWCSets[label] = testSWCs
# -------------------------------------------------------------------------------------------------
dataSets[dataSetName] = DataSet(dataSetName, refSWC, testSWCSets)
# ----------------------------------------------------------------------------------------------------------------------


minDists = {}
allMinDistStats = {}
fig1, ax1 = plt.subplots(figsize=(14, 11.2))
fig2, ax2 = plt.subplots(figsize=(14, 11.2))

for dataSetName, dataSet in dataSets.iteritems():

    temp = dataSet.calcMinDists(0.1)
    minDists[dataSetName] = temp
    dataSetMinDists = []
    for methodName, testSetMinDists in temp.iteritems():
        methodMinDistStats = pd.DataFrame(data=None,
                                          columns=['Mean of minimum distances(um)',
                                                   'Standard Deviation of \nminimum distances(um)',
                                                   'Method',
                                                   'Group Name'])
        methodMinDistStats.loc[:, 'Mean of minimum distances(um)'] = testSetMinDists.mean(axis=1)
        methodMinDistStats.loc[:, 'Standard Deviation of \nminimum distances(um)'] = testSetMinDists.std(axis=1)
        methodMinDistStats.loc[:, 'Method'] = methodName
        methodMinDistStats.loc[:, 'Group Name'] = dataSetName
        dataSetMinDists.append(methodMinDistStats)

    allMinDistStats[dataSetName] = pd.concat(dataSetMinDists)

minDistsStats1DF = pd.concat(allMinDistStats.itervalues())

sns.boxplot(x='Group Name', y='Mean of minimum distances(um)', hue='Method', data=minDistsStats1DF,
            ax=ax1, whis='range')
sns.boxplot(x='Group Name', y='Standard Deviation of \nminimum distances(um)', hue='Method', data=minDistsStats1DF,
            ax=ax2, whis='range')

for fig in [fig1, fig2]:
    fig.tight_layout()
    fig.canvas.draw()


# print('Reasampling Ref')
# refRPts = resampleSWC(refSWC, 0.1)[1][:, :3]
# print('Resampling tests')
# testRPts = [resampleSWC(x, 0.1)[1][:, :3] for x in testSWCs]
# print('Creating testKDtrees')
# testKDTrees = [cKDTree(x, compact_nodes=True, leafsize=100) for x in testRPts]
#
# minDists = np.empty((refRPts.shape[0], len(testRPts)))
#
# for testInd, testKDTree in enumerate(testKDTrees):
#     print('Calculating minDists for ' + testExpNames[testInd])
#     minDists[:, testInd] = testKDTree.query(refRPts, n_jobs=cpu_count() - 1)[0]
#
# # minDists[minDists == np.inf]
#
# meanMinDists = minDists.mean()
# meanStdMinDists = minDists.std(axis=1).mean()
#
#
# print(dataSetName + part, label + ' Results:')
# print('Mean of all minDists: ' + str(meanMinDists))
# print('Mean Std of minDists: ' + str(meanStdMinDists))





