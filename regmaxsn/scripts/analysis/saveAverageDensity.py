import os
from regmaxsn.core.plotDensities import DensityVizualizations, writeTIFF
from regmaxsn.core.transforms import compose_matrix
import numpy as np
from matplotlib import pyplot as plt
from regmaxsn.core.RegMaxSPars import DensitySaveParNames
from regmaxsn.core.misc import parFileCheck
homeFolder = os.path.expanduser('~')
import sys


def saveAverageDensity(regMaxSParFile, refSWC, outFile, gridUnitSize, sigma, reflections, rotations,
                       onlyTips=False):

    tempRotMat = compose_matrix(angles=np.deg2rad(rotations))


    initTrans = np.dot(np.diag(reflections), tempRotMat[:3, :3])


    resampleLen = 1

    gridUnitSize = [gridUnitSize] * 3
    sigmas = [sigma] * 3

    parsList = parFileCheck(regMaxSParFile, DensitySaveParNames)

    swcFiles = []

    for pars in parsList:
        resFile = pars['resFile']
        swcFiles.append(resFile)

    if onlyTips:

        masks = []
        for swcFile in swcFiles:

            data = np.loadtxt(swcFile)
            mask = [ptInd not in data[:, 6] for ptInd in data[:, 0]]
            masks.append(mask)

        densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen, masks=masks,
                                           pcaView=True, refSWC=refSWC, initTrans=initTrans)
        density, bins = densityViz.calculateDensity(swcFiles, sigmas)

    else:

        # densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
        #                                    pcaView='closestPCMatch', refSWC=refSWC, initTrans=initTrans)
        densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
                                           pcaView='assumeRegistered', refSWC=refSWC,
                                           initTrans=initTrans)
        density, bins = densityViz.calculateDensity(swcFiles, sigmas)
        # density, bins = calcMorphDensity(swcFiles, sigmas, gridUnitSize, resampleLen, pcaView=False, refSWC=refSWC)

    # # writeTIFF(density, outFile)
    np.savez_compressed(outFile, density=density, bins=bins, expNames=swcFiles)


def savePlotsTogether(densityDir, outDir):

    plt.rcParams["backend"] = 'agg'

    compressedFiles = [os.path.join(densityDir, x) for x in os.listdir(densityDir) if x.endswith('.npz')]

    mins = np.empty((len(compressedFiles), 3))
    maxs = np.empty((len(compressedFiles), 3))

    for comInd, comFile in enumerate(compressedFiles):
        compressedData = np.load(comFile)
        bins = compressedData['bins']

        mins[comInd, :] = [x.min() for x in bins]
        maxs[comInd, :] = [x.max() for x in bins]



    allMaxs = maxs.max(axis=0)
    allMins = mins.min(axis=0)

    del maxs, mins, bins

    for comInd, comFile in enumerate(compressedFiles):

        label = os.path.split(comFile)[1][:-4]

        print(("Doing {}".format(label)))
        compressedData = np.load(comFile)
        density = compressedData['density']
        bins = compressedData['bins']

        binWidths = [x[1] - x[0] for x in bins]
        finalExtents = [int((x - y) / z) for x, y, z in zip(allMaxs, allMins, binWidths)]
        tempDensity = np.zeros(finalExtents)
        binInds = [(int((binAxis[0] - minAxis) / binWidth),
                    int((binAxis[-1] - minAxis) / binWidth))
                    for binAxis, minAxis, binWidth in zip(bins, allMins, binWidths)]

        tempDensity[binInds[0][0]: binInds[0][1],
                    binInds[1][0]: binInds[1][1],
                    binInds[2][0]: binInds[2][1]] = density


        # fig1, ax1 = plt.subplots(figsize=(10, 8))
        density01 = np.max(tempDensity, axis=2)
        # im1 = ax1.imshow(density01, interpolation='none',
        #              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
        #
        #
        # fig1.colorbar(im1, ax=ax1, use_gridspec=True)
        # ax1.set_ylabel('Axis 1')
        # ax1.set_xlabel('Axis 2')
        # ax1.set_xticklabels([str(x * gridUnitSize[1]) for x in ax1.get_xticks()])
        # ax1.set_yticklabels([str(x * gridUnitSize[0]) for x in ax1.get_yticks()])
        #
        #
        #
        # fig2, ax2 = plt.subplots(figsize=(10, 8))
        density02 = np.max(tempDensity, axis=1)
        # im2 = ax2.imshow(density02, interpolation='none',
        #              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
        #
        #
        # fig2.colorbar(im2, ax=ax2, use_gridspec=True)
        # ax2.set_xlabel('Axis 3')
        # ax2.set_ylabel('Axis 1')
        # ax2.set_xticklabels([str(x * gridUnitSize[2]) for x in ax2.get_xticks()])
        # ax2.set_yticklabels([str(x * gridUnitSize[0]) for x in ax2.get_yticks()])
        #
        # for fig in [fig1, fig2]:
        #     fig.tight_layout()
        #     fig.canvas.draw()

        # scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
        # ax1.add_artist(scaleBar)
        # scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
        # ax2.add_artist(scaleBar)

        outFile = os.path.join(outDir, label)
        # fig1, ax1 = plt.subplots(figsize=np.array(density01.shape) / 300.)
        # ax1.imshow(density01, cmap=plt.cm.jet, vmax=1, vmin=0, interpolation='none')
        # ax1.axis('off')
        # # fig1.tight_layout()
        # fig1.savefig(outFile + '12' + '.ps', dpi=300, bbox_inches='tight', pad_inches=0, frameon=False)
        plt.imsave(outFile + '12.png', density01, cmap=plt.cm.jet, format='png', vmin=0, vmax=1)

        # fig2, ax2 = plt.subplots(figsize=np.array(density02.shape) / 300.)
        # ax2.imshow(density02, cmap=plt.cm.jet, vmax=1, vmin=0, interpolation='none')
        # ax2.axis('off')
        # # fig2.tight_layout()
        # fig2.savefig(outFile + '13' + '.ps', dpi=300, bbox_inches='tight', pad_inches=0, frameon=False)
        plt.imsave(outFile + '13.png', density02, cmap=plt.cm.jet, format='png', vmin=0, vmax=1)

        del tempDensity


def savePlotsSingle(npCompressedFile, label, outDir):

    plt.rcParams["backend"] = 'agg'

    compressedData = np.load(npCompressedFile)
    density = compressedData['density']
    # fig1, ax1 = plt.subplots(figsize=(10, 8))
    density01 = np.max(density, axis=2)
    # im1 = ax1.imshow(density01, interpolation='none',
    #              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
    #
    #
    # fig1.colorbar(im1, ax=ax1, use_gridspec=True)
    # ax1.set_ylabel('Axis 1')
    # ax1.set_xlabel('Axis 2')
    # ax1.set_xticklabels([str(x * gridUnitSize[1]) for x in ax1.get_xticks()])
    # ax1.set_yticklabels([str(x * gridUnitSize[0]) for x in ax1.get_yticks()])
    #
    #
    #
    # fig2, ax2 = plt.subplots(figsize=(10, 8))
    density02 = np.max(density, axis=1)
    # im2 = ax2.imshow(density02, interpolation='none',
    #              cmap=plt.cm.jet, vmin=0, vmax=1, aspect='equal')
    #
    #
    # fig2.colorbar(im2, ax=ax2, use_gridspec=True)
    # ax2.set_xlabel('Axis 3')
    # ax2.set_ylabel('Axis 1')
    # ax2.set_xticklabels([str(x * gridUnitSize[2]) for x in ax2.get_xticks()])
    # ax2.set_yticklabels([str(x * gridUnitSize[0]) for x in ax2.get_yticks()])
    #
    # for fig in [fig1, fig2]:
    #     fig.tight_layout()
    #     fig.canvas.draw()

    # scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
    # ax1.add_artist(scaleBar)
    # scaleBar = ScaleBar(gridUnitSize[1] * 1e-6)
    # ax2.add_artist(scaleBar)

    outFile = os.path.join(outDir, label)
    # fig1, ax1 = plt.subplots(figsize=np.array(density01.shape) / 300.)
    # ax1.imshow(density01, cmap=plt.cm.jet, vmax=1, vmin=0, interpolation='none')
    # ax1.axis('off')
    # # fig1.tight_layout()
    # fig1.savefig(outFile + '12' + '.ps', dpi=300, bbox_inches='tight', pad_inches=0, frameon=False)
    plt.imsave(outFile + '12.png', density01, cmap=plt.cm.jet, format='png', vmin=0, vmax=1)

    # fig2, ax2 = plt.subplots(figsize=np.array(density02.shape) / 300.)
    # ax2.imshow(density02, cmap=plt.cm.jet, vmax=1, vmin=0, interpolation='none')
    # ax2.axis('off')
    # # fig2.tight_layout()
    # fig2.savefig(outFile + '13' + '.ps', dpi=300, bbox_inches='tight', pad_inches=0, frameon=False)
    plt.imsave(outFile + '13.png', density02, cmap=plt.cm.jet, format='png', vmin=0, vmax=1)


    # densityViz.generateDensityColoredSSWC(swcFiles, [os.path.join(densityDir, x + '_density.sswc') for x in expNames],
    #                                       density)



if __name__ == "__main__":

    if len(sys.argv) == 9 and sys.argv[1] == "saveData":
        parFile = sys.argv[2]
        refSWC = sys.argv[3]
        outFile = sys.argv[4]
        gridUnitSize = float(sys.argv[5])
        sigma = float(sys.argv[6])
        reflections = np.array([int(x) for x in sys.argv[7].split()])
        rotations = np.array([float(x) for x in sys.argv[8].split()])
        saveAverageDensity(parFile, refSWC, outFile, gridUnitSize, sigma, reflections, rotations)
    elif len(sys.argv) == 5 and sys.argv[1] == "savePlotsSingle":
        npCompressedFile = sys.argv[2]
        label = sys.argv[3]
        outDir = sys.argv[4]
        savePlotsSingle(npCompressedFile, label, outDir)
    elif len(sys.argv) == 4 and sys.argv[1] == 'savePlotsTogether':
        densityDir = sys.argv[2]
        outDir = sys.argv[3]
        savePlotsTogether(densityDir, outDir)
    else:
        raise ValueError




