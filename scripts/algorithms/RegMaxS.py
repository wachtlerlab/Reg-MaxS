import sys
from RegMaxSCore.iterativeRegistration import IterativeRegistration
from RegMaxSCore.misc import parFileCheck
import os

def runRegMaxS(parFile, parNames):
    parsList = parFileCheck(parFile, parNames)

    for pars in parsList:
        print('Current Parameters:')
        for parN, parV in pars.iteritems():
            print('{}: {}'.format(parN, parV))

        resFile = pars['resFile']
        refSWC = pars['refSWC']
        testSWC = pars['testSWC']

        if os.path.isfile(resFile):

            ch = raw_input('File exists: ' + resFile + '\nDelete(y/n)?')
            if ch == 'y':
                os.remove(resFile)
            else:
                quit()

        resDir = os.path.split(resFile)[0]
        if not os.path.exists(resDir):
            raise(ValueError('Could not create result file in specified directory: {}'.format(resDir)))

        assert os.path.isfile(refSWC), 'Could  not find {}'.format(refSWC)
        assert os.path.isfile(testSWC), 'Could  not find {}'.format(testSWC)

        iterReg = IterativeRegistration(refSWC=pars['refSWC'],
                                        gridSizes=pars['gridSizes'],
                                        rotBounds=pars['rotBounds'],
                                        transBounds=pars['transBounds'],
                                        transMinRes=pars['transMinRes'],
                                        scaleMinRes=pars['minScaleStepSize'],
                                        rotMinRes=pars['rotMinRes'],
                                        nCPU=pars['nCPU'])

        iterReg.performReg(SWC2Align=pars['testSWC'],
                           resFile=pars['resFile'],
                           scaleBounds=pars['scaleBounds'],
                           inPartsDir=pars['inPartsDir'],
                           outPartsDir=pars['outPartsDir'],
                           retainTempFiles=pars['retainTempFiles'])


if __name__ == '__main__':

    from RegMaxSCore.RegMaxSPars import RegMaxSParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python RegMaxS.py parFile\''

    parFile = sys.argv[1]

    runRegMaxS(parFile, RegMaxSParNames)
