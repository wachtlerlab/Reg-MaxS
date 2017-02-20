import os
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import json
from core.RegMaxSPars import RegMaxSParNames
from core.misc import parFileCheck

homeFolder = os.path.expanduser('~')

plt.ion()
mplPars = { 'text.usetex'       :    True,
            'axes.labelsize'    :   'large',
            'font.family'       :   'sans-serif',
            'font.sans-serif'   :   'computer modern roman',
            'font.size'         :    24,
            'font.weight'       :   'black',
            'xtick.labelsize'   :    20,
            'ytick.labelsize'   :    20,
            }

# Example colFunc, takes refSWC and testSWC and returns an object that can be passed to matplotlib plotting argument
# color. For example return objects could be 'b' (blue), 'r' (red) and  [0, 0, 1] (green).
# def colFunc(refSWC, testSWC):
#
#     testInd = int(os.path.split(testSWC)[1][25:-4])
#
#     if testInd in range(2, 5):
#         return 'r'
#     else:
#         return 'b'

colFunc = None

def regErrorVsAIScaling(parFile, colFunc=None):
    # Axis 1: neuron pairs; Axis 2: (reg accuracy, anisotropic scaling)

    parsList = parFileCheck(parFile, RegMaxSParNames)
    translErrStats = np.empty((len(parsList), 2))
    for parInd, par in enumerate(parsList):

        refSWC = par['refSWC']
        testSWC = par['testSWC']
        resFile = par['resFile']
        thresh = par['gridSizes'][-1]

        print('Doing ' + repr((refSWC, resFile)))

        origJSON = testSWC[:-4] + '.json'

        if os.path.isfile(origJSON):
            with open(origJSON, 'r') as fle:
                pars = json.load(fle)
                scales = np.array(pars['scale'])
        else:
            raise(IOError('File not found: {}'.format(origJSON)))

        scalesOrdered = np.sort(scales)
        scalesRelative = np.mean([scalesOrdered[0] / scalesOrdered[1],
                                  scalesOrdered[0] / scalesOrdered[2],
                                  scalesOrdered[1] / scalesOrdered[2]])

        refPts = np.loadtxt(refSWC)[:, 2:5]
        testPts = np.loadtxt(resFile)[:, 2:5]

        if refPts.shape[0] != testPts.shape[0]:

            print('Number of points do not match for ' + refSWC + 'and' + testSWC)
            continue


        ptDiff = np.linalg.norm(refPts - testPts, axis=1)
        translErrStats[parInd, 0] = 100 * sum(ptDiff <= thresh) / float(ptDiff.shape[0])
        translErrStats[parInd, 1] = scalesRelative

    sns.set(rc=mplPars)
    with sns.axes_style('whitegrid'):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

        for parInd, vals in enumerate(translErrStats):
            try:
                if colFunc:
                    col = colFunc(parsList[parInd]['refSWC'], parsList[parInd]['testSWC'])
                else:
                    col = 'b'

                ax.plot(vals[1], vals[0], color=col, marker='o', ls='None', ms=10)
            except Exception as e:
                raise(Exception('Problem with plotting. There could be a problem with argument colFunc'))

    ax.set_xlabel('measure of anisotropic scaling')
    ax.set_ylabel('\% points closer than \nthe lowest grid size')
    ax.set_ylim(-10, 110)

    fig.tight_layout()

    return fig

if __name__ == '__main__':

    import sys
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python refErrorVsAnisotropicscaling.py parFile\''

    parFile = sys.argv[1]
    fig = regErrorVsAIScaling(parFile, colFunc)
    raw_input('Press any key to close figures and quit:')