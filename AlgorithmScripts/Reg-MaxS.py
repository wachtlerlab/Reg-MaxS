import sys
import json
from RegMaxSCore.iterativeRegistration import IterativeRegistration


def runRegMaxS(parFile, parNames):
    with open(parFile, 'r') as fle:
        parsList = json.load(fle)
        assert type(parsList) == list, 'Parameter file does not contain a list of dictionaries as is the requirement.'
        for parInd, par in enumerate(parsList):
            assert type(par) == dict, 'Parameter set # {} in {} not a list'.format(parInd, parFile)

            for pn in parNames:
                assert pn in par, 'Parameter {} not found in ' \
                                  'parameter set # {} of {} is improper'.format(pn, parInd, parFile)

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
