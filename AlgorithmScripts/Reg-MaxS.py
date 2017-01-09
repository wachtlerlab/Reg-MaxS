import sys
import json
from RegMaxSCore.iterativeRegistration import IterativeRegistration
from RegMaxSCore.misc import parFileCheck

def runRegMaxS(parFile, parNames):
    parsList = parFileCheck(parFile, parNames)

    for pars in parsList:
        print('Current Parameters:')
        for parN, parV in pars.iteritems():
            print('{}: {}'.format(parN, parV))

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
                           partsDir=pars['partsDir'],
                           retainTempFiles=pars['retainTempFiles'])


if __name__ == '__main__':

    from RegMaxSCore.RegMaxSPars import RegMaxSParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python Reg-MaxS.py parFile\''

    parFile = sys.argv[1]

    runRegMaxS(parFile, RegMaxSParNames)
