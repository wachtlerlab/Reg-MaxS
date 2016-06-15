import os
import json
import numpy as np
from GJEMS.misc.LOBOSC import linearOrdering, calcClusterCrossing, orderMatrix
from GJEMS.directPixelBased.iterativeRegistration import calcOverlap
from matplotlib import pyplot as plt
import numpy as np
plt.ion()

homeFolder = os.path.expanduser('~')

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = '/home/ajay/DataAndResults/morphology/OriginalData/ChalupaRGCBi'
# expNames = [
#             'cell-116-trace.CNG',
#             'cell-122-trace.CNG',
#             'cell-126-trace.CNG',
#             'cell-129-trace.CNG',
#
#             'cell-213-trace.CNG',
#             'cell-123-trace.CNG',
#             'cell-188-trace.CNG',
#             'cell-169-trace.CNG',
#
#             'cell-177-trace.CNG',
#             'cell-183-trace.CNG',
#             'cell-206-trace.CNG',
#             'cell-232-trace.CNG',
#
#             ]
# refInd = 0
#
# resDir = '/home/ajay/DataAndResults/morphology/directPixelBased/ChalupaRGCBi'
# ----------------------------------------------------------------------------------------------------------------------

# dirPath = '/home/ajay/DataAndResults/morphology/OriginalData/JefferisvPN'
# expNames = [
#             'JBF3LLHSKELETON.CNG',  #0
#             'WKA7L.CNG',            #0.6758241758241759
#             'JBD2LLHskeleton.CNG',  #0.6029411764705883
#             'LHD1RLHSKELETON.CNG',  #0.6386138613861386
#
#             'KLA2L.CNG',            #0.8031914893617021
#             'LBE4R.CNG',            #0.8305084745762712
#             'LLA2RLHSKELETON.CNG',  #0.7555555555555555
#             'NBA8L.CNG',            #0.7531914893617021
#             'NCB7L.CNG',            #0.746031746031746
#             'JCB4LLHSKELETON.CNG',  #0.7552742616033755
#
#             'LHA3LLHskeleton.CNG',  #0.7837837837837838
#             'LHE7LLHskeleton.CNG',  #0.7559808612440191
#             'UQB5R.CNG',            #0.7362637362637363
#             'LHD6RLHSKELETON.CNG',  #0.7743589743589744
#             'LHD6LHskeleton.CNG',   #0.84375
#
#             'LHA5LLHSKELETON.CNG',  #0.856353591160221
#             'UQB5L.CNG',            #0.827906976744186
#             ]
# refInd = 0
#
# resDir = '/home/ajay/DataAndResults/morphology/directPixelBased/JefferisvPN'

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = '/home/ajay/DataAndResults/morphology/OriginalData/ChiangRAL/'
#
# expNames = [
#                 'Trh-F-700063803.CNG',
#                 'Trh-F-500154803.CNG',
#                 'Trh-F-600071803.CNG',
#                 'Trh-F-500050803.CNG',
#                 'Trh-F-500093803.CNG',
#                 'Trh-F-700018803.CNG',
#                 'Trh-M-500051803.CNG',
#                 'Trh-F-500148803.CNG',
#                 'Trh-F-500106803.CNG',
#                 'fru-F-500008803.CNG',
#
#                 'Trh-F-500188804.CNG',
#                 'fru-M-100085804.CNG',
#                 'Trh-F-500010804.CNG',
#                 'fru-M-200080804.CNG',
#                 'Trh-F-000018804.CNG',
#                 'fru-M-100090804.CNG',
#                 'Trh-M-100056804.CNG',
#                 'Trh-F-600083804.CNG',
#                 'Trh-M-400048804.CNG',
#                 'Trh-M-900048804.CNG',
#
#                 'Trh-F-600102801.CNG',
#                 'Trh-M-600091801.CNG',
#                 'Trh-F-600074801.CNG',
#                 'Trh-F-300082801.CNG',
#                 'Trh-F-600093801.CNG',
#                 'Trh-M-600089801.CNG',
#                 'Trh-M-500058801.CNG',
#                 'Trh-F-600085801.CNG',
#                 'Trh-M-600010801.CNG',
#                 'Trh-M-600074801.CNG',
#             ]
#
# refInd = 0
#
# resDir = '/home/ajay/DataAndResults/morphology/directPixelBased/ChiangRAL'
# if not os.path.isdir(resDir):
#     os.mkdir(resDir)

# ----------------------------------------------------------------------------------------------------------------------

# dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-1_Foragers_DB')
#
# expNames = [
#             'HB130425-1-DB',
#             'HB130326-2-DB',
#             'HB140424-1-DB',
#             'HB130408-1-DB',
#             'HB130322-1-DB',
#             'HB130313-4-DB',
#             'HB130501-2-DB',
#             'HB130705-1-DB',
#             ]
# refInd = 0
#
# resDir = os.path.join(homeFolder, 'DataAndResults/morphology/AllAll/DL-Int-Foragers_DB')
# gridsizes = [40.0, 20.0, 10.0]
# ----------------------------------------------------------------------------------------------------------------------

dirPath = os.path.join(homeFolder, 'DataAndResults/morphology/OriginalData/DL-Int-1_Foragers_VB')

expNames = [
            'HB130425-1-VB',
            'HB130326-2-VB',
            'HB140424-1-VB',
            'HB130408-1-VB',
            'HB130322-1-VB',
            'HB130313-4-VB',
            'HB130501-2-VB',
            'HB130705-1-VB',
            ]
refInd = 0

resDir = os.path.join(homeFolder, 'DataAndResults/morphology/AllAll/DL-Int-Foragers_VB')
gridsizes = [40.0, 20.0, 10.0]
# ----------------------------------------------------------------------------------------------------------------------

allVals = {g: [] for g in gridsizes}
figs = {g: [] for g in gridsizes}
# for refInd, refName in enumerate(expNames):
for g in gridsizes:
    for refInd, refName in enumerate(expNames):
        temp = []
        for expInd, expName in enumerate(expNames):
            if expInd == refInd:
                temp.append(1)
            else:
                alignedFName = os.path.join(resDir, expName + '-' + refName + '.swc')
                dis = calcOverlap(os.path.join(dirPath, expNames[refInd] + '.swc'), alignedFName, g)
                temp.append(1 - dis)
        allVals[g].append(temp)


    allVals[g] = np.array(allVals[g])
    vals = allVals[g]
    valsSymm = 0.5 * (vals + vals.T)
    # vals[range(vals.shape[0]), range(vals.shape[1])] = vals.mean()

    lo, valsSymmOrdered = linearOrdering(valsSymm)
    cc = calcClusterCrossing(valsSymmOrdered, 2)
    valsOrdered = orderMatrix(vals, lo)


    fig, ax = plt.subplots(figsize=(10, 8))
    figs[g].append(fig)
    im = ax.imshow(vals, interpolation='None')
    ax.set_yticks(range(len(expNames)))
    ax.set_yticklabels(expNames)
    ax.set_xticks(range(len(expNames)))
    ax.set_xticklabels(expNames, rotation=90)
    ax.set_title('Unordered ' + str(g))
    fig.colorbar(im, ax=ax, use_gridspec=True)

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    figs[g].append(fig1)
    ax1.imshow(valsOrdered, interpolation='None')
    ax1.set_yticks(range(len(expNames)))
    ax1.set_yticklabels([expNames[x] for x in lo])
    ax1.set_xticks(range(len(expNames)))
    ax1.set_xticklabels([expNames[x] for x in lo], rotation=90)
    ax1.set_title('Ordered ' + str(g))

    fig2, ax2 = plt.subplots(figsize=(10, 8))
    figs[g].append(fig2)
    ax2.plot(np.arange(vals.shape[0] - 1) + 0.5, cc[:-1], 'b-o')
    ax2.set_xticks(np.arange(vals.shape[0]))
    ax2.set_xticklabels([expNames[x] for x in lo], rotation=90)
    ax2.set_title('Cluster Crossing ' + str(g))


    for f in figs[g]:
        f.tight_layout()
        f.canvas.show()