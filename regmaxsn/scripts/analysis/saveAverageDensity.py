import os
from regmaxsn.core.plotDensities import DensityVizualizations, writeTIFF
import numpy as np
from matplotlib import pyplot as plt
from regmaxsn.core.RegMaxSPars import DensitySaveParNames
from regmaxsn.core.misc import parFileCheck
homeFolder = os.path.expanduser('~')
import sys

def saveAverageDensity(regMaxSParFile, outFile, gridUnitSize, sigma, onlyTips=False):

    resampleLen = 1

    gridUnitSize = [gridUnitSize] * 3
    sigmas = [sigma] * 3

    parsList = parFileCheck(regMaxSParFile, DensitySaveParNames)

    swcFiles = []

    for pars in parsList:
        resFile = pars['resFile']
        swcFiles.append(resFile)
        refSWC = pars["refSWC"]

    if onlyTips:

        masks = []
        for swcFile in swcFiles:

            data = np.loadtxt(swcFile)
            mask = map(lambda ptInd: ptInd not in data[:, 6], data[:, 0])
            masks.append(mask)

        densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen, masks=masks,
                                           pcaView=True, refSWC=refSWC)
        density, bins = densityViz.calculateDensity(swcFiles, sigmas)

    else:

        # densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
        #                                    pcaView='closestPCMatch', refSWC=refSWC, initTrans=initTrans)
        densityViz = DensityVizualizations(swcFiles, gridUnitSize, resampleLen,
                                           pcaView='assumeRegistered', refSWC=refSWC)
        density, bins = densityViz.calculateDensity(swcFiles, sigmas)
        # density, bins = calcMorphDensity(swcFiles, sigmas, gridUnitSize, resampleLen, pcaView=False, refSWC=refSWC)

    # # writeTIFF(density, outFile)
    np.savez_compressed(outFile, density=density, bins=bins, expNames=swcFiles)


def savePlots(npCompressedFile, label, outDir):

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

    if len(sys.argv) == 6 and sys.argv[1] == "saveData":
        parFile = sys.argv[2]
        outFile = sys.argv[3]
        gridUnitSize = float(sys.argv[4])
        sigma = float(sys.argv[5])
        saveAverageDensity(parFile, outFile, gridUnitSize, sigma)
    elif len(sys.argv) == 5 and sys.argv[1] == "savePlots":
        npCompressedFile = sys.argv[2]
        label = sys.argv[3]
        outDir = sys.argv[4]
        savePlots(npCompressedFile, label, outDir)
    else:
        raise(ValueError("Improper Usage! Please use as:\n"
                         "python {fle} saveData <RegMaxSParFile> <outFile> "
                         "<spatial discretization size> <Gaussian smoothing sigma>\n"
                         "python {fle} savePlots <compressed Data file> <label>"))



